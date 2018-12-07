import random


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


class Card:
    def __init__(self, suit, name, value):
        self.suit = suit
        self.name = name
        self.value = value

    def __str__(self):
        return self.name + " of " + self.suit + "s"


class Cards:
    def __init__(self):
        self.cards = []

    def add_card(self, Card):
        self.cards.append(Card)

    def get_card(self, i):
        return self.cards[i]

    def num_cards(self):
        return len(self.cards)

    def __shuffle__(self):
        random.shuffle(self.cards)

    def pop_card(self, where=-1):
        Card = self.cards.pop(where)

        return Card

    def filter_cards(self, indices):
        new_cards = []
        i = 0
        for Card in self.cards:
            if i not in indices:
                new_cards.append(Card)
            i += 1

        self.cards = new_cards

    def get_card_string(self, i):
        return self.cards[i].__str__()

    def show_cards(
        self, show_indices=False, ignore=None, only=None, per_line=4
    ):
        to_show = []

        if (only is None):
            to_show = list(range(0, self.num_cards()))
        else:
            to_show = only
        if ignore is not None:
            to_show = [x for x in to_show if x not in ignore]

        length = len(to_show)
        if length > 0:
            data = []
            row = []
            last_i = to_show[-1]

            counter = 0
            for i in to_show:
                string = ""

                if show_indices:
                    string += "[" + str(i) + "] "

                string += self.get_card_string(i)
                row.append(string)

                if counter == per_line - 1:
                    data.append(row)
                    row = []
                    counter = 0
                else:
                    counter += 1
                    if i == last_i:
                        data.append(row)

            col_width = max(len(word) for row in data for word in row) + 2
            for row in data:
                print("".join(word.ljust(col_width) for word in row))


class Hand(Cards):
    def __init__(self):
        Cards.__init__(self)


class Player:
    def __init__(self, name, id, suits, types):
        self.name = name
        self.id = id
        self.hand = Hand()
        self.suits = suits
        self.types = types

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def get_hand(self):
        return self.hand

    def add_card_to_hand(self, Card):
        self.hand.add_card(Card)

    def play(self, current_type_index):
        pass

    def call_cheat(self, current_type_index, pool_size):
        pass


class Human(Player):
    def __init__(self, name, id, suits, types):
        Player.__init__(self, name, id, suits, types)

    def play(self, current_type_index):
        cmd = ""
        queue = []

        while True:
            print("--- Available cards to play ---")
            self.hand.show_cards(True, queue)
            print("--- My selection ---")
            self.hand.show_cards(False, None, queue)
            print("--------------------")

            cmd = input("Enter a command or type ? for help\n> ")

            if (cmd == "?"):
                self.show_instructions()
                continue

            # remove duplicates
            cmd = cmd.strip(",").split(",")
            no_dups = []
            for c in cmd:
                if c not in no_dups:
                    no_dups.append(c)
            cmd = no_dups

            if len(cmd) == 0:
                continue

            # verify input
            valid_cmd = True
            special_cmds = ["-1", "cheat", "clear", "undo", "done"]
            for p in cmd:
                if not (p in special_cmds and len(cmd) == 1):
                    if not represents_int(p):
                        print("Expected only integers separated by commas")
                        print("Got: " + p)

                        valid_cmd = False
                    elif not 0 <= int(p) <= self.hand.num_cards():
                        print(
                            "No card numbered " + p + " exists in your hand"
                        )

                        valid_cmd = False
                    elif p == -1 and len(cmd) > 1:
                        print("Can't call cheat while placing cards")
                        valid_cmd = False
                    elif int(p) in queue:
                        print(
                            "You're already going to place the card " +
                            "numbered " + p
                        )
                        valid_cmd = False

                    if not valid_cmd:
                            break
                else:
                    special = cmd[0]
                    if special == "-1" or special == "cheat":
                        print("LOL CHEAT")
                    elif special == "clear":
                        queue = []
                    elif special == "done":
                        if len(queue) == 0:
                            print("You haven't entered anything to play yet")
                        else:
                            return queue
                    elif special == "undo":
                        queue.pop()

                    valid_cmd = False
                    break

            if not valid_cmd:
                continue

            cmd = [int(x) for x in cmd]
            queue.extend(cmd)

    def show_instructions(self):
        print("--- Commands ---")
        print("To select a card, enter the number you see before it")
        print(
            "To enter multiple cards at once, separate card numbers with a " +
            "comma"
        )
        print("~~~")
        print("To call cheat, enter -1")
        print("~~~")
        print("To undo most recent card placement, enter 'undo'")
        print("~~~")
        print("To clear selection, enter 'clear'")
        print("----------------")

    def call_cheat(self, current_type_index):
        pass


class Bot(Player):
    def __init__(self, name, id, suits, types):
        Player.__init__(self, name, id, suits, types)

    def play(self, current_type_index):
        return [0]


class Deck(Cards):
    def __init__(self, suits, types):
        Cards.__init__(self)
        self.suits = suits
        self.types = types

        for i in range(len(self.types)):
            for suit in self.suits:
                self.add_card(Card(suit, self.types[i], i + 1))


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

        name = ""
        while True:
            if num_players == 0:
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

    def current_type_to_play(self, current_type_index):
        return self.get_type(current_type_index)

    def current_player_to_play(self, player_index_to_play):
        return self.get_player(player_index_to_play)

    def pool_size(self):
        return self.pool.num_cards()

    def round(self):
        cur_player = self.get_player(self.player_index_to_play)
        cur_type = self.current_type_to_play(self.current_type_index)
        cards_placed = cur_player.play(cur_type)

        if self.show_outputs:
            self.display_round_info(cur_player, cur_type)
            print("")

        # add cards to pool
        for i in cards_placed:
            self.pool.add_card(cur_player.get_hand().get_card(int(i)))
        cur_player.get_hand().filter_cards(cards_placed)

        # determine next player, next type to play
        self.current_type_index += 1
        if self.current_type_index > self.max_card_value:
            self.current_type_index = 0
        self.player_index_to_play += 1
        if self.player_index_to_play == self.num_players:
            self.player_index_to_play = 0

    def display_round_info(self, cur_player, cur_type):
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

    def play_game(self):
        self.deal()
        while(True):
            self.round()
            if (self.pool_size() == 52):
                break


suits = ["Spade", "Club", "Heart", "Diamond"]
types = [
    "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen",
    "King"
]

g = Game(suits, types, True)
g.play_game()
