# Vehicle Routing Problem (VRP) Optimization

This project tackles the **Vehicle Routing Problem (VRP)** using **Genetic Algorithms (GA)** and **Differential Evolution (DE)**. The VRP is a combinatorial optimization problem that focuses on determining the optimal set of routes for a fleet of vehicles to traverse, ensuring customer demands are met while minimizing overall costs.

---

## **Problem Description**
The VRP generalizes the well-known Traveling Salesman Problem (TSP). It involves:
- One or more depots.
- A fleet of vehicles, each starting and ending at a depot.
- A set of customers with specific requirements.

The goal is to optimize routes under given constraints (such as capacity, time windows, and vehicle limits) while minimizing:
- Distance traveled,
- Transportation costs, or
- Delivery time.

---

## **Solution Approach**
This project employs:
1. **Genetic Algorithms (GA):**
   - Simulates natural selection processes such as mutation, crossover, and selection to evolve better solutions.
2. **Differential Evolution (DE):**
   - A population-based optimization technique designed for continuous optimization problems, adapted here for discrete VRP challenges.

These techniques are used to explore the solution space effectively and converge on an optimal or near-optimal set of vehicle routes.

---

## **Features**
- **Flexible Inputs:** 
  - Define the number of vehicles, depots, and customers dynamically.
- **Hybrid Algorithms:**
  - Combines strengths of GA and DE for robust optimization.
- **Constraint Handling:**
  - Ensures operational constraints such as vehicle capacity and depot requirements are respected.
- **Visual Output:**
  - Provides a visual representation of the optimal routes for better insights.

