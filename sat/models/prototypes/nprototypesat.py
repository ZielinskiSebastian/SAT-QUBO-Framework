import numpy as np
from sat.models.SATNMBase import SATBase
import os


class NPrototypeSAT(SATBase):

    def __init__(self, formula):
        super().__init__(formula)

        self.clause_qubos = []

    def add_clause_qubos(self, c0, c1, c2, c3):
        self.clause_qubos = [c0, c1, c2, c3]

    def create_qubo(self):
        for clause_index, clause in enumerate(self.formula):
            if list(np.sign(clause)) == [1, 1, 1]:
                self.add(clause[0], clause[0], self.clause_qubos[0][(0, 0)])
                self.add(clause[0], clause[1], self.clause_qubos[0][(0, 1)])
                self.add(clause[0], clause[2], self.clause_qubos[0][(0, 2)])
                self.add(clause[1], clause[1], self.clause_qubos[0][(1, 1)])
                self.add(clause[1], clause[2], self.clause_qubos[0][(1, 2)])
                self.add(clause[2], clause[2], self.clause_qubos[0][(2, 2)])

            elif list(np.sign(clause)) == [1, 1, -1]:
                self.add(clause[0], clause[0], self.clause_qubos[1][(0, 0)])
                self.add(clause[0], clause[1], self.clause_qubos[1][(0, 1)])
                self.add(clause[0], clause[2], self.clause_qubos[1][(0, 2)])
                self.add(clause[1], clause[1], self.clause_qubos[1][(1, 1)])
                self.add(clause[1], clause[2], self.clause_qubos[1][(1, 2)])
                self.add(clause[2], clause[2], self.clause_qubos[1][(2, 2)])


            elif list(np.sign(clause)) == [1, -1, -1]:
                self.add(clause[0], clause[0], self.clause_qubos[2][(0, 0)])
                self.add(clause[0], clause[1], self.clause_qubos[2][(0, 1)])
                self.add(clause[0], clause[2], self.clause_qubos[2][(0, 2)])
                self.add(clause[1], clause[1], self.clause_qubos[2][(1, 1)])
                self.add(clause[1], clause[2], self.clause_qubos[2][(1, 2)])
                self.add(clause[2], clause[2], self.clause_qubos[2][(2, 2)])

            else:
                self.add(clause[0], clause[0], self.clause_qubos[3][(0, 0)])
                self.add(clause[0], clause[1], self.clause_qubos[3][(0, 1)])
                self.add(clause[0], clause[2], self.clause_qubos[3][(0, 2)])
                self.add(clause[1], clause[1], self.clause_qubos[3][(1, 1)])
                self.add(clause[1], clause[2], self.clause_qubos[3][(1, 2)])
                self.add(clause[2], clause[2], self.clause_qubos[3][(2, 2)])


    def export_prototype(self, filename):
        """This function creates a SAT-QUBO-class that does no longer need class qubos to be specified."""
        proto_string_path = os.path.join(os.getcwd(), "sat", "models", "prototypes", "n_prototype_string.txt")

        with open(proto_string_path, "r") as file:
            proto_string = file.read()

        for clause_type in range(4):
            for i in range(3):
                for j in range(i, 3):
                   proto_string = proto_string.replace("self.clause_qubos["+str(clause_type)+"][("+str(i)+", " + str(j)+")]", str(self.clause_qubos[clause_type][(i, j)]))

        proto_export_path = os.path.join(os.getcwd(), "sat", "models", filename)
        with open(proto_export_path, "w") as file:
            file.write(proto_string)

