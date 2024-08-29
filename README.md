# MCTS Ultimate Tic Tac Toe
A bot that uses the Monte Carlo Tree Search algorithm to play ultimate tic-tac-toe.

## Modifications
The modified version used partial expansion + Upper Confidence bounds applied to Trees (UCT) + a heuristic. With this, instead of looping through every action that was available, the algorithm would only do a subset of moves. Then instead of always doing a random rollout, the heuristic would loop through the possible moves and would check for if there was a winning move available. If there was, it would immediate pick it, otherwise it would perform the rollout as normal. With the modification, the MCTS bot would win against the vanilla bot over 95% of the time, resulting in a major improvement on the vanilla algorithm. 

## How to run

### For Manual play
`python3 p2_play.py <Arg1> <Arg2>`  
Args `random_bot, rollout_bot, mcts_vanilla, mcts_modified`


### For Simulation
`python3 p2_sim.py <Arg1> <Arg2>`  
Args `random_bot, rollout_bot, mcts_vanilla, mcts_modified`

### Modifiable Values
`rounds = 10` in `p2_sim.py`  
`nodes = 100` in `mcts_modified.py, mcts_vanilla.py`  
`explore_factor = 2` in `mcts_modified.py`  
`sub_set_size = 10` in `mcts_modified.py`  
