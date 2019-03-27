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
from RoliHandler import RoliBlockHandler
from qcomputer import QuantumPlayer

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class MainHandler:
    def __init__(self):
        self.roli = None
        self.gui = None
        self.board = [None]*9
        self.qcomputer = QuantumPlayer()

        self.winner = -1

    def draw_x(self, index):
        self.gui.draw_x(index)
        self.board[index] = 1

        self._check_for_winner()

    def draw_o(self, index):
        self.gui.draw_o(index)
        self.board[index] = 2

        self._check_for_winner()

    def computers_turn(self):
        move = self.qcomputer.take_turn(self.board)
        print("computer is taking turn")
        self.draw_o(move)
        self.roli.send_move(move)

    def _check_for_winner(self):

        # check rows
        for indx in [0, 3, 6]:
            if self.board[indx] and (self.board[indx] == self.board[indx+1] == self.board[indx+2]) :
                self.winner = self.board[indx]
                break

        # check columns
        for indx in [0, 1, 2]:
            if self.board[indx] and (self.board[indx] == self.board[indx + 3] == self.board[indx + 6]):
                self.winner = self.board[indx]
                break

        # check diagonals
        if self.board[0] and (self.board[0] == self.board[4] == self.board[8]):
            self.winner = self.board[0]
        elif self.board[2] and (self.board[2] == self.board[4] == self.board[6]):
            self.winner = self.board[2]

        if self.winner > 0:
            self.draw_winner()

    def draw_winner(self):
        print("yas you won!")
        self.roli.send_winner(self.winner)

    def reset(self):
        self.board = [None] * 9
        self.qcomputer = QuantumPlayer()

        self.winner = -1

        self.gui.reset()


if __name__ == "__main__":

    m = MainHandler()
    app = NoughtsAndCrossesApp(m)

    roli = RoliBlockHandler(m)

    m.roli = roli
    m.gui = app

    roli.run()
    app.mainloop()

