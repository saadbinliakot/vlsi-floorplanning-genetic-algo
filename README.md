# Genetic Algorithm for VLSI Floorplanning

An artificial intelligence approach to optimizing VLSI (Very Large Scale Integration) floorplanning. This project implements a Genetic Algorithm (GA) to determine the optimal $(x, y)$ coordinate placement of foundational macro blocks (such as the ALU, Cache, Control Unit, and Register File) on a fixed-size 2D grid.

The algorithm aims to find a placement layout that satisfies strict structural constraints while optimizing overall performance metrics.

---

## 🚀 Optimization Objectives

The fitness function evaluates layouts by minimizing or maximizing three key criteria:
1. **Overlap Minimization (Hard Constraint):** Ensures no two hardware modules share the same physical grid coordinates.
2. **Wirelength Minimization:** Calculates total interconnect routing using Euclidean distance across connected components in a topological graph.
3. **Bounding Box Area Minimization:** Minimizes the total physical chip area footprint required to encompass all modules.

---

## 🛠️ Genetic Operations Implemented

* **Chromosomal Representation:** Layout structures are encoded as arrays of $(x, y)$ coordinates mapped to specific hardware dimensions.
* **Selection:** Roulette Wheel Selection (Fitness Proportionate Selection) biased towards layouts with fewer overlaps and shorter wirelengths.
* **Crossover:** Supports both **Single-Point Crossover** and **Two-Point Crossover** mechanisms to evaluate evolutionary convergence properties.
* **Mutation:** Random coordinate shift mutation with a low threshold probability ($7.5\%$) to introduce genetic diversity and escape local optima.
* **Elitism:** Tracks and preserves the top 2 highest-performing chromosome designs across generational cycles.

---

## 📋 Sample Dataset & Input Format

The script reads the grid restrictions, parses coordinate setups for 6 consecutive population structures, and assigns functional graphs.

### Execution Input
```text
6 25 25
9 3 12 15 13 16 1 13 4 15 9 6
8 0 7 12 4 11 1 13 14 10 9 11
6 5 12 9 9 7 8 6 2 7 3 1
3 11 11 12 14 11 6 10 3 11 3 0
10 12 8 16 10 4 13 6 6 0 3 7
0 2 0 0 14 12 4 5 12 4 3 10