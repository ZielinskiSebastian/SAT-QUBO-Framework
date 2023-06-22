import pathlib

import numpy as np
import multiprocessing as mp
from multiprocessing import Pool
import functools
import os
import pickle

# ---------------------- n+m QUBOS speziell  ---------------------- #

def find_all_mn_pattern_qubos(from_value, to_value, qubo_size):

    pattern_qubos = {}
    for i in range(0, 4):
        results = find_mn_qubos(from_value, to_value, qubo_size, i)
        pattern_qubos[i] = list(results)
        save_pattern_qubos(from_value, to_value, qubo_size, list(results), i)
        print("clause type ", i, " done")


def find_mn_qubos(from_value, to_value, qubo_size, clause_type):
    found_qubos = prepare_qubos(from_value, to_value, qubo_size)

    results = mp.Manager().list()

    with Pool(8) as p:
        worker_partial = functools.partial(test_mn_qubos, clause_type=clause_type, results=results)
        p.map(worker_partial, found_qubos)

    return results


def test_mn_qubos(qubo, clause_type, results):

    solutions_by_number = test_qubo(qubo, num_vars=3, num_ancillas=1, num_correct_assignments=7)

    if solutions_by_number is None:
        return
    if clause_type == 0:
        if solutions_by_number[0] > solutions_by_number[5]:
            results.append(create_qubo(qubo, 4))
    elif clause_type == 1:
        if solutions_by_number[1] > solutions_by_number[5]:
            results.append(create_qubo(qubo, 4))
    elif clause_type == 2:
        if solutions_by_number[3] > solutions_by_number[5]:
            results.append(create_qubo(qubo, 4))
            return True
    elif clause_type == 3:
        if solutions_by_number[7] > solutions_by_number[5]:
            results.append(create_qubo(qubo, 4))
            return True


# ---------------------- Allgemeine Funktionen ---------------------- #


def test_qubo(qubo, num_vars=3, num_ancillas=0, num_correct_assignments=6):
    solutions = {}
    solutions_by_number = {}

    for solution in range(0, 2**num_vars):
        tmp_solutions = []
        for i in range(2**num_ancillas):
            part_1 = "{0:0" + str(num_vars) + "b}"
            part_2 = "{0:0" + str(num_ancillas) + "b}"
            sample_string = part_1.format(solution) + part_2.format(i)
            sample = [int(j) for j in sample_string]

            tmp_solutions.append(qubo_energy(qubo, sample))

        solutions_by_number[solution] = min(tmp_solutions)

        if min(tmp_solutions) in solutions:
            solutions[min(tmp_solutions)] += 1
        else:
            solutions[min(tmp_solutions)] = 1

    results = list(solutions.items())
    results.sort(key=lambda x: x[0])

    if results[0][1] == num_correct_assignments:
        return solutions_by_number


def qubo_energy(qubo, sample):
    energy = 0
    idx = 0
    for i in range(len(sample)):
        for j in range(i, len(sample)):
            energy += qubo[idx] * sample[i] * sample[j]
            idx += 1
    return energy


def prepare_qubos(from_value, to_value, qubo_size):
    found_qubos = []
    qubo = np.zeros(qubo_size) + from_value

    search_done = False

    while not search_done:
        found_qubos.append(qubo.copy())
        qubo[0] += 1
        for i in range(qubo_size):
            if qubo[i] == to_value + 1:
                if i == qubo_size - 1:
                    search_done = True
                else:
                    qubo[i] = from_value
                    qubo[i+1] = qubo[i+1] + 1
    return found_qubos


def save_pattern_qubos(from_value, to_value, qubo_size, pattern_qubos, clause_type):
    save_dir = os.path.join(os.getcwd(), "pattern_qubos", str(from_value)+"_"+str(to_value)+"_"+str(qubo_size))

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    save_path = os.path.join(save_dir, "clause_type_" + str(clause_type)) + ".pkl"
    with open(save_path, "wb") as file:
        pickle.dump(pattern_qubos, file)


def load_pattern_qubos(from_value, to_value, qubo_size, clause_type):
    load_dir = os.path.join(os.getcwd(), "pattern_qubos",  str(from_value) + "_" + str(to_value) + "_" + str(qubo_size))

    file_path = os.path.join(load_dir, "clause_type_" + str(clause_type) + ".pkl")

    with open(file_path, "rb") as file:
        return pickle.load(file)


def load_all_pattern_qubos(from_value, to_value, qubo_size):
    results = {}

    for i in range(4):
        pattern_qubos = load_pattern_qubos(from_value, to_value, qubo_size, i)
        results[i] = pattern_qubos

    return results


def create_qubo(qubo, size):
    qubo_dict = {}
    idx = 0
    for i in range(size):
        for j in range(i, size):
            qubo_dict[(i, j)] = qubo[idx]
            idx += 1
    return qubo_dict
