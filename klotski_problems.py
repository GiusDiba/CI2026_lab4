from klotski_models import Problem, Piece

def initializeProblem(problem: Problem, pieces: list, target: str) -> None:
    for p in pieces:
        problem.board.insertPiece(p)
    problem.setTargetPiece(target)

# problem p01
# size 3 3
# exit bottom 1
# target A
# =========
# A 5 1
# 6 4 2
# 3 . .
# =========
KP01 = Problem("p01", 3, 3, 1)
pieces = [
    Piece("A", 1, 1, 0, 0),
    Piece("1", 1, 1, 0, 2),
    Piece("2", 1, 1, 1, 2),
    Piece("3", 1, 1, 2, 0),
    Piece("4", 1, 1, 1, 1),
    Piece("5", 1, 1, 0, 1),
    Piece("6", 1, 1, 1, 0),
]
initializeProblem(KP01, pieces, "A")

# problem p02
# size 4 4
# exit bottom 1 2
# target A
# =========
#  A  A  4  7
#  A  A  6  8
#  1  5  .  3
# 10  .  9  2
# =========
KP02 = Problem("p02", 4, 4, 1)
pieces = [
    Piece("A", 2, 2, 0, 0),
    Piece("1", 1, 1, 2, 0),
    Piece("2", 1, 1, 3, 3),
    Piece("3", 1, 1, 2, 3),
    Piece("4", 1, 1, 0, 2),
    Piece("5", 1, 1, 2, 1),
    Piece("6", 1, 1, 1, 2),
    Piece("7", 1, 1, 0, 3),
    Piece("8", 1, 1, 1, 3),
    Piece("9", 1, 1, 3, 2),
    Piece("10", 1, 1, 3, 0),
]
initializeProblem(KP02, pieces, "A")

# problem p03
# size 4 4
# exit bottom 1 2
# target A
# =========
# A A 2 3
# A A 5 .
# B 1 C C
# B . 6 4
# =========
KP03 = Problem("p03", 4, 4, 1)
pieces = [
    Piece("A", 2, 2, 0, 0),
    Piece("1", 1, 1, 2, 1),
    Piece("2", 1, 1, 0, 2),
    Piece("3", 1, 1, 0, 3),
    Piece("4", 1, 1, 3, 3),
    Piece("5", 1, 1, 1, 2),
    Piece("6", 1, 1, 3, 2),
    Piece("B", 1, 2, 2, 0),
    Piece("C", 2, 1, 2, 2),

]
initializeProblem(KP03, pieces, "A")

# problem p04
# size 5 4
# exit bottom 1 2
# target A
# =========
# B A A C
# B A A C
# D F F E
# D 2 3 E
# 1 . . 4
# =========
KP04 = Problem("p04", 4, 5, 1)
pieces = [
    Piece("A", 2, 2, 0, 1),
    Piece("B", 1, 2, 0, 0),
    Piece("C", 1, 2, 0, 3),
    Piece("D", 1, 2, 2, 0),
    Piece("E", 1, 2, 2, 3),
    Piece("F", 2, 1, 2, 1),
    Piece("1", 1, 1, 4, 0),
    Piece("2", 1, 1, 3, 1),
    Piece("3", 1, 1, 3, 2),
    Piece("4", 1, 1, 4, 3),

]
initializeProblem(KP04, pieces, "A")

# problem p05
# size 5 4
# exit bottom 1 2
# target A
# =========
# 4 1 3 B
# A A C B
# A A C D
# . E E D
# . 2 F F
# =========
KP05 = Problem("p05", 4, 5, 1)
pieces = [
    Piece("A", 2, 2, 1, 0),
    Piece("B", 1, 2, 0, 3),
    Piece("C", 1, 2, 1, 2),
    Piece("D", 1, 2, 2, 3),
    Piece("E", 2, 1, 3, 1),
    Piece("F", 2, 1, 4, 2),
    Piece("1", 1, 1, 0, 1),
    Piece("2", 1, 1, 4, 1),
    Piece("3", 1, 1, 0, 2),
    Piece("4", 1, 1, 0, 0),

]
initializeProblem(KP05, pieces, "A")

# problem p06
# size 4 4
# exit bottom 1 2
# target A
# =========
# B 2 . 3
# B 1 A A
# 4 . A A
# C C D D
# =========
KP06 = Problem("p06", 4, 4, 1)
pieces = [
    Piece("A", 2, 2, 1, 2),
    Piece("B", 1, 2, 0, 0),
    Piece("C", 2, 1, 3, 0),
    Piece("D", 2, 1, 3, 2),
    Piece("1", 1, 1, 1, 1),
    Piece("2", 1, 1, 0, 1),
    Piece("3", 1, 1, 0, 3),
    Piece("4", 1, 1, 2, 0),

]
initializeProblem(KP06, pieces, "A")
