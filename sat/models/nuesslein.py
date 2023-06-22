from sat.models.SATNMBase import SATBase
import numpy as np


class NuessleinNM(SATBase):

    def __init__(self, formula):
        super().__init__(formula)

    # this function creates the QUBO-Matrix
    def create_qubo(self):
        for i, c in enumerate(self.formula):
            if list(np.sign(c)) == [1, 1, 1]:
                self.add(c[0], c[1], 2)
                self.add(c[0], self.num_variables + i + 1, -2)
                self.add(c[1], self.num_variables + i + 1, -2)
                self.add(c[2], c[2], -1)
                self.add(c[2], self.num_variables + i + 1, 1)
                self.add(self.num_variables + i + 1, self.num_variables + i + 1, 1)
            elif list(np.sign(c)) == [1, 1, -1]:
                self.add(c[0], c[1], 2)
                self.add(c[0], self.num_variables + i + 1, -2)
                self.add(c[1], self.num_variables + i + 1, -2)
                self.add(c[2], c[2], 1)
                self.add(c[2], self.num_variables + i + 1, -1)
                self.add(self.num_variables + i + 1, self.num_variables + i + 1, 2)
            elif list(np.sign(c)) == [1, -1, -1]:
                self.add(c[0], c[0], 2)
                self.add(c[0], c[1], -2)
                self.add(c[0], self.num_variables + i + 1, -2)
                self.add(c[1], self.num_variables + i + 1, 2)
                self.add(c[2], c[2], 1)
                self.add(c[2], self.num_variables + i + 1, -1)
            else:
                self.add(c[0], c[0], -1)
                self.add(c[0], c[1], 1)
                self.add(c[0], c[2], 1)
                self.add(c[0], self.num_variables + i + 1, 1)
                self.add(c[1], c[1], -1)
                self.add(c[1], c[2], 1)
                self.add(c[1], self.num_variables + i + 1, 1)
                self.add(c[2], c[2], -1)
                self.add(c[2], self.num_variables + i + 1, 1)
                self.add(self.num_variables + i + 1, self.num_variables + i + 1, -1)



