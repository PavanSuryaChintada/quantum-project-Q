import math
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import QFT
import matplotlib.pyplot as plt

def c_amod15(a: int, power: int) -> QuantumCircuit:
    """Controlled multiplication by a^(2^power) mod 15 on 4 work qubits."""
    if math.gcd(a, 15) != 1:
        raise ValueError("a must be coprime with 15")

    exponent = pow(a, 2**power, 15)
    qc = QuantumCircuit(4)
    
    if exponent == 1:
        pass  # Identity
    elif exponent == 2:
        qc.swap(2, 3)
        qc.swap(1, 2)
        qc.swap(0, 1)
    elif exponent == 4:
        qc.swap(1, 3)
        qc.swap(0, 2)
    elif exponent == 7:
        qc.cx(1, 3)
        qc.cx(0, 2)
        qc.ccx(0, 2, 3)
        qc.cx(0, 2)
        qc.cx(1, 3)
        qc.swap(2, 3)
        qc.swap(1, 2)
        qc.swap(0, 1)
    elif exponent == 8:
        qc.swap(0, 1)
        qc.swap(1, 2)
        qc.swap(2, 3)
    elif exponent == 11:
        qc.swap(0, 2)
        qc.swap(1, 3)
        qc.cx(0, 2)
        qc.cx(1, 3)
        qc.ccx(0, 2, 3)
        qc.cx(0, 2)
        qc.cx(1, 3)
    elif exponent == 13:
        qc.swap(0, 1)
        qc.swap(1, 2)
        qc.swap(2, 3)
        qc.cx(1, 3)
        qc.cx(0, 2)
        qc.ccx(0, 2, 3)
        qc.cx(0, 2)
        qc.cx(1, 3)
    else:
        raise ValueError(f"Unsupported exponent {exponent} for N=15")

    qc = qc.to_gate()
    qc.name = f"*{exponent} mod 15"
    return qc.control()

def build_shor_circuit(a: int, t: int = 8) -> QuantumCircuit:
    """Create the Shor order-finding circuit for N=15 and given base a."""
    if math.gcd(a, 15) != 1:
        raise ValueError("a must be coprime with 15")

    # Counting and work registers
    counting = QuantumRegister(t, name="count")
    work = QuantumRegister(4, name="work")
    classical = ClassicalRegister(t, name="c")
    qc = QuantumCircuit(counting, work, classical)

    # Initialize work register to |1>
    qc.x(work[0])

    # Hadamard on counting register
    qc.h(counting)

    # Controlled modular multiplication by a^(2^j)
    for j in range(t):
        qc.append(c_amod15(a, j), [counting[j]] + list(work))

    # Apply inverse QFT to counting register
    qc.append(QFT(num_qubits=t, inverse=True, do_swaps=True, name="QFT†"), counting)

    # Measure counting register
    qc.measure(counting, classical)
    return qc

# Create and display the circuit for a=7 (you can change this to 2, 4, 8, 11, or 13)
a = 7
t = 8  # Number of counting qubits

print(f"Building Shor's algorithm circuit for N=15, a={a}")
qc = build_shor_circuit(a, t)

# Display the circuit
print("\nCircuit diagram:")
fig = qc.draw(output='mpl', fold=100, scale=0.7)
plt.tight_layout()
plt.show()

# Print circuit information
print("\nCircuit information:")
print(f"Total qubits: {qc.num_qubits}")
print(f"Circuit depth: {qc.depth()}")
print(f"Gate counts: {qc.count_ops()}")
print("\nNote: The circuit may be too large to display clearly. Consider using a smaller 't' value (e.g., t=4) for a simpler visualization.")
