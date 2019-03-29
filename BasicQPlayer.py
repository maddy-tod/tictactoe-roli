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
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class BasicQPlayer:
    def __init__(self):
        print("made a q player")

    def take_turn(self, board):
        """
        Args:
            board [int] : the current state of the board
        Returns:
            int : the index of the move to be made
        """

        # TODO would it be better to only map to qubits that could be moves
        # However this would mean lots of index/physical qubit number swaps

        num_qubits = 9
        q = QuantumRegister(num_qubits)
        c = ClassicalRegister(num_qubits)
        qc = QuantumCircuit(q, c)

        # make the option definitely a 1 if there is a move in the space already
        for index, move in enumerate(board):
            if move:
                qc.x(q[index])
                print('MY BOY X on qubit', index)
            else :
                # this space is a potential move
                # so put into a superposition
                qc.h(q[index])

                t_count = 0

                # so it is the start of a row
                if index % 3 == 0:

                    # two pieces in a row - need to block/win
                    if board[index + 1] and board[index + 2] and board[index + 1] == board[index + 2] :
                        qc.t(q[index])
                        qc.t(q[index])
                        t_count += 2
                    # one of the spaces is empty so go there
                    elif board[index + 1] != board[index + 2]:
                        qc.t(q[index])
                        t_count += 1

                # so it is the middle of a row
                if index % 3 == 1:

                    # two pieces in a row - need to block/win
                    if board[index + 1] and board[index - 1] and board[index + 1] == board[index - 1] :
                        qc.t(q[index])
                        qc.t(q[index])
                        t_count += 2
                    elif board[index + 1] != board[index - 1]:
                        qc.t(q[index])
                        t_count += 1

                # so it is the end of a row
                if index % 3 == 2:
                    # two pieces in a row - need to block/win
                    if board[index - 1] and board[index - 2] and board[index - 1] == board[index - 2]:
                        qc.t(q[index])
                        qc.t(q[index])
                        t_count += 2
                    elif board[index - 1] != board[index - 2]:
                        qc.t(q[index])
                        t_count += 1

                # so is the top row
                if index / 3 < 1:
                    if board[index + 3] and board[index - 6] and board[index - 3] == board[index - 3]:
                        qc.t(q[index])
                        qc.t(q[index])
                        t_count += 2
                    elif board[index + 3] != board[index - 6]:
                        qc.t(q[index])
                        t_count += 1

                # so it is the middle row
                if 2 > index / 3 >= 1:
                    if board[index - 3] and board[index + 3] and board[index - 3] == board[index + 3]:
                        qc.t(q[index])
                        qc.t(q[index])
                        t_count += 2
                    elif board[index - 3] != board[index + 3]:
                        qc.t(q[index])
                        t_count += 1

                # so it is the top row
                if index / 3 >= 2:
                    if board[index - 3] and board[index - 6] and board[index - 3] == board[index - 6]:
                        qc.t(q[index])
                        qc.t(q[index])
                        t_count += 2
                    elif board[index - 3] != board[index - 6]:
                        qc.t(q[index])
                        t_count += 1

                print("applied ", t_count,  " t gates to ", index)

        # hard code in the diagonals
        if board[0] and board[0] == board[4]:
            qc.t(q[8])
            qc.t(q[8])
            qc.t(q[8])
            print('extra t gate for 8')
        if board[0] and board[0] == board[8]:
            qc.t(q[4])
            qc.t(q[4])
            qc.t(q[4])
            print('extra t gate for 4')
        if board[4] and board[4] == board[8]:
            qc.t(q[0])
            qc.t(q[0])
            qc.t(q[0])
            print('extra t gate for 0')
        if board[2] and board[2] == board[4]:
            qc.t(q[6])
            qc.t(q[6])
            qc.t(q[6])
            print('extra t gate for 6')
        if board[2] and board[2] == board[6]:
            qc.t(q[4])
            qc.t(q[4])
            qc.t(q[4])
            print('extra t gate for 4')
        if board[4] and board[4] == board[6]:
            qc.t(q[2])
            qc.t(q[2])
            qc.t(q[2])
            print('extra t gate for 2')

        for index, move in enumerate(board):
            if not move:
                qc.h(q[index])
        qc.measure(q, c)

        backend = Aer.get_backend('qasm_simulator')
        shots = 100
        job_sim = execute(qc, backend, shots=shots)
        sim_result = job_sim.result().get_counts(qc)

        counts = [0]*num_qubits

        for key, count in sim_result.items():
            # need to iterate over the results and see when the value was chosen most

            #keys are the opposite way round to expected
            key = key[::-1]
            print(key, " : ", count)
            for index, val in enumerate(key):
                if val == '1':
                    counts[index] += count


        for i, c in enumerate(counts):
            print(i, " - ", c, ' occupied? ', board[i])

        max_count = 0
        max_index = 0
        for index, count in enumerate(counts):
            if not board[index] and count > max_count:
                max_index = index
                max_count = count

        print("move : ",max_index)
        return max_index