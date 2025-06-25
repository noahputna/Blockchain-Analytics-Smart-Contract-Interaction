# Blockchain Analytics & Smart Contract Interaction

This project simulates a decentralised token-based marketplace, where users purchase products using a custom ERC-20 token called **BMMCoin**. It demonstrates smart contract interaction using Python (`Web3.py`) and explored blockchain-based demand analytics through both real-time logic and mock simulations.

Developed as part of the University of Melbourne subject **FNCE30012: Foundations of Fintech**, this repository now includes:
- The original assignment notebook.
- A fully functional simulation version using mock block data.

---

## Important Note
The `Blockchain Analytics & Smart Contract Interaction (FNCE30012).py` will not fully run outsude of the original university-controlled environment.
This is due to:
- Custom internal modules (`bmmnet`).
- Missing blockchain credentials and private keys.
- Inaccessible node connections.

To provide a complete, working version, a seperate simulation (`BMM Blockchain Simulation.py`) has been created with mock blockchain data. This is to reproduce and illustrate key analytics and plots.

---

## Features

### Smart Contracts
- `BMMCoin.sol`: ERC-20 token contract (OpenZeppelin standard).
- `BMMMarket.sol`: Contract for purchasing products A, B, C with BMMCoin.

### Python + Blockchain Interaction
