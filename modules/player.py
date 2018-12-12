import random
from cards import Hand
from colours import bcolours


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


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

    def give_cards(self, Cards):
        self.hand.add_cards(Cards)

    def num_cards(self):
        return self.hand.num_cards()

    def play(self, current_type_index, max_size=4):
        pass

    # returns bool for decision
    def call_cheat(self, current_type_index, pool_size):
        pass


class Human(Player):
    def __init__(self, name, id, suits, types):
        Player.__init__(self, name, id, suits, types)

    def play(self, current_type_index, max_size=4):
        cmd = ""
        queue = []

        while True:
            print("--- Available cards to play ---")
            self.hand.show_cards(True, queue)
            print("\n--- My selection ---")
            self.hand.show_cards(False, None, queue)
            print("--------------------")

            cmd = input("Enter a command or type ? for help\n> ")

            if (cmd == "?"):
                print("")
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
            special_cmds = ["clear", "undo", "done", "sort"]
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
                    if special == "clear":
                        queue = []
                    elif special == "done":
                        if len(queue) == 0:
                            print("You haven't entered anything to play yet")
                        else:
                            return queue
                    elif special == "undo":
                        if len(queue) > 0:
                            queue.pop()
                        else:
                            print("Nothing to undo")
                    elif special == "sort":
                        self.hand.sort_cards()

                    valid_cmd = False
                    break

            if not valid_cmd:
                continue

            if len(cmd) + len(queue) > max_size:
                print(
                    "You can't play more than " + str(max_size) +
                    " cards at a time"
                )

            cmd = [int(x) for x in cmd]
            queue.extend(cmd)

    def show_instructions(self):
        print(bcolours().OKGREEN, end="")
        print("--- Commands ---")
        print("To select a card, enter the number you see before it")
        print(
            "To enter multiple cards at once, separate card numbers with a " +
            "comma"
        )
        print("~~~")
        print("To sort cards, enter 'sort'")
        print("~~~")
        print("To undo most recent card placement, enter 'undo'")
        print("~~~")
        print("To clear selection, enter 'clear'")
        print("----------------")
        print(bcolours().ENDC, end="")

    def call_cheat(self, current_type_index, pool_size=None):
        inp = ""
        while(True):
            inp = input("Call cheat? (y / n / h / s / ?) > ")
            if inp == "y":
                return True
            elif inp == "n":
                return False
            elif inp == "h":
                self.hand.show_cards()
            elif inp == "s":
                self.hand.sort_cards()
                self.hand.show_cards()
            elif inp == "?":
                print("y: call cheat\nn: continue\nh: see hand\ns: sort hand")
                print(
                    "(calling cheat accuses the player of placing at least " +
                    "one card that doesn't match the current type)"
                )
            else:
                print("Options: y / n / h / s / ?")


class Bot(Player):
    def __init__(self, name, id, suits, types):
        Player.__init__(self, name, id, suits, types)

    def play(self, current_type_index, max_size=4):
        return random.choice(self.hand.get_combos(max_size, True))

    def call_cheat(self, current_type_index, pool_size):
        return random.choice([True, False])
