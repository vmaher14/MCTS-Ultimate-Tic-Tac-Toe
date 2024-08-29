
from mcts_node import MCTSNode
from p2_t3 import Board
from random import choice
from math import sqrt, log

num_nodes = 500
explore_faction = 2.

def traverse_nodes(node: MCTSNode, board: Board, state, bot_identity: int):
    """ Traverses the tree until the end criterion are met.
    e.g. find the best expandable node (node with untried action) if it exist,
    or else a terminal node

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 1 or 2

    Returns:
        node: A node from which the next stage of the search can proceed.
        state: The state associated with that node

    """

    best_node = None
    highest_ucb = float('-inf')

    # Iterate through child nodes to find the one with the highest UCB
    for _, child in node.child_nodes.items():
        current_ucb = ucb(child, False)
        if current_ucb > highest_ucb:
            highest_ucb = current_ucb
            best_node = child

    # If no child node is found, the original node remains the best
    if not best_node:
        best_node = node

    # Update the state if the best node has a parent action
    next_state = board.next_state(state, best_node.parent_action) if best_node.parent_action else state

    return best_node, next_state

def expand_leaf(node: MCTSNode, board: Board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node (if it is non-terminal).

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:
        node: The added child node
        state: The state associated with that node

    """
    if node.untried_actions:
        act = node.untried_actions.pop()

        if board.is_legal(state, act):
            node2 = MCTSNode(parent=node, parent_action=act, action_list=board.legal_actions(board.next_state(state, act)))
            node.child_nodes[act] = node2
            state = board.next_state(state, act)
            return node2, state
        
    return node, state

def rollout(board: Board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.
    
    Returns:
        state: The terminal game state

    """
    while not board.is_ended(state):
        moves = board.legal_actions(state)
        nxtmove = choice(moves)
        state = board.next_state(state, nxtmove)
    return state

def backpropagate(node: MCTSNode|None, won: bool):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    if not node:
        return None
    else:
        node.visits += 1
        if won:
            node.wins += 1
    backpropagate(node.parent, won)

def ucb(node: MCTSNode, is_opponent: bool):
    """ Calcualtes the UCB value for the given node from the perspective of the bot

    Args:
        node:   A node.
        is_opponent: A boolean indicating whether or not the last action was performed by the MCTS bot
    Returns:
        The value of the UCB function for the given node
    """
    if node.visits == 0:
        return 0
    
    if is_opponent:
        exploit = node.wins / node.visits
        explore = explore_faction * sqrt(log(node.parent.visits, 2) / node.visits)
    else:
        exploit = node.wins / node.visits
        explore = explore_faction * sqrt(log(node.visits, 2) / node.visits)

    return exploit + explore



def get_best_action(root_node: MCTSNode):
    """ Selects the best action from the root node in the MCTS tree

    Args:
        root_node:   The root node
    Returns:
        action: The best action from the root node
    
    """
    best = float("-inf")
    best_act = None
    for child in root_node.child_nodes:
        cur = root_node.child_nodes[child]
        rate = cur.wins / cur.visits
        if rate >= best:
            best = rate
            best_act = child
    return best_act

def is_win(board: Board, state, identity_of_bot: int):
    # checks if state is a win state for identity_of_bot
    outcome = board.points_values(state)
    assert outcome is not None, "is_win was called on a non-terminal state"
    return outcome[identity_of_bot] == 1

def think(board: Board, current_state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        current_state:  The current state of the game.

    Returns:    The action to be taken from the current state

    """
    bot_identity = board.current_player(current_state) # 1 or 2
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(current_state))

    for _ in range(num_nodes):
        state = current_state
        node = root_node

        # Do MCTS - This is all you!
        # ...

        # Selection - Navigating the Tree
        while node.child_nodes and not node.untried_actions:
            node.visits += 1
            node, state = traverse_nodes(node, board, state, bot_identity)

        # Expansion
        if node.untried_actions:
            node, state = expand_leaf(node, board, state)
            node.visits += 1
            node, state = traverse_nodes(node, board, state, bot_identity)

        # Simulation/Playout/Rollout
        state = rollout(board, state)
        won = is_win(board, state, bot_identity)
        backpropagate(node, won)

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    best_action = get_best_action(root_node)
    
    print(f"Action chosen: {best_action}")
    return best_action

