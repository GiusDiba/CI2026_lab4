from klotski_models import Board, Problem
from upq import UPQ
from copy import deepcopy
def search(
    initial_state: Board
):
    frontier = UPQ()
    cur_board = initial_state
    state_costs = dict()
    state_costs[initial_state] = 0
    parent_state = dict()
    parent_state[cur_board] = None

    while cur_board is not None and not cur_board.isVictory():
        for action in cur_board.legal_moves:
            new_board = deepcopy(cur_board)
            new_board.movePiece(action[0], action[1])
            if new_board not in state_costs and new_board not in frontier:
                parent_state[new_board] = cur_board
                state_costs[new_board] = state_costs[cur_board] + 1 # Every state is 1 move away from the previous one
                frontier.push_update(new_board, state_costs[new_board] + new_board.getManhattanDistanceToExit())
            elif new_board in frontier and state_costs[new_board] > state_costs[cur_board] + 1:
                state_costs[new_board] = state_costs[cur_board] + 1
                parent_state[new_board] = cur_board
        
        if frontier:
            cur_board, _ = frontier.pop()
        else:
            cur_board = None
    
    path = []
    state = cur_board
    while state:
        path.append(state.printBoard())
        state = parent_state[state]

    path.reverse()
    return path


