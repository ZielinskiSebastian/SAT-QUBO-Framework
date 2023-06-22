from sat.models.prototypes.nmprototypesat import NMPrototypeSAT
from sat.qubosearcher import *
from sat.formula_creator import *
import os
from sat.models.choi import ChoiSAT
from sat.models.chancellor import ChancellorSAT
from sat.models.nuesslein import NuessleinNM


# --- Load a formula ---
formula = load_formula_from_dimacs_file(os.path.join(os.getcwd(), "formulas", "0.dimacs"))
print(formula)

# --- Choi Transformation ---
formula = load_formula_from_dimacs_file(os.path.join(os.getcwd(), "formulas", "0.dimacs"))
choi_sat = ChoiSAT(formula)
choi_sat.create_qubo()
print(choi_sat.qubo)

# --- Chancellor Transformation ---
formula = load_formula_from_dimacs_file(os.path.join(os.getcwd(), "formulas", "0.dimacs"))
chancellor_sat = ChancellorSAT(formula)
chancellor_sat.create_qubo()
print(chancellor_sat.qubo)

# --- Nuesslein Transformation ---
formula = load_formula_from_dimacs_file(os.path.join(os.getcwd(), "formulas", "0.dimacs"))
nuesslein_sat = NuessleinNM(formula)
nuesslein_sat.create_qubo()
print(nuesslein_sat.qubo)

# --- Search all pattern QUBOs - min -1, max 1, step 1  (see https://arxiv.org/pdf/2305.02659.pdf) ---
# Care: exhaustive search - running time grows exponentially with size of value range
find_all_mn_pattern_qubos(-1, 1, 10)
found_pattern_qubos = load_all_pattern_qubos(-1, 1, 10)

# --- Build concrete QUBO-transformation from pattern qubos ---
formula = load_formula_from_dimacs_file(os.path.join(os.getcwd(), "formulas", "0.dimacs"))

find_all_mn_pattern_qubos(-1, 1, 10)

# Structure of found_pattern_qubos:
# found_pattern_qubos[0] is a list of all found pattern qubos for clause type 0
# found_pattern_qubos[1] is a list of all found pattern qubos for clause type 1
# ....

found_pattern_qubos = load_all_pattern_qubos(-1, 1, 10)

sat_transformation = NMPrototypeSAT(formula)
sat_transformation.add_clause_qubos(found_pattern_qubos[0][0], found_pattern_qubos[1][0],
                                    found_pattern_qubos[2][0], found_pattern_qubos[3][0])
sat_transformation.create_qubo()
print(sat_transformation.qubo)

# Additionally: Export this transformation to a standalone python file
sat_transformation.export_prototype("NewTransformation.py")

