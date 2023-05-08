# Programming assignment 4
We have a vehicle which needs to pass a known test track. You are given values $P_{req}(t)$ for each time $t=1,...,T$ which the vehicle's wheels needs to exert in order to successfully pass this test track.

The vehicle has a combustion engine, a motor/generator connected to a battery, and a friction break. Motor/generator can act either as a motor when it uses energy stored in the battery to power the wheels, or as a generator when it extracts the power from the wheels (regenerative breaking) or the engine to store it in the battery.

$P_{req}(t)$ is positive when the wheels need power, e.g. vehicle is ascending a hill or accelerating: power for the wheels needs to be provided by the combustion engine and/or the motor/generator which extracts the power stored in the battery. When $P_{req}(t)$ is negative (e.g. because vehicle is descending a hill), the power is extracted by the motor/generator which can store it in the battery and/or by the friction break.

Power is conserved, i.e., at each time t, we have
$$P_{req}(t) = P_{eng}(t) + P_{mg}(t) - P_{br}(t)$$
where $0 \leq P_{eng}(t) \leq Peng \textunderscore max$ is power produced by the combustion engine, $Pmg \textunderscore min \leq P_{mg}(t) \leq Pmg \textunderscore max$ is power produced by the motor/generator (can be also negative if motor/generator absorbs power to charge the battery) and $P_{br}(t) \geq 0$ is the power absorbed by the friction break. See data below for the definition of the constants.

For every $t=1,...,T+1$, the energy $E(t)$ in the battery has to be between 0 and Ebatt_max representing the power stored in empty and full battery respectively. Moreover, we need to take into account the charging and discharging of the battery: we have
$$E(t+1) = E(t) - P_{mg}(t) - \eta|P_{mg}(t)|$$ 
for $t=1,...,T$, see variable $\eta$ in the data. The term with coefficient $\eta$ represents the energy lost due to the inefficiency of the battery and motor/generator. We also require $E(T+1)=E(1)$ to make a fair comparison with a non-hybrid vehicle which has no battery.

The objective is to minimize the total fuel consumption of the vehicle over time, where the consumption at time $t$ is given by formula $P_{eng}(t) + \gamma (P_{eng}(t))^2$, i.e., a quadratic function. See data for the value of $\gamma$.

## Formulating the problem as a convex program
It is almost convex, just one set of constraints is problematic. \
**Hint**: Try to relax it, only one inequality is important, but provide an explanation (e.g. in the comments of your code) why your formulation is equivalent.

## Task 1: Solve your convex program with cvxpy library
Link to the library: https://www.cvxpy.org/. Implement it in function ``` car_with_battery() ```

## Task 2: comparison with a battery-less car
Change $Ebatt \textunderscore max$ to $0$ and solve your program again to see how does it affect the power consumption. Implement your code in function ``` car_without_battery() ```

**Hint**: Maybe you can prepare a single function which takes the value $Ebatt \textunderscore max$ as a parameter and solves your convex program based on this parameter. You can then call it from both functions (with/without battery) with the desired parameter value.

## Task 3: handle glitches
You may find out that although your program is equivalent, the solution found by the solver does not fulfill all the relaxed constraints with equality. This might happen during long periods of breaking when there is a lot of opportunities to charge the battery and sometimes the solver may decide to waste part of the power available to charge the battery (because it may charge it fully in the following time steps). There are two options how to proceed:

1. Postprocess the solution to get another solution with the same objective value where the relaxed constraints are preserved with equality. Such solution must exist since your program is equivalent to the original one. Hint: just move all the power from motor/generator to the battery and, if the battery is full, move it to the friction break.
2. Add a small term to the objective which will discourage such situation: for every $t=1,...,T$, you can add a term $\epsilon \cdot \max(0, -P_{mg}(t))$ for some small positive $\epsilon$ in order to discourage absorbing power by the motor/generator if it is not going to be used for charging the battery (because it is cheaper to absorb the power using the friction break)
In case you decide to modify the objective, make sure the power consumption achieved by your program is similar to the power consumption achieved by the program with the original objective (with your choice of $\epsilon$, they should not differ by more than $0.1$).
## Data
Template already contains a code which generates data. The array ```Preq``` contains power requirements in all time steps. Below the definition of ```Preq```, there are the bounds specifying the parameters of the engine, motor/generator, capacity of the battery, coefficient $\eta$ of the inefficiency of charging/discharging and coefficient $\gamma$ in the objective function.

## A note on precision
LP solvers which we used so far always provided a precise feasible solutions. This is not always the case with the solvers for convex optimization. If you want better precision, see "eps" parameters in Solver options. However, default values are good enough for the purpose of this assignment.
