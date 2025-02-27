from mqt import qmap
from mqt.qcec import verify

from qiskit import QuantumCircuit
from qiskit.providers.fake_provider import FakeLondon


def test_heuristic_no_swaps_trivial_layout() -> None:
    """Verify that the heuristic mapper works on a simple circuit that requires no swaps on a trivial initial layout."""
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.measure_all()

    qc_mapped, results = qmap.compile(qc, arch=FakeLondon())
    assert results.timeout is False
    assert results.mapped_circuit != ""
    # assert results.output.swaps == 0

    result = verify(qc, qc_mapped)
    assert result.considered_equivalent() is True


def test_heuristic_no_swaps_non_trivial_layout() -> None:
    """Verify that the heuristic mapper works on a simple circuit that requires a non-trivial layout to achieve no swaps."""
    qc = QuantumCircuit(4)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(0, 2)
    qc.cx(0, 3)
    qc.measure_all()

    qc_mapped, results = qmap.compile(qc, arch=FakeLondon())

    assert results.timeout is False
    assert results.mapped_circuit != ""
    # assert results.output.swaps == 0

    result = verify(qc, qc_mapped)
    assert result.considered_equivalent() is True


def test_heuristic_non_trivial_swaps() -> None:
    """Verify that the heuristic mapper works on a simple circuit that requires at least a single SWAP."""
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.cx(2, 0)
    qc.measure_all()

    qc_mapped, results = qmap.compile(qc, arch=FakeLondon())

    assert results.timeout is False
    assert results.mapped_circuit != ""
    assert results.output.swaps == 1

    print("\n")
    print(qc_mapped)

    result = verify(qc, qc_mapped)
    print(result)

    assert result.considered_equivalent() is True
