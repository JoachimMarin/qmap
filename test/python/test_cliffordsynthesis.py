from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import pytest
from mqt import qcec, qmap

from qiskit import QuantumCircuit
from qiskit.quantum_info import Clifford, PauliList


@dataclass
class Configuration:
    """Configuration for a test case."""

    expected_minimal_gates: int
    expected_minimal_depth: int
    expected_minimal_gates_at_minimal_depth: int
    expected_minimal_two_qubit_gates: int
    expected_minimal_gates_at_minimal_two_qubit_gates: int

    description: str
    initial_tableau: str | None = None
    target_tableau: str | None = None
    initial_circuit: str | None = None


def create_circuit_tests() -> list[Configuration]:
    path = Path(__file__).resolve().parent.parent / "cliffordsynthesis" / "circuits.json"
    with path.open() as f:
        circuits = json.load(f)
    return [Configuration(**c) for c in circuits]


def create_tableau_tests() -> list[Configuration]:
    path = Path(__file__).resolve().parent.parent / "cliffordsynthesis" / "tableaus.json"
    with path.open() as f:
        tableaus = json.load(f)
    return [Configuration(**t) for t in tableaus]


@pytest.mark.parametrize("test_config", create_circuit_tests())
@pytest.mark.parametrize("use_maxsat", [True, False], ids=["maxsat", "binary_search"])
def test_optimize_clifford_gates(test_config: Configuration, use_maxsat: bool) -> None:
    circ, results = qmap.optimize_clifford(
        circuit=test_config.initial_circuit, use_maxsat=use_maxsat, target_metric="gates"
    )

    assert results.gates == test_config.expected_minimal_gates
    print("\n", circ)


@pytest.mark.parametrize("test_config", create_circuit_tests())
@pytest.mark.parametrize("use_maxsat", [True, False], ids=["maxsat", "binary_search"])
def test_optimize_clifford_depth(test_config: Configuration, use_maxsat: bool) -> None:
    circ, results = qmap.optimize_clifford(
        circuit=test_config.initial_circuit, use_maxsat=use_maxsat, target_metric="depth"
    )

    assert results.depth == test_config.expected_minimal_depth
    print("\n", circ)


@pytest.mark.parametrize("test_config", create_circuit_tests())
@pytest.mark.parametrize("use_maxsat", [True, False], ids=["maxsat", "binary_search"])
def test_optimize_clifford_gates_at_minimal_depth(test_config: Configuration, use_maxsat: bool) -> None:
    circ, results = qmap.optimize_clifford(
        circuit=test_config.initial_circuit,
        use_maxsat=use_maxsat,
        target_metric="depth",
        minimize_gates_after_depth_optimization=True,
    )

    assert results.gates == test_config.expected_minimal_gates_at_minimal_depth
    print("\n", circ)


@pytest.mark.parametrize("test_config", create_circuit_tests())
@pytest.mark.parametrize("use_maxsat", [True, False], ids=["maxsat", "binary_search"])
def test_optimize_clifford_two_qubit_gates(test_config: Configuration, use_maxsat: bool) -> None:
    circ, results = qmap.optimize_clifford(
        circuit=test_config.initial_circuit,
        use_maxsat=use_maxsat,
        target_metric="two_qubit_gates",
        try_higher_gate_limit_for_two_qubit_gate_optimization=True,
    )

    assert results.two_qubit_gates == test_config.expected_minimal_two_qubit_gates
    print("\n", circ)


@pytest.mark.parametrize("test_config", create_circuit_tests())
@pytest.mark.parametrize("use_maxsat", [True, False], ids=["maxsat", "binary_search"])
def test_optimize_clifford_gates_at_minimal_two_qubit_gates(test_config: Configuration, use_maxsat: bool) -> None:
    circ, results = qmap.optimize_clifford(
        circuit=test_config.initial_circuit,
        use_maxsat=use_maxsat,
        target_metric="two_qubit_gates",
        try_higher_gate_limit_for_two_qubit_gate_optimization=True,
        minimize_gates_after_two_qubit_gate_optimization=True,
    )

    assert results.gates == test_config.expected_minimal_gates_at_minimal_two_qubit_gates
    print("\n", circ)


@pytest.mark.parametrize("test_config", create_tableau_tests())
@pytest.mark.parametrize("use_maxsat", [True, False], ids=["maxsat", "binary_search"])
def test_synthesize_clifford_gates(test_config: Configuration, use_maxsat: bool) -> None:
    circ, results = qmap.synthesize_clifford(
        target_tableau=test_config.target_tableau,
        initial_tableau=test_config.initial_tableau,
        use_maxsat=use_maxsat,
        target_metric="gates",
    )

    assert results.gates == test_config.expected_minimal_gates
    print("\n", circ)


@pytest.mark.parametrize("test_config", create_tableau_tests())
@pytest.mark.parametrize("use_maxsat", [True, False], ids=["maxsat", "binary_search"])
def test_synthesize_clifford_depth(test_config: Configuration, use_maxsat: bool) -> None:
    circ, results = qmap.synthesize_clifford(
        target_tableau=test_config.target_tableau,
        initial_tableau=test_config.initial_tableau,
        use_maxsat=use_maxsat,
        target_metric="depth",
    )

    assert results.depth == test_config.expected_minimal_depth
    print("\n", circ)


@pytest.mark.parametrize("test_config", create_tableau_tests())
@pytest.mark.parametrize("use_maxsat", [True, False], ids=["maxsat", "binary_search"])
def test_synthesize_clifford_gates_at_minimal_depth(test_config: Configuration, use_maxsat: bool) -> None:
    circ, results = qmap.synthesize_clifford(
        target_tableau=test_config.target_tableau,
        initial_tableau=test_config.initial_tableau,
        use_maxsat=use_maxsat,
        target_metric="depth",
        minimize_gates_after_depth_optimization=True,
    )

    assert results.gates == test_config.expected_minimal_gates_at_minimal_depth
    print("\n", circ)


@pytest.mark.parametrize("test_config", create_tableau_tests())
@pytest.mark.parametrize("use_maxsat", [True, False], ids=["maxsat", "binary_search"])
def test_synthesize_clifford_two_qubit_gates(test_config: Configuration, use_maxsat: bool) -> None:
    circ, results = qmap.synthesize_clifford(
        target_tableau=test_config.target_tableau,
        initial_tableau=test_config.initial_tableau,
        use_maxsat=use_maxsat,
        target_metric="two_qubit_gates",
        try_higher_gate_limit_for_two_qubit_gate_optimization=True,
    )

    assert results.two_qubit_gates == test_config.expected_minimal_two_qubit_gates
    print("\n", circ)


@pytest.mark.parametrize("test_config", create_tableau_tests())
@pytest.mark.parametrize("use_maxsat", [True, False], ids=["maxsat", "binary_search"])
def test_synthesize_clifford_gates_at_minimal_two_qubit_gates(test_config: Configuration, use_maxsat: bool) -> None:
    circ, results = qmap.synthesize_clifford(
        target_tableau=test_config.target_tableau,
        initial_tableau=test_config.initial_tableau,
        use_maxsat=use_maxsat,
        target_metric="two_qubit_gates",
        try_higher_gate_limit_for_two_qubit_gate_optimization=True,
        minimize_gates_after_two_qubit_gate_optimization=True,
    )

    assert results.gates == test_config.expected_minimal_gates_at_minimal_two_qubit_gates
    print("\n", circ)


# The following tests merely check that all kinds of conversions work as expected.
# They only check for the correctness of the result for a simple circuit.


@pytest.fixture
def bell_circuit() -> QuantumCircuit:
    """Return a Bell state circuit."""
    circ = QuantumCircuit(2)
    circ.h(0)
    circ.cx(0, 1)
    return circ


def test_optimize_quantum_computation(bell_circuit: QuantumCircuit) -> None:
    """Test that we can optimize an MQT QuantumComputation."""
    qc = qmap.QuantumComputation.from_qiskit(bell_circuit)
    circ, results = qmap.optimize_clifford(circuit=qc)
    assert qcec.verify(circ, bell_circuit).considered_equivalent()


def test_optimize_from_qasm_file(bell_circuit: QuantumCircuit) -> None:
    """Test that we can optimize from a QASM file."""
    with Path("bell.qasm").open("w") as f:
        f.write(bell_circuit.qasm())
    circ, results = qmap.optimize_clifford(circuit="bell.qasm")
    assert qcec.verify(circ, bell_circuit).considered_equivalent()


def test_optimize_qiskit_circuit(bell_circuit: QuantumCircuit) -> None:
    """Test that we can optimize a Qiskit QuantumCircuit."""
    circ, results = qmap.optimize_clifford(circuit=bell_circuit)
    assert qcec.verify(circ, bell_circuit).considered_equivalent()


def test_optimize_with_initial_tableau(bell_circuit: QuantumCircuit) -> None:
    """Test that we can optimize a circuit with an initial tableau."""
    circ, results = qmap.optimize_clifford(circuit=bell_circuit, initial_tableau=qmap.Tableau(bell_circuit.num_qubits))
    assert qcec.verify(circ, bell_circuit).considered_equivalent()


def test_synthesize_from_tableau(bell_circuit: QuantumCircuit) -> None:
    """Test that we can synthesize a circuit from an MQT Tableau."""
    tableau = qmap.Tableau("['XX', 'ZZ']")
    circ, results = qmap.synthesize_clifford(target_tableau=tableau)
    assert qcec.verify(circ, bell_circuit).considered_equivalent()


def test_synthesize_from_qiskit_clifford(bell_circuit: QuantumCircuit) -> None:
    """Test that we can synthesize a circuit from a Qiskit Clifford."""
    cliff = Clifford(bell_circuit)
    circ, results = qmap.synthesize_clifford(target_tableau=cliff)
    assert qcec.verify(circ, bell_circuit).considered_equivalent()


def test_synthesize_from_qiskit_pauli_list(bell_circuit: QuantumCircuit) -> None:
    """Test that we can synthesize a circuit from a Qiskit PauliList."""
    pauli_list = PauliList(["XX", "ZZ"])
    circ, results = qmap.synthesize_clifford(target_tableau=pauli_list)
    assert qcec.verify(circ, bell_circuit).considered_equivalent()


def test_invalid_kwarg_to_synthesis() -> None:
    """Test that we raise an error if we pass an invalid kwarg to synthesis."""
    with pytest.raises(ValueError):
        qmap.synthesize_clifford(target_tableau=qmap.Tableau("Z"), invalid_kwarg=True)
