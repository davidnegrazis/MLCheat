# MLCheat

Currently, you can mess around with playing against the AI or let them play against themselves. The AI is pretty unintelligent at the moment, though.

I'm in the midst of researching and implementing ML so the bots can learn from the games they play. This will be done via **reinforcement learning**.

## To play
Make sure you have Python 3.x installed. To play, head into `scripts/` and run
```
python3.x cheat.py
```

In `modules/game.py`, you can see that the `Game` object initialization accepts the following params:
```
self, suits, types, Simulate=False, show_outputs=True, num_players=0, min_p=3, max_p=8,
```
The `suits` and `types` are as expected (see `scripts/cheat.py`). They can be changed (e.g. more cards can be added). To simulate the games, set `Simulate` to true when creating the game. Here's an example you can try:
```
g = Game(suits, types, true, true, 5)
```
by editing line 12 of `scripts/cheat.py`. This will simulate a game with five bots.

## Example gameplay
<img src='https://i.imgur.com/58L3cGj.png'>
