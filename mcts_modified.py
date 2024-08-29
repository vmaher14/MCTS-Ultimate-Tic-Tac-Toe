from mcts_node import MCTSNode
from p2_t3 import Board
from random import choice
from math import sqrt, log
from time import time

num_nodes = 100
explore_factor = 2
sub_set_size = 10

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
    while not board.is_ended(state):
        if node.untried_actions != []:
            return node, state
        else:
            best_action = None
            best_uct_value = float('-inf')
            for action, child_node in node.child_nodes.items():
                uct_value = uct(child_node, True)
                if uct_value > best_uct_value:
                    best_uct_value = uct_value
                    best_action = action
            state = board.next_state(state, best_action)
            node = node.child_nodes[best_action]
    return node, state

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
    added_nodes = []
    best_val = float('-inf')
    best_node = None
    if not node.untried_actions:
        return node, state
    
    for i in range(min(len(node.untried_actions), sub_set_size)):
        action = choice(node.untried_actions)
        node.untried_actions.remove(action)
        new_state = board.next_state(state, action)
        new_node = MCTSNode(parent=node, parent_action=action, action_list=board.legal_actions(new_state))
        node.child_nodes[action] = new_node
        added_nodes.append(new_node)

    for i in added_nodes:
        uct_val = uct(i, True)
        if uct_val > best_val:
            best_val = uct_val
            best_node = i
    next_state = board.next_state(state, best_node.parent_action)
    return best_node, next_state

def rollout(board: Board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.
    
    Returns:
        state: The terminal game state

    """
    while not board.is_ended(state):
        for i in board.legal_actions(state):
            if is_win(board, board.next_state(state, i), board.current_player(state)):
                return board.next_state(state, i)
        rollout_move = choice(board.legal_actions(state))
        state = board.next_state(state, rollout_move)

    return state

def backpropagate(node: MCTSNode|None, won: bool):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    while node is not None:
        node.visits += 1
        if won:
            node.wins += 1
        node = node.parent
    
def ucb(node: MCTSNode, is_opponent: bool):
    """ Calcualtes the UCB value for the given node from the perspective of the bot

    Args:
        node:   A node.
        is_opponent: A boolean indicating whether or not the last action was performed by the MCTS bot
    Returns:
        The value of the UCB function for the given node
    nvm we really need xj = average reward of child node j
    nj which is number of times j was played
    n is number of overall plays so far
    
    """
    if node.visits == 0:
        return float('inf')

    win_rate = node.wins / node.visits
    if is_opponent:
        win_rate = 1 - win_rate
    exploration_term = sqrt((2 * log(node.parent.visits)) / node.visits)
    return win_rate + exploration_term * explore_factor

def uct(node: MCTSNode, is_opponent: bool):
    if node.visits == 0:
        return float('inf')
    win_rate = node.wins / node.visits
    if is_opponent:
        win_rate = 1 - win_rate 
    exploration_term = sqrt((2 * log(node.parent.visits)) / node.visits)
    return win_rate + exploration_term + explore_factor * sqrt(log(node.parent.visits) / node.visits)

def get_best_action(root_node: MCTSNode):
    """ Selects the best action from the root node in the MCTS tree

    Args:
        root_node:   The root node
    Returns:
        action: The best action from the root node
    
    """
    best_action = None
    best_ucb_value = float('-inf')
    for action, child_node in root_node.child_nodes.items():
        ucb_value = uct(child_node, False)
        if ucb_value > best_ucb_value:
            best_ucb_value = ucb_value
            best_action = action

    return best_action

def is_win(board: Board, state, identity_of_bot: int):
    # checks if state is a win state for identity_of_bot
    outcome = board.points_values(state)
    if outcome is not None:
        return outcome[identity_of_bot] == 1
    else:
        return False

def think(board: Board, current_state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        current_state:  The current state of the game.

    Returns:    The action to be taken from the current state

    """
    bot_identity = board.current_player(current_state) # 1 or 2
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(current_state))

    # Time constrain for experiment 3
    # start_time = time.time()
    # while (time.time() - start_time) < 3.0:
    for _ in range(num_nodes):
        state = current_state
        node = root_node

        node, state = traverse_nodes(root_node, board, current_state, bot_identity)
        if node.untried_actions:
            node, state = expand_leaf(node, board, state)
        rollout_result = rollout(board, state)
        won = is_win(board, rollout_result, bot_identity)

        backpropagate(node, won)

    best_action = get_best_action(root_node)
    print(f"Action chosen: {best_action}")
    return best_action