"""
Grover's Algorithm - Step by Step Implementation

This script provides a clear, step-by-step implementation of Grover's algorithm
with detailed explanations and visualizations.
"""

# Step 1: Import required libraries
print("Step 1: Importing required libraries...")
from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram, plot_bloch_multivector
import numpy as np
import matplotlib.pyplot as plt

# Step 2: Define the number of qubits and target state
print("\nStep 2: Setting up the problem...")
n_qubits = 2
target = '11'  # The state we want to find
print(f"We'll search for the state |{target}> in a {n_qubits}-qubit system")

# Step 3: Create a quantum circuit
print("\nStep 3: Creating quantum circuit...")
qc = QuantumCircuit(n_qubits, n_qubits)  # n_qubits quantum bits, n_qubits classical bits
print("Created quantum circuit with", n_qubits, "qubits")

# Step 4: Initialize superposition
print("\nStep 4: Applying Hadamard gates to create superposition...")
qc.h(range(n_qubits))
print("Applied Hadamard gates to all qubits")
print("State after superposition: (|00> + |01> + |10> + |11>)/2")

# Visualize the circuit so far
print("\nCircuit after superposition:")
display(qc.draw('mpl'))

# Step 5: Define and apply the oracle
print("\nStep 5: Applying the oracle...")
print(f"The oracle marks the target state |{target}> with a phase of -1")

# For |11> target, we can use a controlled-Z gate
if target == '11':
    qc.cz(0, 1)  # Controlled-Z gate
    print("Applied CZ gate (control=qubit 0, target=qubit 1)")

# Visualize the circuit after oracle
print("\nCircuit after oracle:")
display(qc.draw('mpl'))

# Step 6: Apply the diffusion operator (Grover diffusion)
print("\nStep 6: Applying the diffusion operator...")
print("This step amplifies the amplitude of the marked state")

# Apply Hadamard gates
qc.h(range(n_qubits))
print("Applied Hadamard gates to all qubits")

# Apply X gates
qc.x(range(n_qubits))
print("Applied X gates to all qubits")

# Apply multi-controlled Z gate (for 2 qubits, this is just CZ)
if n_qubits == 2:
    qc.cz(0, 1)
    print("Applied CZ gate (control=qubit 0, target=qubit 1)")

# Apply X gates again
qc.x(range(n_qubits))
print("Applied X gates to all qubits")

# Apply Hadamard gates again
qc.h(range(n_qubits))
print("Applied Hadamard gates to all qubits")

# Visualize the complete circuit
print("\nComplete Grover's circuit:")
display(qc.draw('mpl'))

# Step 7: Add measurement
print("\nStep 7: Adding measurement...")
qc.measure(range(n_qubits), range(n_qubits))
print("Added measurement operations")

# Visualize the final circuit
print("\nFinal circuit with measurements:")
display(qc.draw('mpl'))

# Step 8: Simulate the circuit
print("\nStep 8: Running simulation...")
simulator = Aer.get_backend('qasm_simulator')
result = execute(qc, backend=simulator, shots=1024).result()
counts = result.get_counts()

# Step 9: Display results
print("\nStep 9: Displaying results...")
print("\nMeasurement results:")
print(counts)

# Plot the results
print("\nVisualizing the measurement results:")
plot_histogram(counts)
plt.title(f"Grover's Algorithm Results for |{target}>")
plt.show()

print("\nNote: The algorithm successfully amplifies the probability of measuring the target state |{}>.".format(target))
