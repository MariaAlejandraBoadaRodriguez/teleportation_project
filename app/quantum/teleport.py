import pennylane as qml
from pennylane import numpy as np

dev = qml.device("default.qubit", wires=3)

def teleport_and_correct(theta, phi, m0, m1):
    @qml.qnode(dev)
    def circuit():
        psi = np.array([np.cos(theta / 2), np.exp(1j * phi) * np.sin(theta / 2)], dtype=complex)
        qml.MottonenStatePreparation(psi, wires=[0])
        qml.Hadamard(wires=1)
        qml.CNOT(wires=[1, 2])
        qml.CNOT(wires=[0, 1])
        qml.Hadamard(wires=0)
        if m1 == 1:
            qml.PauliX(wires=2)
        if m0 == 1:
            qml.PauliZ(wires=2)
        return qml.state()
    return circuit()

def quantum_teleportation(theta, phi):
    results = []
    for m0 in [0, 1]:
        for m1 in [0, 1]:
            state = teleport_and_correct(theta, phi, m0, m1)
            alpha = state[4]
            beta = state[5]
            results.append((m0, m1, alpha, beta))
    return results
