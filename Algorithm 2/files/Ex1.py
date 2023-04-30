import pulp
from pulp import *

x = LpVariable('x', lowBound=-10, upBound=None, cat='Continuous', e=None)
y = LpVariable('y', lowBound=None, upBound=10, cat='Continuous', e=None)

lp_problem = LpProblem(name='LP Problem', sense=LpMinimize)

lp_problem += 122*x + 143*y

lp_problem += 3*x +  2*y <=  10
lp_problem += 12*x + 14*y >= -12.5
lp_problem += 2*x + 3*y >= 3
lp_problem += 5*x -  6*y >= -100

lp_problem.solve(PULP_CBC_CMD(msg=False))

print("Objective value:", lp_problem.objective.value())

print("Optimal solution: x =", x.value(), ", ", "y =", y.value())

print("Tight constraints:")
if x.value() ==  -10: print(1)
if y.value() ==  10: print(2)
if 3*x.value() +  2*y.value() ==  10: print(3)
if 12*x.value() +  14*y.value() ==  -12.5: print(4)
if 2*x.value() +  3*y.value() ==  3: print(5)
if 5*x.value() -  6*y.value() ==  -100: print(6)