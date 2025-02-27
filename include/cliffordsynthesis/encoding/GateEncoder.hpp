//
// This file is part of the MQT QMAP library released under the MIT license.
// See README.md or go to https://github.com/cda-tum/qmap for more information.
//

#pragma once

#include "LogicBlock/LogicBlock.hpp"
#include "cliffordsynthesis/Results.hpp"
#include "cliffordsynthesis/encoding/TableauEncoder.hpp"
#include "operations/OpType.hpp"

#include <cstddef>
#include <memory>

namespace cs::encoding {

class GateEncoder {
public:
  GateEncoder(const std::size_t nQubits, const std::size_t timestepLimit,
              TableauEncoder::Variables*             tableauVars,
              std::shared_ptr<logicbase::LogicBlock> logicBlock)
      : N(nQubits), T(timestepLimit), tvars(tableauVars),
        lb(std::move(logicBlock)) {}
  virtual ~GateEncoder() = default;

  struct Variables {
    // variables for the single-qubit gates
    logicbase::LogicMatrix3D gS{};
    // variables for the two-qubit gates
    logicbase::LogicMatrix3D gC{};

    void
         collectSingleQubitGateVariables(std::size_t pos, std::size_t qubit,
                                         logicbase::LogicVector& variables) const;
    void collectTwoQubitGateVariables(std::size_t pos, std::size_t qubit,
                                      bool                    target,
                                      logicbase::LogicVector& variables) const;
  };

  // variable creation
  void createSingleQubitGateVariables();
  void createTwoQubitGateVariables();

  // encode the relation between the tableaus and the gates
  virtual void encodeGates() {
    assertConsistency();
    assertGateConstraints();
  }

  virtual void encodeSymmetryBreakingConstraints();

  // extracting the circuit
  void extractCircuitFromModel(Results& res, logicbase::Model& model);

  [[nodiscard]] auto* getVariables() { return &vars; }

  static constexpr std::array<qc::OpType, 7> SINGLE_QUBIT_GATES = {
      qc::OpType::None, qc::OpType::X, qc::OpType::Y,   qc::OpType::Z,
      qc::OpType::H,    qc::OpType::S, qc::OpType::Sdag};
  [[nodiscard]] static constexpr std::size_t
  gateToIndex(const qc::OpType type) {
    for (std::size_t i = 0; i < SINGLE_QUBIT_GATES.size(); ++i) {
      if (SINGLE_QUBIT_GATES.at(i) == type) {
        return i;
      }
    }
    return 0;
  }

protected:
  // number of qubits N
  std::size_t N{}; // NOLINT (readability-identifier-naming)
  // timestep limit T
  std::size_t T{}; // NOLINT (readability-identifier-naming)

  // the gate variables
  Variables vars{};

  // the tableau variables
  TableauEncoder::Variables* tvars{};

  // the logic block to use
  std::shared_ptr<logicbase::LogicBlock> lb{};

  void assertExactlyOne(const logicbase::LogicVector& variables) const;

  virtual void assertConsistency() const = 0;

  virtual void assertGateConstraints()                           = 0;
  virtual void assertSingleQubitGateConstraints(std::size_t pos) = 0;
  [[nodiscard]] virtual logicbase::LogicTerm
  createSingleQubitGateConstraint(std::size_t pos, std::size_t qubit,
                                  qc::OpType gate)            = 0;
  virtual void assertTwoQubitGateConstraints(std::size_t pos) = 0;
  [[nodiscard]] virtual logicbase::LogicTerm
  createTwoQubitGateConstraint(std::size_t pos, std::size_t ctrl,
                               std::size_t trgt) = 0;

  void extractSingleQubitGatesFromModel(std::size_t             pos,
                                        logicbase::Model&       model,
                                        qc::QuantumComputation& qc,
                                        std::size_t& nSingleQubitGates);
  void extractTwoQubitGatesFromModel(std::size_t pos, logicbase::Model& model,
                                     qc::QuantumComputation& qc,
                                     std::size_t&            nTwoQubitGates);

  virtual void
  assertSingleQubitGateSymmetryBreakingConstraints(std::size_t pos);
  virtual void assertTwoQubitGateSymmetryBreakingConstraints(std::size_t pos);

  virtual void assertSingleQubitGateOrderConstraints(std::size_t pos,
                                                     std::size_t qubit) = 0;
  virtual void assertSingleQubitGateCancellationConstraints(std::size_t pos,
                                                            std::size_t qubit);

  virtual void assertTwoQubitGateOrderConstraints(std::size_t pos,
                                                  std::size_t ctrl,
                                                  std::size_t trgt) = 0;
};
} // namespace cs::encoding
