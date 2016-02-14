Author: Jacob Drilling

My program uses python3.
To run it on campus machines, use the command:
    python3 puzzle.py <PuzzlePath> [Algorithm]

The PuzzlePath parameter is mandatory and is the realive path to the puzzle file.
The Algorithm parameter is optional. If no option is given, it will default to
Greedy Best First Graph Search.

The options for the Algorithm paramater are currently:
    "BFTS"    - The algo for assignment 1, Breadth First Tree Search
    "DFTS" - The algo for assignment 2, Iterative Deepening - Depth First Tree Search 
    "GBFGS" - Algo for assignment 3, Greedy Best First *Graph* Search
    "GBFTS" - Algo for assignment 3 Bonus, Greedy Best First *Tree* Search

Sometimes, my program will output debbugging information regarding the algorithm's 
current depth in the search tree and the original state of the game. Just ignore this.

The last piece of information the program outputs is the path to the 
solution file.

Solutions are output to a file path that is similar to the input file path, 
but output files will end in "_sol.txt\.


## BONUS
I did attempt the bonus for this assignment. My bonus solutions are in the 
bonusSolutions/ directory. The algorithm for these can be run by using the
command:
  python3 puzzle.py <PuzzlePath> gbfts
