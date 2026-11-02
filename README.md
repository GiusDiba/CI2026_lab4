# CI2026_lab4

## _Klotski Problem_ approached using path search

---

### State

In this implementation, the state space is given by all possible board configurations, therefore states and nodes are represented by `Board` objects.

### Path

A path is a sequence of successive board configuartion ("linked" states differ only from a single move). All legal moves that may be performed in a given state are stored in the property `Board.legal_moves`.

### Algorithm

I implemented an A* algorithm: each move has a cost of 1, and the heuristic is the sum of the manhattan distance of the target piece from the exit and the amount of pieces in the way.

### Credits and AI use

I used the priority queue implementation from the professor. I have used Claude just to debug my code once it was finished (i had a bug in the manhattan distance calculation and in the hash code implementation).