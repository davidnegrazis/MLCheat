import sys
sys.path.append("../modules")
from game import Game  # noqa: E402


suits = ["Spade", "Club", "Heart", "Diamond"]
types = [
    "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen",
    "King"
]

g = Game(suits, types)
g.play_game()
