from __future__ import annotations 

MOVES = {
    "left": (0, -1),
    "right": (0, 1),
    "up": (1, -1),
    "down": (1, 1)
}

# Coordinates of a piece always refer to its top-left corner
class Piece:
    tag: str
    width: int
    height: int
    row: int
    col: int

    available_moves: set

    def __init__(self, tag: str, width: int, height: int, row: int, col: int):
        self.tag = tag
        self.width = width
        self.height = height
        self.row = row
        self.col = col
        self.available_moves = set()

    def __str__(self) -> str:
        return f"piece {self.tag}: {self.width}x{self.height} in ({self.row}, {self.col})\n"

    def verticalStep(self, step: int) -> None:
        self.row += step

    def sideStep(self, step: int) -> None:
        self.col += step

    def addAvailableMove(self, action_tag: str) -> None:
        self.available_moves.add(action_tag)

    def removeAvailableMove(self, action_tag: str) -> None:
        self.available_moves.discard(action_tag)

# If there is a piece blocking the way, error_code is its tag. If the piece would be out of bounds, error_code is an empty_string
class IllegalMoveException(Exception):
    def __init__(self, message: str, error_code: str):
        self.message = message
        super().__init__(self.message)
        self.error_code = error_code

class Board:
    width: int
    height: int
    exit_loc: int # the full "door" spans from index exit_loc to exit_loc + pieces[target].width - 1; it's always at the bottom

    pieces = dict
    legal_moves: set
    board = list
    target: str
    win_position: tuple # (row, col), the coordinates that have to be reached by the top-left cell of the piece in order to win 

    def __init__(self, width: int, height: int, exit_loc: int):
        self.width = width
        self.height = height

        self.exit_loc = exit_loc
        self.legal_moves = set()

        self.pieces = {}
        self.board = [["." for _ in range(width)] for _ in range(height)]

    def __hash__(self):
        return hash(self.printBoard())

    def __eq__(self, other):
        return len(self.board) == len(other.board)

    def __lt__(self, other):
        return len(self.board) < len(other.board)

    def setTargetPiece(self, tag: str) -> tuple | None:
        far_left = self.pieces[tag].width + self.exit_loc - 1
        if len(self.pieces) == 0 or far_left >= self.width:
            return None
        self.target = tag
        self.win_position = (self.height - self.pieces[tag].height, self.exit_loc)
        door = tuple(range(self.exit_loc, far_left + 1))
        return door
    
    def isVictory(self) -> bool:
        v_row, v_col = self.win_position
        target_piece = self.pieces[self.target]
        return (target_piece.row == v_row) and (target_piece.col == v_col)

    def printBoard(self) -> str:
        brd = "=========\n"
        for idx in range(self.height):
            brd += self.stringifyRow(idx) + "\n"
        brd += "=========\n"
        return brd

    def stringifyRow(self, row_idx) -> str:
        row = ""
        for col_idx in range(self.width):
            row += f"{self.board[row_idx][col_idx]} "
        return row.strip()

    def insertPiece(self, piece: Piece) -> bool:
        col_boundary = piece.col + piece.width
        row_boundary = piece.row + piece.height

        # Check if the piece would be out of bounds
        if (col_boundary > self.width or row_boundary > self.height):
            return False

        # Check if the positions that would be occupied are free
        for p_row in range(piece.row, row_boundary):
            for p_col in range(piece.col, col_boundary):
                if (self.board[p_row][p_col] != "."):
                    return False
        
        # Actually insert piece
        for p_row in range(piece.row, row_boundary):
            for p_col in range(piece.col, col_boundary):
                self.board[p_row][p_col] = piece.tag
        self.pieces[piece.tag] = piece
        for p in self.pieces:
            self.updatePieceAvailableMoves(self.pieces[p])

    def getRangeAndCol(self, piece: Piece, increment: int) -> (int, int):
        if increment > 0:                      # If I go right, i have to check 1 column to the right
            col_to_check = piece.col + piece.width
        else:                                       # Else I want to check 1 column to the left
            col_to_check = piece.col - 1
        range_to_check = range(piece.row, piece.row + piece.height) # I want to check every element in the column
        # actual check
        if (col_to_check >= self.width ) or (col_to_check < 0):
            raise IllegalMoveException("Out of bounds", "")
        for idx in range_to_check:
            if self.board[idx][col_to_check] != ".":
                raise IllegalMoveException("A piece is blocking the way", self.board[idx][col_to_check])
        return range_to_check, col_to_check

    def getRangeAndRow(self, piece: Piece, increment: int) -> (int, int):
        if increment > 0:                      # If I go down, I have to check 1 row to the bottom
            row_to_check = piece.row + piece.height
        else:
            row_to_check = piece.row - 1
        range_to_check = range(piece.col, piece.col + piece.width)
        # actual check
        if (row_to_check >= self.height) or (row_to_check < 0):
            raise IllegalMoveException("Out of bounds", "")
        for idx in range_to_check:
            if self.board[row_to_check][idx] != ".":
                raise IllegalMoveException("A piece is blocking the way", self.board[row_to_check][idx])
        return range_to_check, row_to_check

    def updatePieceAvailableMoves(self, piece: Piece) -> None:
        global MOVES
        for action in MOVES:
            axis, increment = MOVES[action]
            try:
                if axis == 0:
                    self.getRangeAndCol(piece, increment)
                else:
                    self.getRangeAndRow(piece, increment)
                piece.addAvailableMove(action)
                self.legal_moves.add((piece.tag, action))
            except IllegalMoveException:
                piece.removeAvailableMove(action)
                self.legal_moves.discard((piece.tag, action))

    def movePiece(self, tag: str, direction: str) -> str:
        global MOVES
        piece = self.pieces[tag]    

        if direction not in piece.available_moves:
            return ""
        
        move_axis, move_increment = MOVES[direction]

        if move_axis == 0:                              # I'm changing column
            try:
                range_to_check, col_to_check = self.getRangeAndCol(piece, move_increment)
            except IllegalMoveException as e:
                return e.error_code
            # free furthest column and populate new one
            for idx in range_to_check:
                self.board[idx][col_to_check - move_increment * piece.width] = "."
                self.board[idx][col_to_check] = tag
            # update piece
            piece.sideStep(move_increment)
        else: 
            try:                                          # I'm changing row
                range_to_check, row_to_check = self.getRangeAndRow(piece, move_increment)
            except IllegalMoveException as e:
                return e.error_code
            # free furthest row and populate new one
            for idx in range_to_check:
                self.board[row_to_check - move_increment * piece.height][idx] = "."
                self.board[row_to_check][idx] = tag
            # update piece
            piece.verticalStep(move_increment)
        for p in self.pieces:
            self.updatePieceAvailableMoves(self.pieces[p])
        return tag

    def getManhattanDistanceToExit(self) -> int: # ideal number of moves neede if the board would be empty in order to reach the exit
        piece = self.pieces[self.target]
        return abs(piece.row - self.win_position[0] + piece.col - self.win_position[1])

class Problem():
    _id: str
    size: tuple
    _exit: tuple
    target: str

    board: Board

    def __init__(self, _id: str, width: int, height: int, _exit_idx: int):
        self._id = _id
        self.size = (width, height)
        self._exit = (1,)
        self.board = Board(width, height, _exit_idx)

    def getBoard(self) -> Board:
        return self.board

    def setTargetPiece(self, tag: str) -> None:
        res = self.board.setTargetPiece(tag)
        if res is None:
            return
        else:
            self.target = tag
            self._exit = res

    def __str__(self) -> str:
        problem = f"problem {self._id}\n"
        size = f"size {self.size[0]} {self.size[1]}\n"
        locs = ""
        for l in self._exit:
            locs += f"{l} "
        ex = f"exit bottom {locs}\n"
        tgt = f"target {self.target}\n"
        return problem + size + ex + tgt + self.board.printBoard()

    def isSolved(self) -> bool:
        return self.board.isVictory()

