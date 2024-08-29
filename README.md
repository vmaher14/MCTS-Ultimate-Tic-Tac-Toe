# CMPM146 P2
Team Members: Victor Maher, Yash Malegaonkar

## Modifications
For the modified MCTS we thought that we were supposed to implement the modifications that were shown
in the slides rather than improve a heuristic. So we decided to implement partial expansion + UCT, and
that was the first modification that we did. In order to do this, we implemented the UCT calculation instead of UCB
and then for the partial expansion, we made it so instead of looping through every single action that was available, it would only 
do a subset of moves. For example if the list of available moves was 20 long, we would only do the first 10. After this partial expansion 
was implemented, the modified bot would lose, probably because it would not be taking in every possible action to rollout. 
After this, we realzied that the modification was supposed to be in the rollout stage, we added a heuristic instead of always doing a random 
rollout. We chose to loop through the possible moves, and modified the is_win helper function to check if that choosing that move would win the game. If it did, we would return that move. If none of the moves were winning moves, then we would just rollout as normal. 
By doing this, our modified MCTS bot would win against the vanilla bot almost every time. The higher the nodes the greater the win rate.
