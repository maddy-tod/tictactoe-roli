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

    #TODO these methods need to check if winner
    def draw_x(self, index):
        self.gui.draw_x(index)
        self.board[index] = 1

    def draw_o(self, index):
        self.gui.draw_o(index)
        self.board[index] = 2

    def computers_turn(self):
        move = self.qcomputer.take_turn(self.board)
        print("computer is taking turn")
        self.draw_o(move)
        self.roli.send_move(move)


if __name__ == "__main__":

    m = MainHandler()
    app = NoughtsAndCrossesApp(m)

    roli = RoliBlockHandler(m)

    m.roli = roli
    m.gui = app

    roli.run()
    app.mainloop()

