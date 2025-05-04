# Optimization Algorithms

This repository contains a collection of algorithmic implementations developed as part of the **Advanced Programming and Optimization Algorithms** course during the second year of my BSc. Each assignment tackles a different optimization or scheduling problem and includes a Python-based solution.

## Repository Structure

Each assignment includes:
- The Python implementation
- A `description.md` file detailing the problem and the method
- The input file used for testing (where applicable)


## Assignments Included

### **Assignment 1 – Maximal Independent Set**
- **Goal:** Find the largest independent set in a graph.
- **Input:** Adjacency list (`hw1-03.txt`)
- **Approach:** Greedy selection with local improvements.
- **Output:** Set of non-adjacent nodes forming a maximal independent set.


### **Assignment 2 – Pastry Scheduling**
- **Goal:** Schedule baking tasks to minimize delivery delays.
- **Input:** Task durations and deadlines (`bakery.txt`).
- **Approach:** Greedy scheduling with a visual representation of criticality.
- **Output:** Optimized baking schedule and annotated timeline (`visualization.png`).


### **Assignment 3 – Custom Optimization Task**
- **Goal:** Solve a task-specific combinatorial optimization problem.
- **Approach:** Heuristic algorithm tailored to the problem structure.
- **Output:** Optimized configuration (details in `description.md`).


### **Assignment 4 – Graph Path Traversal with Cost Minimization**
- **Goal:** Traverse a graph starting and ending at the same node with the lowest cost, visiting at least once all edge types (red and blue).
- **Approach:** Construct and solve the problem using depth-first path generation, edge marking, and pruning.
- **Output:** A valid round-trip path and the associated cost.

## File Tree
```bash
assignment_1/
├── algorithm_1.py
├── description_1.md
└── hw1-03.txt

assignment_2/
├── algorithm_2.py
├── description_2.md
├── bakery.txt
└── visualization.png

assignment_3/
├── algorithm_3.py
├── description_3.md
└── input_file.txt

assignment_4/
├── algorithm_4.py
└── description.md
```
