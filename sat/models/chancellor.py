import numpy as np
from sat.models.SATNMBase import SATBase


class ChancellorSAT(SATBase):
    """
    This class creates a QUBO model for 3SAT problems, according to the special case (page 5)
    in Nick Chancellors's paper: https://www.nature.com/articles/srep37107.pdf.

    Idea: (x or y or z) = x + y + z -xy -xz -yz + xyz
    --> 0 0 0 has value 0
    --> else: has value 1
    --> maximization -> transform to minimization

    _(1)_ minimize: -x - y - z +xy +xz +yz - xyz
    --> 0 0 0 has value 0
    --> else: has value -1

    Use: x -> 0.5(x_spin + 1) where x_spin in {-1,1} -> x_spin = -1 -> x = 0, x_spin = 1 -> x = 1
    in _(1)_ = -1/8x -1/8y -1/8z +1/8xy +1/8xz +1/8yz -1/8xyz (-7/8)
    ---> -1 -1 -1 has value 0
    ---> else: has value -1

    _(2)_ multiply 1 by 8: -x -y -z +xy +xz +yz -xyz -7 (still spins {-1,1} not binary {0,1})!

    --- XOR TERM: xyz ---

    x_spin*y_spin*z_spin is a parity checking term. -- c(x) = sign(x)
    --> create hamiltonian: -xyz = g/2 * c(x)x_spin * c(y)y_spin * c(z)z_spin
    --> h = g = 1, J_a = 2J > |h| --> choose J=h=1 -> J_a = 2, h_a = 2h --> 2
    !!! choose h=J=1 to create qubos with the least amount of couplers
    Ising vector h:
    [1, 1, 1, 2]

    Ising matrix J:
    --- a -- b -- c -- K
     a  - -- 1 -- 1 -- 2
     b  - -- - -- 1 -- 2
     c  - -- - -- - -- 2
     K  - -- - -- - -- -

    To test:

    h = {0: 1, 1: 1, 2: 1, 3: 2}
    J = {(0, 1): 1, (0, 2): 1, (0, 3): 2, (1, 2): 1, (1, 3): 2, (2, 3): 2}
    ---
    Minimization Hamiltonians:

   -----------------------------------
    a or b or c: -1/8a -1/8b -1/8c +1/8ab +1/8ac +1/8bc -1/8abc -7/8 --> h = -1 (because the triple term is -abc)

    Ising vector h:
    [-2, -2, -2, -2]

    Ising matrix J:
    --- a -- b -- c -- K
     a  - -- 2 -- 2 -- 2
     b  - -- - -- 2 -- 2
     c  - -- - -- - -- 2
     K  - -- - -- - -- -

    To test:

    # h = {0: -2,  1: -2, 2: -2, 3: -2}
    # J = {(0, 1): 2, (0, 2): 2, (1, 2): 2, (1, 3): 2, (2, 3): 2,  (0, 3): 2}
    -----------------------------------


    a or b or -c: -1/8a -1/8b +1/8c +1/8ab - 1/8ac -1/8bc +1/8abc -7/8 --> h = +1 (because the triple term is +abc)


    c + ab -bc -ac -ab(1-c)

    Ising vector h:
    [0, 0, 2, 2]

    Ising matrix J:
    --- a -- b -- c -- K
     a  - -- 2 -- 0 -- 2
     b  - -- - -- 0 -- 2
     c  - -- - -- - -- 2
     K  - -- - -- - -- -

    To test:
    # h = {0: 0,  1: 0, 2: 2, 3: 2}
    # J = {(0, 1): 2, (0, 2): 0, (1, 2): 0, (1, 3): 2, (2, 3): 2,  (0, 3): 2}
    -----------------------------------

    a or -b or -c: -1/8a + 1/8b +1/8c -1/8ab -1/8ac +1/8bc -1/8abc -7/8 --> h = -1 (because the triple term is -abc)


    Ising vector h:
    [-2, 0, 0, -2]

    Ising matrix J:
    --- a -- b -- c -- K
     a  - -- 0 -- 0 -- 2
     b  - -- - -- 2 -- 2
     c  - -- - -- - -- 2
     K  - -- - -- - -- -

    To test:
    # h = {0: -2,  1: 0, 2: 0, 3: -2}
    # J = {(0, 1): 0, (0, 2): 0, (1, 2): 2, (1, 3): 2, (2, 3): 2,  (0, 3): 2}
    -----------------------------------
    -a or -b or -c: 1/8a +1/8b +1/8c +1/8ab +1/8ac +1/8bc +1/8abc +7/8 --> h = +1 (because the triple term is +abc)




    Ising vector h:
    [2, 2, 2, 2]

    Ising matrix J:
    --- a -- b -- c -- K
     a  - -- 2 -- 2 -- 2
     b  - -- - -- 2 -- 2
     c  - -- - -- - -- 2
     K  - -- - -- - -- -


    # h = {0: 2, 1: 2, 2: 2, 3: 2}
    # J = {(0, 1): 2, (0, 2): 2,  (1, 2): 2, (1, 3): 2, (2, 3): 2, (0, 3): 2}
    """

    def __init__(self, formula):
        super().__init__(formula)

    def create_qubo(self):
        for clause_index, clause in enumerate(self.formula):
            if list(np.sign(clause)) == [1, 1, 1]:
                self.add(clause[0], clause[0], -2)
                self.add(clause[1], clause[1], -2)
                self.add(clause[2], clause[2], -2)
                self.add(self.num_variables + clause_index + 1, self.num_variables + clause_index + 1, -2)

                self.add(clause[0], clause[1], 1)
                self.add(clause[0], clause[2], 1)
                self.add(clause[0], self.num_variables + clause_index + 1, 1)

                self.add(clause[1], clause[2], 1)
                self.add(clause[1], self.num_variables + clause_index + 1, 1)

                self.add(clause[2], self.num_variables + clause_index + 1, 1)

            elif list(np.sign(clause)) == [1, 1, -1]:
                self.add(clause[0], clause[0], -1)
                self.add(clause[1], clause[1], -1)
                self.add(clause[2], clause[2], 0)
                self.add(self.num_variables + clause_index + 1, self.num_variables + clause_index + 1, -1)

                self.add(clause[0], clause[1], 1)
                self.add(clause[0], clause[2], 0)
                self.add(clause[0], self.num_variables + clause_index + 1, 1)

                self.add(clause[1], clause[2], 0)
                self.add(clause[1], self.num_variables + clause_index + 1, 1)

                self.add(clause[2], self.num_variables + clause_index + 1, 1)

            elif list(np.sign(clause)) == [1, -1, -1]:
                self.add(clause[0], clause[0], -1)
                self.add(clause[1], clause[1], -1)
                self.add(clause[2], clause[2], -1)
                self.add(self.num_variables + clause_index + 1, self.num_variables + clause_index + 1, -2)

                self.add(clause[0], clause[1], 0)
                self.add(clause[0], clause[2], 0)
                self.add(clause[0], self.num_variables + clause_index + 1, 1)

                self.add(clause[1], clause[2], 1)
                self.add(clause[1], self.num_variables + clause_index + 1, 1)

                self.add(clause[2], self.num_variables + clause_index + 1, 1)

            else:
                self.add(clause[0], clause[0], -1)
                self.add(clause[1], clause[1], -1)
                self.add(clause[2], clause[2], -1)
                self.add(self.num_variables + clause_index + 1, self.num_variables + clause_index + 1, -1)

                self.add(clause[0], clause[1], 1)
                self.add(clause[0], clause[2], 1)
                self.add(clause[0], self.num_variables + clause_index + 1, 1)

                self.add(clause[1], clause[2], 1)
                self.add(clause[1], self.num_variables + clause_index + 1, 1)

                self.add(clause[2], self.num_variables + clause_index + 1, 1)




