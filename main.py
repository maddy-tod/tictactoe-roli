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
from BasicQPlayer import BasicQPlayer
from Logic.GameLogic import GameLogic

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

    def draw_x(self, index):
        self.gui.draw_x(index)
        self.board[index] = 1

    def draw_o(self, index):
        self.gui.draw_o(index)
        self.board[index] = 2

    def computers_turn(self):
        # check to see if the player has won
        self.winner = self.logic.check_for_winner(self.board)

        # no one has won and there are still spaces left
        if self.winner == -1 and any([x is None for x in self.board]):
            move = self.qcomputer.take_turn(self.board)
            print("computer is taking turn")
            self.draw_o(move)
            self.roli.send_move(move)

            # check to see if the computer has won
            self.winner = self.logic.check_for_winner(self.board)
            if self.winner != -1 :
                self.draw_result()
        else:
            # could be a draw or a winner
            self.draw_result()

    def draw_result(self):
        self.roli.send_winner(self.winner)

    def reset(self):
        self.board = [None] * 9
        self.qcomputer = BasicQPlayer()

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

