import random
import itertools
from colours import bcolours


class Card:
    def __init__(self, suit, _type, value):
        self.suit = suit
        self.type = _type
        self.value = value

    def __str__(self):
        return self.type + " of " + self.suit + "s"

    def __lt__(self, other):
        return self.value < other.value

    def get_type(self):
        return self.type


class Cards:
    def __init__(self):
        self.cards = []

    def sort_cards(self):
        self.cards.sort()

    def add_card(self, Card):
        self.cards.append(Card)

    def add_cards(self, Cards):
        for i in range(0, Cards.num_cards()):
            self.add_card(Cards.get_card(i))

    def clear(self):
        self.cards.clear()

    def get_card(self, i):
        return self.cards[i]

    def get_combos(self, n=-1, remove_empties=False):
        if n == -1:
            n = self.num_cards()

        indices = range(0, self.num_cards())
        combos = []

        for L in range(0, n):
            for subset in itertools.combinations(indices, L):
                combos.append(list(subset))

        if remove_empties:
            combos.pop(0)

        return combos

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
                    string += (
                        bcolours().BOLD + "[" + str(i) + "] " + bcolours().ENDC
                    )

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


class Deck(Cards):
    def __init__(self, suits, types):
        Cards.__init__(self)
        self.suits = suits
        self.types = types

        for i in range(len(self.types)):
            for suit in self.suits:
                self.add_card(Card(suit, self.types[i], i))
