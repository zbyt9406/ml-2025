# 🎮 Machine Learning Mini-Project 4: Reinforcement Learning

This repository contains the **fourth and final mini-project** for the **Machine Learning (Spring 2025)** course at **K. N. Toosi University of Technology**.  
It provides a structured journey through **Reinforcement Learning (RL)**:  
from **tabular methods** (Q-Learning) ➝ to **Deep Q-Networks (DQN)** ➝ to **Policy Gradient methods (REINFORCE)**.

---

## 📁 Project Structure

├── Question_1_Q_Learning/
│ └── Tabular Q-Learning in a discrete Gridworld environment
├── Question_2_Deep_Q_Networks/
│ └── Deep Q-Network (DQN) implementation for continuous state spaces
├── Question_3_Policy_Gradients/
│ └── REINFORCE algorithm (Policy Gradient) implementation
└── README.md

---

## 🤖 Question 1: Q-Learning in a Discrete Environment

An introduction to **core RL concepts**: Agent, Environment, States, Actions, Rewards.  
Implements **Q-Learning** from scratch in a simple **Gridworld**-style environment.

### 🔑 Key Steps
- **Q-Learning Algorithm**  
  - Model-free, off-policy RL method.  
  - Learns an **optimal action-value function** with the **Bellman equation**.  
  - Stores values in a **Q-table**.  

- **Exploration vs. Exploitation**  
  - Uses an **epsilon-greedy** policy to balance exploration of new actions with exploitation of known good ones.  

- **Evaluation**  
  - Agent trained until it discovers an **optimal policy**, maximizing cumulative rewards.  

---

## 🧠 Question 2: Deep Q-Networks (DQN)

Extends Q-Learning to environments with **large/continuous state spaces** using **neural networks** as function approximators.  
Applied to the **CartPole-v1** environment.

### 🔑 Key Steps
- **Function Approximation**  
  - Q-table replaced with a **Deep Neural Network**.  
  - Input: state vector ➝ Output: Q-value for each action.  

- **Training Stabilization**  
  - **Experience Replay**: Stores experiences `(s, a, r, s')` in a buffer and samples mini-batches for training.  
  - **Target Network**: A separate, periodically updated network provides stable target Q-values.  

- **Application**  
  - DQN agent trained to **balance a pole** on a moving cart.  
  - Performance evaluated by episode length and reward.  

---

## 📈 Question 3: Policy Gradient Methods (REINFORCE)

Introduces **Policy-Based RL**: instead of learning a value function, the agent learns a **parameterized policy directly**.  
Implements the **REINFORCE algorithm**.

### 🔑 Key Steps
- **Value-Based vs. Policy-Based**  
  - Q-Learning (value-based): estimates action values.  
  - REINFORCE (policy-based): learns probabilities of actions.  
  - Policy-based methods are ideal for **continuous action spaces** or **stochastic policies**.  

- **REINFORCE Algorithm**  
  - Policy represented by a neural network.  
  - Input: state ➝ Output: probability distribution over actions.  
  - Actions are **sampled** from the distribution.  
  - After each episode, parameters are updated using the **Policy Gradient Theorem**:  
    - Increase probability of good actions.  
    - Decrease probability of bad actions.  

- **Application & Comparison**  
  - Applied to **CartPole** environment.  
  - Learning curve and performance compared with **DQN** from Question 2.  

---

## 📌 Summary

This mini-project provides:
- Hands-on understanding of **Q-Learning** and **epsilon-greedy exploration**.  
- Implementation of **Deep Q-Networks** with stability tricks (Replay Buffer & Target Network).  
- Exposure to **Policy Gradient methods**, specifically **REINFORCE**.  
- A practical comparison between **value-based** and **policy-based** RL methods.  

---



## 📄 License
This project is licensed under the **MIT License** — see the `LICENSE` file for details.
