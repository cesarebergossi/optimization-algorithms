import numpy as np
import cvxpy as cp


a=[0.5, -0.5, 0.2, -0.7, 0.6, -0.2, 0.7, -0.5, 0.8, -0.4]
l=[40, 20, 40, 40, 20, 40, 30, 40, 30, 60]
Preq=np.arange(a[0],a[0]*(l[0]+0.5),a[0])
for i in range(1, len(l)):
    Preq=np.r_[ Preq, np.arange(Preq[-1]+a[i],Preq[-1]+a[i]*(l[i]+0.5),a[i]) ]

T = sum(l)

Peng_max = 20.0
Pmg_min = -6.0
Pmg_max = 6.0
eta = 0.1
gamma = 0.1


def car_with_battery():
    Ebatt_max = 100.0
    
    retval = solve_convex_problem(Ebatt_max)
    
    return retval
    


def car_without_battery():
    Ebatt_max = 0
    
    retval = solve_convex_problem(Ebatt_max)
            
    return retval



def solve_convex_problem(Ebatt_max):
    
    # Small term epsilon
    epsilon = 2*1e-4

    # Define optimization variables
    Peng = cp.Variable(T)
    Pmg = cp.Variable(T)
    Pbr = cp.Variable(T)
    E = cp.Variable(T+1)

    # Define objective function (with penalization for negative motor/generator power, i.e. when the motor/generator absorbs
    # power to charge the battery)
    obj = cp.sum(Peng + gamma*cp.square(Peng) + epsilon*cp.maximum(0, -Pmg))
    
    # Define constraints
    constraints = []
    
    for t in range(T):
        constraints += [Peng[t] >= 0, Peng[t] <= Peng_max]
        constraints += [Pmg[t] >= Pmg_min, Pmg[t] <= Pmg_max]
        constraints += [Pbr[t] >= 0]
        constraints += [E[t] >= 0, E[t] <= Ebatt_max]
        
        # Conservation of power
        constraints += [Preq[t] == Peng[t] + Pmg[t] - Pbr[t]]
        
        # The only constraint which is not convex is the one containing the absolute value (i.e. the equality related to the
        # battery dynamics), as it describes a non-convex region: to address this problem, we introduce a relaxation.
        # First, we split the equality into two equivalent inequalities; then, we consider the less-or-equal inequality 
        # (E[t+1] <= E[t] - Pmg[t] - eta*abs(Pmg[t])) which is the important one and we exploit the property of the absolute
        # value: we move it to the LHS and then remove the absolute value by splitting it into two other inequalities.
        # Note: the greater-or-equal inequality (E[t+1] >= E[t] - Pmg[t] - eta*abs(Pmg[t])) can be omitted, since the solver
        # will already try to increase the battery charge at every iteration (to decrease the fuel consumption). It is the 
        # less-or-equal inequality which is not trivial, and therefore needs to be expressed.
        
        constraints += [eta*Pmg[t] <= E[t] - Pmg[t] - E[t+1]]
        constraints += [eta*Pmg[t] >= -E[t] + Pmg[t] + E[t+1]]
        
    constraints += [E[T] == E[0]]

    # Solve optimization problem
    prob = cp.Problem(cp.Minimize(obj), constraints)
    prob.solve(solver=cp.ECOS)

    # Extract solution
    Pbr_sol = Pbr.value
    Peng_sol = Peng.value
    Pmg_sol = Pmg.value
    E_sol = E.value

    # Convert solution arrays to lists
    Pbr_sol = [float(x) for x in Pbr_sol]
    Peng_sol = [float(x) for x in Peng_sol]
    Pmg_sol = [float(x) for x in Pmg_sol]
    E_sol = [float(x) for x in E_sol]

    # Store results in dictionary
    retval = {}
    retval['Peng'] = Peng_sol
    retval['Pmg'] = Pmg_sol
    retval['Pbr'] = Pbr_sol
    retval['E'] = E_sol
    
    return retval