import numpy as np
from pysat.solvers import Glucose4
import os
import multiprocessing as mp
from multiprocessing import Pool
import functools


def create_solvable_formulas(num_variables, num_clauses, type, amount, output_directory):

    mp.set_start_method("spawn")
    with Pool(8, maxtasksperchild=10) as p:
        worker_partial = functools.partial(worker, num_variables=num_variables, num_clauses=num_clauses, type=type, output_directory=output_directory)
        p.map(worker_partial, list(range(0, amount)))


def worker(index, num_variables, num_clauses, type, output_directory):

    formula = []

    if type == "random":
        formula = create_random_uniform_formula(num_variables, num_clauses)

        while not is_satisfiable(formula):
            formula = create_random_uniform_formula(num_variables, num_clauses)


    export_formula_to_dimacs(formula, os.path.join(output_directory, str(index) + ".dimacs"))




def is_satisfiable(formula):
    with Glucose4(bootstrap_with=formula, use_timer=True) as solver:

        if solver.solve():
            stats = solver.accum_stats()

            print("SAT")
            print('Solution:', solver.get_model())
            print("TIME: ", solver.time_accum())
            print("Stats: ", stats)

            return True

def create_random_uniform_formula(num_vars, num_clauses):
    formula = []
    while len(formula) < num_clauses:
        clause_vars = np.random.choice(range(1, num_vars+1), size=3, replace=False)
        signs = np.random.choice([-1, +1], size=3, replace=True)
        # convert numpy integers -> python 'int': python sat solvers cannot handle numpy integers
        formula.append([x.item() for x in clause_vars * signs])

    return formula







# ---------------------------------- Helpers ---------------------------------- #

def export_formula_to_dimacs(sat_formula, file_path):
    num_clauses = len(sat_formula)
    num_vars = len(set([abs(literal) for clause in sat_formula for literal in clause]))

    with open(file_path, "w") as sat_file:
        sat_file.write("p cnf {vars} {clauses} \n".format(vars=num_vars, clauses=num_clauses))
        for clause in sat_formula:
            for literal in clause:
                sat_file.write(str(literal) + " ")
            sat_file.write("0\n")

def load_formula_from_dimacs_file(file_path):
    formula = []
    with open(file_path, "r") as file:
        for line in file:
            # discard first dimacs line
            if not line.startswith("p"):
                # discard dimacs 0 at the end of each line ([:-1])
                formula.append(list(map(lambda x: int(x), line.split(" ")))[:-1])
    return formula
