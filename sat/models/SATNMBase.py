import numpy as np


class SATBase:

    def __init__(self, formula):
        self.formula = [sorted(clause, reverse=True) for clause in formula]
        self.num_variables = len(set([abs(literal) for clause in formula for literal in clause]))
        self.qubo = {}


    def add(self, x, y, value):

        # Dimacs - SAT variables start at 1, QUBO variables start at 0
        x = np.abs(x) - 1
        y = np.abs(y) - 1
        if x > y:
            x, y = y, x
        if (x, y) in self.qubo.keys():
            self.qubo[(x, y)] += value
        else:
            self.qubo[(x, y)] = value

    def is_answer(self, answer_dict):
        assignment = [answer_dict[i] for i in range(self.num_variables)]

        sat_clauses = self.check_solution(assignment)
        if sat_clauses < len(self.formula):
            return False, "unsat clause", sat_clauses
        else:
            return True, "SAT", sat_clauses

    def check_solution(self, assignment):
        satisfied_clauses = 0
        for clause in self.formula:
            for literal in clause:
                if literal < 0 and assignment[abs(literal) - 1] == 0:
                    satisfied_clauses += 1
                    break
                elif literal > 0 and assignment[abs(literal) - 1] == 1:
                    satisfied_clauses += 1
                    break
        return satisfied_clauses

    def printQUBO(self):
        num_qubo_variables = self.num_variables + len(self.formula)

        for row in range(num_qubo_variables):
            for column in range(num_qubo_variables):
                if row > column:
                    print("      ", end='')
                    continue
                printing = ""
                if (row, column) in self.qubo.keys() and self.qubo[(row, column)] != 0:
                    printing = str(self.qubo[(row, column)])
                printing += "_____"
                printing = printing[:5]
                printing += " "
                print(printing, end='')
            print("")
