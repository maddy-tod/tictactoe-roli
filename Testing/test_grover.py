# -*- coding: utf-8 -*-

# Copyright 2019 IBM.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
import logging

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


import pylab
import numpy as np
from qiskit import LegacySimulators
from qiskit.tools.visualization import plot_histogram
from qiskit_aqua import QuantumInstance
from qiskit_aqua import run_algorithm
from qiskit_aqua.algorithms import Grover
from qiskit_aqua.components.oracles import SAT
from qiskit import Aer


with open('SATRules.cnf', 'r') as f:
    sat_cnf = f.read()


board = [0]*9
board[0] = 1

opponent_moves = []

for index, space in enumerate(board):
    if space == 1:
        # as spaces in sat start from 1
        opponent_moves.append(index+1)


new_sat_lines = []
for move in opponent_moves:
    line = '-' + str(move) + ' 0'
    new_sat_lines.append(line)

cnf = sat_cnf.split('\n')

new_cnf = ''
for line in cnf:
    if line.startswith('p'):
        # 8 is the size of the base rule set
        new_cnf = new_cnf + 'p cnf 9 ' + str(len(new_sat_lines) + 8) + '\n'
    else:
        # copy over comments or actual sat lines
        new_cnf = new_cnf + line + '\n'
for line in new_sat_lines:
    new_cnf = new_cnf + line + '\n'

print(new_cnf)

sat_oracle = SAT(new_cnf)
grover = Grover(sat_oracle)

backend = Aer.get_backend('qasm_simulator')
quantum_instance = QuantumInstance(backend, shots=100)
result = grover.run(quantum_instance)
print(result['result'])

# potential moves are > 0 results
potential_moves = [x for x in result['result'] if x > 0]
if len(potential_moves) == 0:
    print("No move found! Choosing randomly")
elif 5 in potential_moves:
    print("Taking the centre! Move ", 4)
elif [x for x in potential_moves if x in [1,3,7,9]]:
    print('Taking a corner! Choosing from ', [x for x in potential_moves if x in [1,3,7,9]])
else :
    print('No special move, choosing from ', potential_moves)

