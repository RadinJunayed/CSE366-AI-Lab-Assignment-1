# A* and IDA* Pathfinding Algorithms Simulation

This project demonstrates and compares two important pathfinding algorithms - A* (A-Star) and IDA* (Iterative Deepening A*) - through an interactive visualization built with Pygame. The simulation shows how agents navigate through environments with barriers to complete tasks efficiently.

## Table of Contents
- [Algorithms Overview](#algorithms-overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Simulations](#running-the-simulations)
- [Simulation Features](#simulation-features)
- [Algorithm Analysis and Observations](#algorithm-analysis-and-observations)
- [Implementation Challenges and Solutions](#implementation-challenges-and-solutions)
- [Performance Comparison](#performance-comparison)
- [Further Improvements](#further-improvements)

## Algorithms Overview

### A* Algorithm
A* (A-Star) is a best-first search algorithm that finds the shortest path from a start node to a goal node. It combines:

- **g(n)**: The cost from the start node to the current node
- **h(n)**: A heuristic function that estimates the cost from the current node to the goal
- **f(n) = g(n) + h(n)**: The total estimated cost

A* uses an open set (priority queue) to always expand the node with the lowest f(n) value. It's complete and optimal when using an admissible heuristic.

### IDA* Algorithm
IDA* (Iterative Deepening A*) combines A* with iterative deepening to reduce memory usage. Key features:

- Uses depth-first search with a cutoff value
- Iteratively increases the cutoff value based on f(n)
- Trades time for space (recomputes paths instead of storing them)
- Useful for memory-constrained environments

Both algorithms use the Manhattan distance (sum of horizontal and vertical distances) as the heuristic function in this implementation.

## Project Structure

```
pathfinding-simulation/
│
├── agent.py         - Agent implementations (A* and IDA*)
├── environment.py   - Environment setup with tasks and barriers
├── run.py           - Main simulation runner
└── README.md        - This documentation file
```

## Installation

1. Ensure you have Python 3.6+ installed
2. Install required dependencies:

```bash
pip install pygame
```

## Running the Simulations

To run the A* simulation:

```bash
python run.py
```

To run the IDA* simulation:

```bash
# Replace the agent import in run.py or use the alternative run file
python run_ida.py
```

## Simulation Features

- **Grid Environment**: Customizable grid with random barriers and tasks
- **Real-time Visualization**: See the agent's path planning and execution
- **Interactive Controls**:
  - Start: Begin the simulation
  - Pause/Resume: Control the simulation flow
  - Restart: Generate a new random environment
- **Status Panel**: View detailed statistics about:
  - Tasks completed
  - Current position
  - Steps taken
  - Path costs
  - Nodes expanded
  - Current target

## Algorithm Analysis and Observations

### A* Algorithm
- **Memory Usage**: Uses a priority queue to store all frontier nodes
- **Speed**: Generally faster in simple environments
- **Completeness**: Always finds a solution if one exists
- **Optimality**: Guarantees the shortest path with an admissible heuristic
- **Node Expansion**: Visible through blue highlighted cells in the simulation
- **Path Quality**: Optimal paths shown as blue dots

### IDA* Algorithm
- **Memory Usage**: Significantly lower as it doesn't maintain an open set
- **Speed**: Can be slower due to repeated calculations
- **Node Expansion**: More nodes may be expanded (visible as red highlighted cells)
- **Performance in Complex Environments**: Handles maze-like environments better when memory is constrained
- **Iterative Deepening**: Visible as the explored area grows in waves

### Key Observations
1. A* expands fewer nodes but uses more memory
2. IDA* uses minimal memory but may expand nodes multiple times
3. In environments with many barriers, the difference in node expansion becomes more pronounced
4. Both algorithms find optimal paths, but A* typically does so faster in the simulation

## Implementation Challenges and Solutions

### Challenge 1: Efficient Node Exploration
- **Problem**: Preventing excessive node exploration
- **Solution**: Implemented a closed set to avoid revisiting nodes in A*

### Challenge 2: Memory Management
- **Problem**: A* can consume large amounts of memory in complex environments
- **Solution**: IDA* implementation with bounded memory usage

### Challenge 3: Visualization of Explored Nodes
- **Problem**: Clearly showing the algorithm's exploration process
- **Solution**: Semi-transparent overlays with different colors for expanded nodes

### Challenge 4: Path Reconstruction
- **Problem**: Efficiently tracking and displaying the chosen path
- **Solution**: Used a came_from dictionary in A* and path list in IDA*

### Challenge 5: Real-time Performance
- **Problem**: Balancing computation speed with visualization
- **Solution**: Implemented a delay system and pause functionality

## Performance Comparison

| Aspect | A* Algorithm | IDA* Algorithm |
|--------|-------------|---------------|
| Memory Usage | O(b^d) - Exponential | O(d) - Linear |
| Time Complexity | O(b^d) | O(b^d) in worst case |
| Path Quality | Optimal | Optimal |
| Node Expansion | Fewer | More (with repetition) |
| Best For | Smaller search spaces | Memory-constrained environments |

Where b is the branching factor and d is the solution depth.

## Further Improvements

1. **Algorithm Variants**: Add weighted A* and other variants
2. **Multiple Agents**: Compare cooperative pathfinding approaches
3. **Dynamic Obstacles**: Add moving barriers to test replanning
4. **Different Heuristics**: Compare performance with various heuristics
5. **User-Created Maps**: Allow custom environment creation
6. **Performance Metrics**: Add timing and memory usage statistics
7. **Path Smoothing**: Implement post-processing to smooth paths

## License

This project is open source and available under the MIT License.
