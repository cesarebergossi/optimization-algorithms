# Programming Assignment 1
Use the PuLP library https://pypi.org/project/PuLP/ to solve the following problems. Documentation to PuLP can be found here: https://coin-or.github.io/pulp/main/index.html
## A few hints
To surpress the messages from the solver, you can use GLPK(msg = 0) (if you use GLPK) or PULP_CBC_CMD(msg=False) (if you use CBC) or a similar option for other solvers as a solver parameter of solve() method. You can use function value() to evaluate any expression involving the variables in the optimal solution. If you need many variables, it might be good to introduce them using an array of their names using dicts() method and use the returned dictionary to access them.
## Part 1
Solve the following program:
```text
       min 122x + 143y
subject to:
         x ≥ -10
         y ≤  10
  3x +  2y ≤  10
 12x + 14y ≥ -12.5
  2x +  3y ≥   3
  5x -  6y ≥ -100
```
Required output example:
```text
Optimal solution: x = 0.1 y = -2.3
Objective value: 100.1214
Tight constraints:
1
2
4
```
So, your program should find the optimal solution, determine its objective value, and identify the tight constraints.

## Part 2
Find an optimal mixed strategy of the following game: \
Both players choose independently a single integer from 1 to 6. Then, the numbers are compared: 
-	If they are equal, there is a draw 
-	If they differ by 1, the player who played the smaller number gets 2EUR from the other player
-	If they differ by ≥2, the player who played the larger number gets 1EUR from the other player 

Note that the game is symmetric and the same strategy is optimal for both players. \
\
Required output example:
```text
x1: 0.2 x2: 0.1 x3: 0.2 x4: 0.1 x5: 0.2 x6: 0.2
```

## Part 3
On some imaginary island, there are 69 companies and there are bilateral contracts between them. The monarch of the island would like to inspect validity of each of these contracts during a single large event. The monarch requires two representatives to represent each contract relationship (they can be both from the same party of the contract or each from a different one). This is of course satisfied by each company sending a single representative, which would require involvement of 69 representatives in total. However, the companies want to find a solution which minimizes the total number of representatives who need to attend the event. \
\
Input file hw1-03.txt contains information about the contracts. Each line corresponds to a single contract and contains identifiers (1-69) of both involved parties separated by a space. \
\
Example output:
```text
representatives from company 1: 1.0
representatives from company 2: 2.0
representatives from company 3: 1.0
...
representatives from company 69: 1.0
Total number of representatives involved: 58
```
**Important**: It is not possible to send an arbitrary fraction of a representative. However, it is enough to solve the LP relaxation since it already gives an integral solution. Reasons for this will be explained later in the class.

