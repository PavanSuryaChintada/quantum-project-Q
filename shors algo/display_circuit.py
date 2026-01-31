# Import required modules
from shors_alg import build_shor_circuit_for_15
from qiskit.visualization import circuit_drawer
import matplotlib.pyplot as plt

# Create the circuit for N=15, a=7 (you can change 'a' to other values like 2, 4, 8, 11, 13)
qc = build_shor_circuit_for_15(a=7, t=8)

# Draw the circuit
print("Drawing Shor's Algorithm Circuit for N=15, a=7")
fig = qc.draw(output='mpl', fold=100)  # fold=100 prevents line wrapping for better visibility
plt.show()

# Print some information about the circuit
print(f"Number of qubits: {qc.num_qubits}")
print(f"Circuit depth: {qc.depth()}")
print(f"Gate counts: {qc.count_ops()}")
