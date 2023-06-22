import numpy as np
from sat.models.SATNMBase import SATBase


class AlgorithmQUBO(SATBase):

    # 3 5 5 6 in pattern qubos -1, 1, 10
    # In Paper: QCE 2023
    def __init__(self, formula):
        super().__init__(formula)

    def create_qubo(self):
        for clause_index, clause in enumerate(self.formula):
            if list(np.sign(clause)) == [1, 1, 1]:
                self.add(clause[0], clause[0], 0.0)
                self.add(clause[0], clause[1], 1.0)
                self.add(clause[0], clause[2], 0.0)
                self.add(clause[0], self.num_variables + clause_index + 1, -1.0)
                self.add(clause[1], clause[1], 0.0)
                self.add(clause[1], clause[2], 0.0)
                self.add(clause[1], self.num_variables + clause_index + 1, -1.0)
                self.add(clause[2], clause[2], -1.0)
                self.add(clause[2], self.num_variables + clause_index + 1, 1.0)
                self.add(self.num_variables + clause_index + 1, self.num_variables + clause_index + 1, 0.0)

            elif list(np.sign(clause)) == [1, 1, -1]:
                self.add(clause[0], clause[0], 0.0)
                self.add(clause[0], clause[1], 0.0)
                self.add(clause[0], clause[2], 0.0)
                self.add(clause[0], self.num_variables + clause_index + 1, -1.0)
                self.add(clause[1], clause[1], 0.0)
                self.add(clause[1], clause[2], -1.0)
                self.add(clause[1], self.num_variables + clause_index + 1, 1.0)
                self.add(clause[2], clause[2], 1.0)
                self.add(clause[2], self.num_variables + clause_index + 1, -1.0)
                self.add(self.num_variables + clause_index + 1, self.num_variables + clause_index + 1, 1.0)

            elif list(np.sign(clause)) == [1, -1, -1]:
                self.add(clause[0], clause[0], 0.0)
                self.add(clause[0], clause[1], -1.0)
                self.add(clause[0], clause[2], 0.0)
                self.add(clause[0], self.num_variables + clause_index + 1, 1.0)
                self.add(clause[1], clause[1], 1.0)
                self.add(clause[1], clause[2], 0.0)
                self.add(clause[1], self.num_variables + clause_index + 1, -1.0)
                self.add(clause[2], clause[2], 0.0)
                self.add(clause[2], self.num_variables + clause_index + 1, 1.0)
                self.add(self.num_variables + clause_index + 1, self.num_variables + clause_index + 1, 0.0)

            else:
                self.add(clause[0], clause[0], 0.0)
                self.add(clause[0], clause[1], 0.0)
                self.add(clause[0], clause[2], 0.0)
                self.add(clause[0], self.num_variables + clause_index + 1, 1.0)
                self.add(clause[1], clause[1], 0.0)
                self.add(clause[1], clause[2], 1.0)
                self.add(clause[1], self.num_variables + clause_index + 1, -1.0)
                self.add(clause[2], clause[2], 0.0)
                self.add(clause[2], self.num_variables + clause_index + 1, -1.0)
                self.add(self.num_variables + clause_index + 1, self.num_variables + clause_index + 1, 1.0)

