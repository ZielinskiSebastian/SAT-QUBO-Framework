class ChoiSAT:
    """
    This class creates a QUBO model for 3SAT problems, according to Vicky Choi's paper:
    https://arxiv.org/pdf/1004.2226.pdf
    """

    def __init__(self, formula):
        self.formula = formula
        self.literals = [literal for clause in formula for literal in clause]
        self.num_variables = len(set([abs(literal) for clause in formula for literal in clause]))
        self.qubo = {}

    def create_qubo(self):
        for i in range(len(self.literals)):
            for j in range(len(self.literals)):
                if i > j:
                    continue
                # Main diagonal
                if i == j:
                    self.qubo[(i, j)] = -1
                # Triangle penalties
                elif j - i <= 2 and j//3 == i//3:
                    self.qubo[(i, j)] = 3
                # Punish contradictions
                elif abs(self.literals[i]) == abs(self.literals[j]) and self.literals[i] != self.literals[j]:
                    self.qubo[(i, j)] = 3

    # Checks how many clauses are satisfied - uses overwriting!
    # def is_answer(self, answer_dict):
    #     assignment = [0 for _ in range(self.num_variables)]
    #     for i in range(len(self.literals)):
    #         if answer_dict[i] == 1:
    #             if self.literals[i] < 0:
    #                 assignment[abs(self.literals[i]) - 1] = 0
    #             else:
    #                 assignment[abs(self.literals[i]) - 1] = 1
    #
    #     n = utils.check_solution(self.formula, assignment)
    #     if n < len(self.formula):
    #         return False, "unsat clause", n
    #     else:
    #         return True, "SAT", n

    # SAT / UNSAT only
    def is_answer2(self, answer_dict):
        true_indices = [literal_index for (literal_index, literal_value) in answer_dict.items() if literal_value == 1]
        true_variables = set([self.literals[i] for i in true_indices])

        # Check contradiction
        for variable in true_variables:
            if -variable in true_variables:
                return False, "contradiction"

        # Check satisfaction
        for clause in self.formula:
            clause_satisfied = False
            for literal in clause:
                if literal in true_variables:
                    clause_satisfied = True
                    break
            if not clause_satisfied:
                return False, "unsat clause"

        return True, "SAT"




    def export_qubo_to_file(self, filename):

        var_list = [i for i in range(0, 3 * len(self.formula))]
        max_length = 0
        for value in self.qubo.values():
            if len(str(value)) > max_length:
                max_length = len(str(value))
        with open(filename, "w") as file:
            for i in range(0, len(var_list)):
                line = ""
                for j in range(0, len(var_list)):
                    if j < i:
                        line += "0" + " " * (max_length - 1)
                    else:
                        if (i, j) in self.qubo:
                            line += str(self.qubo[(i, j)]) + " " * (max_length - len(str(self.qubo[(i, j)])))
                        else:
                            line += "0" + " " * (max_length - 1)

                    line += " "
                line += "\n"
                file.write(line)

