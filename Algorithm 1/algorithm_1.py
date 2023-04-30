import pulp
from pulp import *

def ex1():
    retval = {}
    retval["x"] = None
    retval["y"] = None
    retval["obj"] = None
    retval["tight_constraints"] = [ None ]
    
    # Creating the variables
    x = LpVariable('x', lowBound=-10, upBound=None, cat='Continuous', e=None)
    y = LpVariable('y', lowBound=None, upBound=10, cat='Continuous', e=None)
    
    # Creating the LP problem
    lp_problem = LpProblem(name='minimization_problem', sense=LpMinimize)
    
    # Setting the function to be minimized
    lp_problem += 122*x + 143*y

    # Adding the constraints
    lp_problem += 3*x +  2*y <=  10
    lp_problem += 12*x + 14*y >= -12.5
    lp_problem += 2*x + 3*y >= 3
    lp_problem += 5*x -  6*y >= -100

    # Solving the LP problem
    lp_problem.solve(PULP_CBC_CMD(msg=False))

    # Finding the optimal solution
    retval["x"] = x.value()
    retval["y"] = y.value()
    
    # Finding the objective value
    retval["obj"] = lp_problem.objective.value()
    
    # Setting the tight constraints as an empty list
    retval["tight_constraints"] = []
    
    # Checking if the constraints are tight
    if x.value() ==  -10: retval["tight_constraints"].append(1)
    if y.value() ==  10: retval["tight_constraints"].append(2)
    for i in range(4):
        if value(lp_problem.constraints["_C" + str(i+1)]) == 0:
            retval["tight_constraints"].append(i+3)
       
    # Setting the tight constraints back to None if the list is still empty
    if retval["tight_constraints"] == []: 
        retval["tight_constraints"] = [ None ]
        
    # Return retval dictionary
    return retval


def ex2():
    retval = {}
    retval['x1'] = None
    retval['x2'] = None
    retval['x3'] = None
    retval['x4'] = None
    retval['x5'] = None
    retval['x6'] = None
    retval['obj'] = None
    
    # Creating the variables
    x_0 = LpVariable('x_0', lowBound=None, upBound=None, cat='Continuous', e=None)
    choices = LpVariable.dicts('choices', range(1,7), lowBound=0, upBound=1, cat='Continuous')

    # Creating the LP problem
    lp_problem = LpProblem(name='lp_problem', sense=LpMaximize)

    # Setting the function to be maximized
    lp_problem += x_0

    # Adding the constraints
    lp_problem += x_0 <= -2*choices[2] + choices[3] + choices[4] + choices[5] + choices[6]
    lp_problem += x_0 <= 2*choices[1] - 2*choices[3] + choices[4] + choices[5] + choices[6]
    lp_problem += x_0 <= -choices[1] + 2*choices[2] - 2*choices[4] + choices[5] + choices[6]
    lp_problem += x_0 <= -choices[1] - choices[2] + 2*choices[3] - 2*choices[5] + choices[6]
    lp_problem += x_0 <= -choices[1] - choices[2] - choices[3] + 2*choices[4] - 2*choices[6]
    lp_problem += x_0 <= -choices[1] - choices[2] - choices[3] - choices[4] + 2*choices[5]
    lp_problem += choices[1] + choices[2] + choices[3] + choices[4] + choices[5] + choices[6] == 1

    # Solving the LP problem
    lp_problem.solve(PULP_CBC_CMD(msg=False))
    
    # Finding the objective value
    retval['obj'] = lp_problem.objective.value()
    
    # Finding the optimal solution
    for i in range(1,7):
        retval['x' + str(i)] = choices[i].value()

    # return retval dictionary
    return retval


def ex3():
    retval = {}
    retval['obj'] = None
    retval['x1'] = None
    # there should be retval['xi'] for each company number i
    
    lp_problem = LpProblem("minimize_representatives", LpMinimize)
    
    representatives = LpVariable.dicts("representatives", range(69), lowBound=0, cat='Integer')

    # Reading the contracts information in the file
    f = open('hw1-03.txt')
    
    for line in f:
        
        # Converting the string information into integers
        i, j = map(int, line.split())
        
        # Adding the constraints (i.e. at least two representatives for each contract)
        lp_problem += representatives[i-1] + representatives[j-1] >= 2

    # Adding the function to be minimized (i.e. the number of total representatives)
    lp_problem += lpSum(representatives)

    lp_problem.solve(PULP_CBC_CMD(msg=False))

    # Finding the total number of representatives
    retval['obj'] = lp_problem.objective.value()
    
    # Finding the number of representatives for each company
    for i in range(69):
        retval['x' + str(i+1)] = representatives[i].value()

    # return retval dictionary
    return retval