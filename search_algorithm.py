from utils.klotski_models import Board, Problem
from utils.upq import UPQ
from copy import deepcopy
def search(
    initial_state: Board
) -> dict:
    frontier = UPQ()
    cur_board = initial_state
    state_costs = dict()
    state_costs[initial_state] = 0
    parent_state = dict()
    parent_state[cur_board] = None
    previous_move = dict()
    previous_move[cur_board] = None
    moves = []

    while cur_board is not None and not cur_board.isVictory():
        #print(f"Considering state:\n{cur_board.printBoard()}")
        for action in cur_board.legal_moves:
            new_board = deepcopy(cur_board)
            new_board.movePiece(action[0], action[1])
            if new_board not in state_costs and new_board not in frontier:
                parent_state[new_board] = cur_board
                previous_move[new_board] = action
                state_costs[new_board] = state_costs[cur_board] + 1 # Every state is 1 move away from the previous one
                frontier.push_update(new_board, state_costs[new_board] + new_board.getManhattanDistanceToExit() + new_board.countPiecesInTheWay())
            elif new_board in frontier and state_costs[new_board] > state_costs[cur_board] + 1:
                state_costs[new_board] = state_costs[cur_board] + 1
                parent_state[new_board] = cur_board
                previous_move[new_board] = action
                frontier.push_update(new_board, state_costs[new_board] + new_board.getManhattanDistanceToExit() + new_board.countPiecesInTheWay())        
        if frontier:
            cur_board, _ = frontier.pop()
        else:
            cur_board = None
    
    if cur_board is None:
        solution = {
            "solved": False,
            "visited_states": len(state_costs)
        }
    else:
        states_path = []
        moves_path = []
        state = cur_board
        while state:
            states_path.append(state.printBoard())
            moves_path.append(previous_move[state])
            state = parent_state[state]

        states_path.reverse()
        moves_path.pop()
        moves_path.reverse()

        solution = {
            "solved": True,
            "path": states_path,
            "moves": moves_path,
            "visited_states": len(state_costs) 
        }
    return solution


