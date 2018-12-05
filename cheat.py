import random


class Card:
    def __init__(self, suit, name, value):
        self.suit = suit
        self.name = name
        self.value = value

    def __str__(self):
        return self.name + " of " + self.suit + "s"


class Cards:
    def __init__(self, suits, values):
        self.suits = suits
        self.values = values
        self.cards = []

    def add_card(self, Card):
        self.cards.append(Card)

    def num_cards(self):
        return len(self.cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def pop_card(self):
        Card = self.cards.pop()

        return Card

    def show_cards(self):
        for Card in self.cards:
            print(Card.__str__())


class Hand(Cards):
    def __init__(self, suits, values):
        Cards.__init__(self, suits, values)


class Player:
    def __init__(self, name, id, suits, values):
        self.name = name
        self.id = id
        self.hand = Hand(suits, values)

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def get_hand(self):
        return self.hand

    def add_card_to_hand(self, Card):
        self.hand.add_card(Card)


class Human(Player):
    def __init__(self, name, id, suits, values):
        Player.__init__(self, name, id, suits, values)


class Bot(Player):
    def __init__(self, name, id, suits, values):
        Player.__init__(self, name, id, suits, values)


class Deck(Cards):
    def __init__(self, suits, values):
        Cards.__init__(self, suits, values)

        for i in range(13):
            for suit in self.suits:
                self.add_card(Card(suit, self.values[i], i + 1))


class Game:
    def __init__(self, suits, values):
        self.suits = suits
        self.values = values
        self.players = []
        self.num_players = 0
        self.pool = []
        self.current_card_type_index = 0
        self.max_card_type = 13
        self.player_index_to_play = 0

        while True:
            try:
                self.num_players = int(input(
                    "Enter number of AI players. (min 2, max 7)\n> "
                ))
            except ValueError:
                print("Must be an integer.")
                break

            if not 2 <= self.num_players <= 8:
                print("min 2, max 7")
                continue
            else:
                self.num_players += 1
                break

        self.player_id = random.randint(0, self.num_players - 1)

        for i in range(self.num_players):
            if i == self.player_id:
                self.players.append(Human(
                    "player", i, self.suits, self.values
                ))
            else:
                self.players.append(Bot(
                    "bot " + str(i), i, self.suits, self.values
                ))

        self.deck = Deck(self.suits, self.values)

    def get_player(self, player_index):
        return self.players[player_index]

    def get_type(self, type_index):
        return self.values[type_index]

    def deal(self):
        players_index = 0
        self.deck.shuffle()

        for i in range(self.deck.num_cards()):
            if players_index > self.num_players - 1:
                players_index = 0

            self.players[players_index].add_card_to_hand(self.deck.pop_card())
            players_index += 1

    def current_type_to_play(self, current_card_type_index):
        return self.get_type(current_card_type_index)

    def current_player_to_play(self, player_index_to_play):
        return self.get_player(player_index_to_play)

    def round(self):
        print("Current card type to play:")
        print(self.current_type_to_play(self.current_card_type_index))
        print("---")
        print("Player to place cards:")
        print(
            self.get_player(self.player_index_to_play).get_name()
        )


suits = ["Spade", "Club", "Heart", "Diamond"]
values = [
    "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen",
    "King"
]
