# Quick notes on smart contracts

A smart contract is a contract with aditional blockchain features. It is a computer program or a transaction protocol to automatically execute, control or document legally relevant actions/events according to some contract terms.

## What does it solve?

- the need of trusted intermediates
- accidental exceptions
- malicious attacks
- fraud losses
- arbitrations and enforcement costs
- cost reduction (no intermediates)
- speed (no intermediates)

## Vending machine analogy

A smart contract is like a vending machine, you just insert the coin and select what you want, reducing the need for an intermediate to get your snack.

A smart contract is a "virtual and online" vending machine

## Law

Some legal academics say that smart contracts are not legal agreements.

A smart contract is not necessarily legally enforceable as a contract. But a smart legal contract has all the elements of a legally blinding contract in the jurisdiction where applicable.

A smart legal contract can be enforced by a court of law.

-------------------------------------------------------

- A smart contract can be any kind of computer program. It can be viewed as a collection of code and data deployed using cryptographically signed transactions on the blockchain.

- For database experts, a smart contract can be viewed as a secure stored procedure.

- Smart contracts cannot be modified after a transactions (after being stored in the blockchain).

## How does a smart contract works?

A smart contract occurs by sending a transaction from a wallet. **Transactions include the compiled code for the smart contract and a receiver address**

Smart contracts can store arbitrary states and execute arbitrary computations.

Once deployed it cannot be updated.

## What are blockchain transactions?

1. Transactions must be included in a blockchain block.
2. End-clients interact with a smart contract through transactions.
3. Transactions can invoke other smart contracts.
4. Transactions might result in changing the state and sending coins from one account to another.

## Programming languages for smart contracts

ETH blockchain:
	- Solidity
	- Vyper

Solana blockchain:
	- Rust (yes, Rust!!!)

Other programming languages:
	- JavaScript (Hyperledge Fabric)
	- Ivy
	- Scilla
	- Bitcoin Script

## Security Issues

A blockchain-based smart contract is visible to all blockchain users. This can lead to a situation where bugs (including security holes), are visible to all, but yet, not easily fixable.

### Ethereum issues

- No central resource for documenting known vulnerabilities
- Blockchain network attacks
- Bugs immutability (once deployed, smart contracts can't be modified)
- Compiler bugs
- EVM (*Ethereum Virtual Machine*) bugs
