import random
from cards import Cards, Deck
from player import Human, Bot


class Game:
    def __init__(
        self, suits, types, Simulate=False, show_outputs=True, num_players=0,
        min_p=3, max_p=8,
    ):
        self.suits = suits
        self.types = types
        self.players = []
        self.min_players = min_p
        self.max_players = max_p
        self.num_players = num_players
        self.pool = Cards()
        self.current_type_index = 0
        self.max_card_value = len(types) - 1
        self.player_index_to_play = 0
        self.player_id = -1  # the Human player
        self.show_outputs = show_outputs
        self.winners = []

        name = ""
        if num_players == 0:
            while True:
                inp_msg = (
                    "Enter number of players. "
                    "(min " + str(self.min_players) + ", max " +
                    str(self.max_players) + ")\n> "
                )
                try:
                    self.num_players = int(input(inp_msg))
                except ValueError:
                    print("Must be an integer.")
                    continue

                if not (
                    self.min_players <= self.num_players <= self.max_players
                ):
                    print(
                        "min " + str(self.min_players) + ", max " +
                        str(self.max_players)
                    )
                    continue
                else:
                    break

        # get player name
        if not Simulate:
            while True:
                try:
                    name = str(input("Enter your name!\n> "))
                except ValueError:
                    print("Must be a string.")
                    continue

                if name == "":
                    print("Enter a name.")
                    continue
                else:
                    break

            # assign player random turn number
            self.player_id = random.randint(0, self.num_players - 1)

        for i in range(self.num_players):
            if i == self.player_id:
                self.players.append(Human(
                    name, i, self.suits, self.types
                ))
            else:
                self.players.append(Bot(
                    "bot " + str(i), i, self.suits, self.types
                ))

        self.deck = Deck(self.suits, self.types)

    def get_player(self, player_index):
        return self.players[player_index]

    def get_type(self, type_index):
        return self.types[type_index]

    def deal(self):
        players_index = 0
        self.deck.__shuffle__()

        for i in range(self.deck.num_cards()):
            if players_index > self.num_players - 1:
                players_index = 0

            self.players[players_index].add_card_to_hand(self.deck.pop_card())
            players_index += 1

    def current_type_to_play(self):
        return self.get_type(self.current_type_index)

    def current_player_to_play(self):
        return self.get_player(self.player_index_to_play)

    def pool_size(self):
        return self.pool.num_cards()

    def round(self):
        cur_player = self.current_player_to_play()
        cur_type = self.current_type_to_play()

        if self.show_outputs:
            self.display_round_info(cur_player, cur_type)

        cards_placed = cur_player.play(cur_type, len(self.suits))
        num_placed = len(cards_placed)

        if self.show_outputs:
            print("\n~~~~~")
            print(
                cur_player.get_name() + " placed " + str(num_placed) +
                " cards"
            )
            print(
                "The pool now has " + str(self.pool_size() + num_placed) +
                " cards"
            )
            print("~~~~~\n")

        # add cards to pool
        for i in cards_placed:
            self.pool.add_card(cur_player.get_hand().get_card(int(i)))
        cur_player.get_hand().filter_cards(cards_placed)

        return num_placed

    # get the next player index to play that's not a winner. -1 if none
    def next_player(self, start, cur):
        cur += 1
        if cur == self.num_players:
            cur = 0

        # base case
        if cur == start:
            return -1

        if cur not in self.winners:
            return cur

        return self.next_player(start, cur)

    def display_round_info(self, cur_player, cur_type):
        print("\n")
        for i in range(0, 30):
            print("#", end="")
        print("")
        print("Current card type to play:")
        print(cur_type)
        print("---")
        print("Player to place cards:")
        print(cur_player.get_name())

        if cur_player == self.player_id:
            print("(It's your turn.)")

        print("---")
        print("Pool size:")
        print(str(self.pool_size()))

        for i in range(0, 30):
            print("#", end="")
        print("")

    def play_game(self):
        self.deal()
        while(True):
            num_placed = self.round()

            # check cheat
            accusers = []
            c = 0
            for P in self.players:
                if (
                    c not in self.winners and
                    not c == self.player_index_to_play
                ):
                    if P.call_cheat(self.current_type_index, self.pool_size()):
                        accusers.append(c)

                c += 1

            if len(accusers) > 0:
                accuser = accusers[0]
                receiver = accuser

                if self.show_outputs:
                    print("\n^^^^")
                    print(
                        self.get_player(accuser).get_name() +
                        " called cheat on " +
                        self.current_player_to_play().get_name()
                    )
                    print("^^^^\n")

                # check last num_placed cards to see if they were valid
                cheated = False
                for i in range(
                    self.pool_size() - num_placed, self.pool_size()
                ):
                    if not (self.pool.get_card(i).get_type() ==
                            self.current_type_to_play()):
                        cheated = True
                        receiver = self.player_index_to_play
                        break

                P = None
                msg = ""
                if cheated:
                    P = self.current_player_to_play()
                    msg += P.get_name() + " cheated!"
                else:
                    P = self.get_player(accuser)
                    msg += (
                        P.get_name() + " incorrectly accused " +
                        self.current_player_to_play().get_name()
                    )

                if self.show_outputs:
                    print(msg)
                    print("Here were the placed cards:")
                    # show the placed cards
                    self.pool.show_cards(
                        False,
                        None,
                        list(range(
                            self.pool_size() - num_placed,
                            self.pool_size())
                        )
                    )

                    print(
                        self.get_player(receiver).get_name() +
                        " has to pick up all " + str(self.pool_size()) +
                        " cards from the pool!"
                    )

                P.give_cards(self.pool)
                self.pool.clear()

            # if player has no more cards, add them to winners list
            if self.current_player_to_play().num_cards() == 0:
                self.winners.append(self.player_index_to_play)

            # determine next player, next type to play
            self.current_type_index += 1
            if self.current_type_index > self.max_card_value:
                self.current_type_index = 0

            next_player_index = self.next_player(self.player_index_to_play,
                                                 self.player_index_to_play)
            self.player_index_to_play = next_player_index

            if self.player_index_to_play == -1:
                break

        if self.show_outputs:
            print("\n\n~~~ Winners ~~~")
            c = 1
            for i in self.winners:
                print(str(c) + "  " + self.get_player(i).get_name())
                c += 1
