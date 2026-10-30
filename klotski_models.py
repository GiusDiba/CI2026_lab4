from __future__ import annotations 

MOVES = {
    "left": (0, -1),
    "right": (0, 1),
    "up": (1, -1),
    "down": (1, 1)
}

class Move:
    tag: str
    action: tuple

    def __init__(self, tag: str, action: tuple):
        self.tag = tag
        self.action = action 

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

class IllegalMoveException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class Board:
    width: int
    height: int
    exit_loc: tuple

    pieces = dict
    board = list

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        loc = (width - 1) // 2
        self.exit_loc = (loc, loc + 1)

        self.pieces = {}
        self.board = [["." for _ in range(width)] for _ in range(height)]

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
        self.updatePieceAvailableMoves(self.pieces[piece.tag])

    def getRangeAndCol(self, piece: Piece, increment: int) -> (int, int):
        if increment > 0:                      # If I go right, i have to check 1 column to the right
            col_to_check = piece.col + piece.width
        else:                                       # Else I want to check 1 column to the left
            col_to_check = piece.col - 1
        range_to_check = range(piece.row, piece.row + piece.height) # I want to check every element in the column
        # actual check
        if (col_to_check >= self.width ) or (col_to_check < 0):
            raise IllegalMoveException("Out of bounds")
        for idx in range_to_check:
            if self.board[idx][col_to_check] != ".":
                raise IllegalMoveException("No space available")
        return range_to_check, col_to_check

    def getRangeAndRow(self, piece: Piece, increment: int) -> (int, int):
        if increment > 0:                      # If I go down, I have to check 1 row to the bottom
            row_to_check = piece.row + piece.height
        else:
            row_to_check = piece.row - 1
        range_to_check = range(piece.col, piece.col + piece.width)
        # actual check
        if (row_to_check >= self.height) or (row_to_check < 0):
            raise IllegalMoveException("Out of bounds")
        for idx in range_to_check:
            if self.board[row_to_check][idx] != ".":
                raise IllegalMoveException("No space available")
        return range_to_check, row_to_check

    def updatePieceAvailableMoves(self, piece: Piece) -> None:
        global MOVES
        for action in MOVES:
            axis, increment = MOVES[action]
            print(f"Checking move {axis}, {increment}")
            try:
                if axis == 0:
                    self.getRangeAndCol(piece, increment)
                else:
                    self.getRangeAndRow(piece, increment)
                piece.addAvailableMove(action)
            except IllegalMoveException:
                piece.removeAvailableMove(action)


    def movePiece(self, tag: str, direction: str) -> bool:
        global MOVES
        piece = self.pieces[tag]    

        if direction not in piece.available_moves:
            return False
        
        move_axis, move_increment = MOVES[direction]

        if move_axis == 0:                              # I'm changing column
            try:
                range_to_check, col_to_check = self.getRangeAndCol(piece, move_increment)
            except IllegalMoveException:
                return False
            # free furthest column and populate new one
            for idx in range_to_check:
                self.board[idx][col_to_check - move_increment * piece.width] = "."
                self.board[idx][col_to_check] = tag
            # update piece
            piece.sideStep(move_increment)
        else: 
            try:                                          # I'm changing row
                range_to_check, row_to_check = self.getRangeAndRow(piece, move_increment)
            except IllegalMoveException:
                return False
            # free furthest row and populate new one
            for idx in range_to_check:
                self.board[row_to_check - move_increment * piece.height][idx] = "."
                self.board[row_to_check][idx] = tag
            # update piece
            piece.verticalStep(move_increment)

        self.updatePieceAvailableMoves(piece)
        return True


        # Check if the piece would be out of bounds
        
        



