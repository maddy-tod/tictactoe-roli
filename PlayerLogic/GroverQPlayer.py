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
from qiskit.aqua import QuantumInstance
import random
from qiskit.aqua.algorithms import Grover
from qiskit.aqua.components.oracles import LogicalExpressionOracle
from qiskit import Aer
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class GroverQPlayer:
    def __init__(self):
        print("made a q player")
        self.move = 0

    def take_turn(self, board):
        """
        Args:
            board [int] : the current state of the board
        """
        with open('PlayerLogic/data/SATRules.cnf', 'r') as f:
            sat_cnf = f.read()

        print(board)
        opponent_moves = []

        for index, space in enumerate(board):
            # == 1 means opponent move
            if space == 1:
                # as spaces in sat start from 1
                opponent_moves.append(index + 1)

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

        sat_oracle = LogicalExpressionOracle(new_cnf)
        grover = Grover(sat_oracle)

        backend = Aer.get_backend('qasm_simulator')
        quantum_instance = QuantumInstance(backend, shots=100)
        result = grover.run(quantum_instance)
        print(result['result'])
        print(result)

        from qiskit.visualization import plot_histogram
        plot_histogram(result['measurements'], filename='classic.png')

        new_dict = {k: v for k, v in result['measurements'].items()if v > 1}

        counts_per_space = [0]*9

        for key, count in result['measurements'].items():
            for index, space in enumerate(key):
                # check this
                if space == '0':
                    counts_per_space[index] += count

        new_dict = {i: count for i, count in enumerate(counts_per_space)}

        print('--', result['measurements'])
        print('---', new_dict)
        plot_histogram(new_dict, filename='neww.png')

        # remove any moves which already have something in them, and filter to be the potential moves
        # which are indicated by being positive literals
        potential_moves = [x for x in result['result'] if x > 0 and not board[x-1]]

        if len(potential_moves) == 0:
            print("No move found! Choosing randomly")
            self.move = random.randint(1, 10)
        elif 5 in potential_moves:
            print("Taking the centre! Move ", 4)
            self.move = 5
        else :
            corner_moves = [x for x in potential_moves if x in [1, 3, 7, 9]]
            if corner_moves:
                print('Taking a corner! Choosing from ', corner_moves)
                self.move = random.choice(corner_moves)
            else:
                print('No special move, choosing from ', potential_moves)
                self.move = random.choice(potential_moves)

        # -1 as in SAT indices start from 1, but everywhere else they start from 0
        self.move -= 1
