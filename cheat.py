import random


class Card:
    def __init__(self, suit, name, value):
        self.suit = suit
        self.name = name
        self.value = value

    def __str__(self):
        return self.name + " of " + self.suit + "s"


class Cards:
    def __init__(self, suits, types):
        self.suits = suits
        self.types = types
        self.cards = []

    def add_card(self, Card):
        self.cards.append(Card)

    def num_cards(self):
        return len(self.cards)

    def __shuffle__(self):
        random.shuffle(self.cards)

    def pop_card(self, where=-1):
        Card = self.cards.pop(where)

        return Card

    def show_cards(self):
        for Card in self.cards:
            print(Card.__str__())

    def show_cards_with_indices(self):
        i = 0
        for Card in self.cards:
            print(str(i) + ": " + Card.__str__())
            i += 1


class Hand(Cards):
    def __init__(self, suits, types):
        Cards.__init__(self, suits, types)


class Player:
    def __init__(self, name, id, suits, types):
        self.name = name
        self.id = id
        self.hand = Hand(suits, types)
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

class Human(Player):
    def __init__(self, name, id, suits, types):
        Player.__init__(self, name, id, suits, types)

    def play(self, current_type_index):
        print("--- My cards ---")
        self.hand.show_cards_with_indices()
        print("----------------")
        index_to_play = 0

        while True:
            try:
                index_to_play = int(input("Enter which card to play\n> "))
            except ValueError:
                print("Must be an integer.")
                continue

            if not 0 <= index_to_play <= self.hand.num_cards() - 1:
                print("Invalid index.")
                continue
            else:
                break

        return [self.hand.pop_card(index_to_play)]


class Bot(Player):
    def __init__(self, name, id, suits, types):
        Player.__init__(self, name, id, suits, types)

    def play(self, current_type_index):
        print("A bot is gonna play! " + self.name)
        return [self.hand.pop_card()]


class Deck(Cards):
    def __init__(self, suits, types):
        Cards.__init__(self, suits, types)

        for i in range(len(self.types)):
            for suit in self.suits:
                self.add_card(Card(suit, self.types[i], i + 1))


class Game:
    def __init__(self, suits, types):
        self.suits = suits
        self.types = types
        self.players = []
        self.num_players = 0
        self.pool = []
        self.current_type_index = 0
        self.max_card_value = len(types) - 1
        self.player_index_to_play = 0
        name = ""

        while True:
            try:
                self.num_players = int(input(
                    "Enter number of AI players. (min 2, max 7)\n> "
                ))
            except ValueError:
                print("Must be an integer.")
                continue

            if not 2 <= self.num_players <= 8:
                print("min 2, max 7")
                continue
            else:
                self.num_players += 1
                break

        # get player name
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

        if name == "no lol":
            self.player_id = -1
        else:
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
        return len(self.pool)

    def round(self):
        cur_player = self.get_player(self.player_index_to_play)
        cur_type = self.current_type_to_play(self.current_type_index)

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

        cards_placed = cur_player.play(cur_type)
        self.pool.extend(cards_placed)

        # determine next player, next type to play
        self.current_type_index += 1
        if self.current_type_index > self.max_card_value:
            self.current_type_index = 0
        self.player_index_to_play += 1
        if self.player_index_to_play == self.num_players:
            self.player_index_to_play = 0

        print("\n")

suits = ["Spade", "Club", "Heart", "Diamond"]
types = [
    "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen",
    "King"
]
