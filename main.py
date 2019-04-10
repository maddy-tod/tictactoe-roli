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
from GUI.MainGUI import NoughtsAndCrossesApp
from Roli.RoliHandler import RoliBlockHandler
from PlayerLogic.BasicQPlayer import BasicQPlayer
from PlayerLogic.GroverQPlayer import GroverQPlayer
from PlayerLogic.SVMQPlayer import SVMQPlayer
from GameLogic.GameLogic import GameLogic

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class MainHandler:
    def __init__(self):
        self.roli = None
        self.gui = None
        self.board = [None] * 9
        self.qcomputer = BasicQPlayer()
        self.winner = -1

        self.logic = GameLogic()
        self.computers_turn = False
        self.q_animating_frame = 0
        self.svm = SVMQPlayer()

    def draw_x(self, index):
        self.gui.draw_x(index)
        self.board[index] = 1

    def draw_o(self, index):
        self.gui.draw_o(index)
        self.board[index] = 2

    def computer_take_turn(self):
        # check to see if the player has won
        self.winner = self.logic.check_for_winner(self.board)
        if self.winner != -1:
            self.draw_result()

        self.computers_turn = True
        self.qcomputer.take_turn(self.board)

    def _show_computer_turn(self):

        # no one has won and there are still spaces left
        if self.winner == -1 and any([x is None for x in self.board]):
            move = self.qcomputer.move
            self.draw_o(move)
            self.roli.send_move(move)

            # check to see if the computer has won
            self.winner = self.logic.check_for_winner(self.board)
            if self.winner != -1:
                self.draw_result()

            self.computers_turn = False
        else:
            # could be a draw or a winner
            self.draw_result()

    def draw_result(self):
        self.roli.send_winner(self.winner)

        if self.winner == 1:
            winner = 'You'
        elif self.winner == 2:
            winner = 'The quantum computer'
        else :
            winner = 'No one'

        self.gui.set_winner(winner)


    def reset(self):
        self.board = [None] * 9
        self.qcomputer = BasicQPlayer()

        self.winner = -1

        self.gui.reset()

    def get_next_blochs(self):
        """Get the next bloch spheres to be shown in the animation"""
        if self.computers_turn:

            q_blochs = self.qcomputer.num_t_gates

            if self.q_animating_frame == 0:
                # reset all to pointing up
                blochs = [('', x) for x in range(0, 9)]
            elif self.q_animating_frame == 1:
                # move the ones which aren't possible moves
                blochs = [(-1, x) for x in range(0, 9) if q_blochs[x] == -1]

            elif self.q_animating_frame == 2:
                # H everyone
                # Bloch 0 at every index
                blochs = [(0, x) for x in range(0, 9) if q_blochs[x] != -1]

            else:
                # first three frames are taken by setup
                qubit = self.q_animating_frame - 3

                while qubit < len(q_blochs) - 1 and q_blochs[qubit] <= 0:
                    qubit += 1

                # at the end
                if qubit > 8:
                    print('I would be showing the other bloch spheres here if I could')
                    self._show_computer_turn()

                    # reset
                    self.computers_turn = False
                    self.q_animating_frame = 0
                    return []

                blochs = [(q_blochs[qubit], qubit)]

            self.q_animating_frame += 1
            return blochs

    def get_final_blochs(self):
        """Get the final Bloch sphere states"""
        if self.computers_turn:

            q_blochs = self.qcomputer.num_t_gates

            blochs = [(q_blochs[x], x) for x in range(0, 9)]
            return blochs

    def show_result(self):
        """Show the computers turn"""
        if self.computers_turn:
            self._show_computer_turn()
            # reset
            self.computers_turn = False
            self.q_animating_frame = 0

    def change_computer(self, computer_name):

        # Has GUI at the end as its the name of the frame
        if computer_name == "BasicPlayerGUI":
            self.qcomputer = BasicQPlayer()
        elif computer_name == "GroverPlayerGUI":
            self.qcomputer = GroverQPlayer()
        elif computer_name == "SVMPlayerGUI":

            # stop havign to retrain SVM
            if not self.svm :
                self.svm = SVMQPlayer()

            self.qcomputer = self.svm

        #TODO reset the Roli too

    def get_svm_counts(self, size):
        if self.computers_turn:
            return self.qcomputer.get_data_view(self.board, size)
        return None


if __name__ == "__main__":

    m = MainHandler()
    app = NoughtsAndCrossesApp(m)

    roli = RoliBlockHandler(m)

    m.roli = roli
    m.gui = app

    roli.run()
    app.mainloop()

