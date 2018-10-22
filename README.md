# Solutions to ECE209AS Robotics Pset2

Code base and the Testbench for getting results

## Overview
The code include each class component and the testbench for getting results.
### Prerequisites

* python3
* numpy
* matplotlib
## Descriptions
### Basic Components
* Action.py: Class for action component
* State.py: Class for state component
* Env.py: Class for creating the state space (the environment) and calculating the adjacent possible states given current state.
* Policy.py: Class for policy component. Initialize policy matrix given rules of project.
### Main
* Agent.py: Class for agent (robot). Essential functions for creating trajetcory, policy iteration and value iteration etc.
### Test
* testbench.py: Code sections for each problem.
* Solution2Pset.ipynb: Jupyer notbook for running code.

## Running the tests

The code encapsulation has been done in testbench.py. Run the code in each section corresponding to problems those need some results. (e.g value and figures) 

## Authors

* **Yuxiao Huang** - [Pillumina](https://github.com/Pillumina)

## References

* Reinforcement Learning: An Introduction (Sutton & Barto)
* https://github.com/dennybritz/reinforcement-learning.git 



