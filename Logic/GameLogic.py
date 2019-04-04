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


class GameLogic:
    def __init__(self):
        print()

    def check_for_winner(self, board):

        # check rows
        for indx in [0, 3, 6]:
            if board[indx] and (board[indx] == board[indx+1] == board[indx+2]):
                return board[indx]

        # check columns
        for indx in [0, 1, 2]:
            if board[indx] and (board[indx] == board[indx + 3] == board[indx + 6]):
                return board[indx]

        # check diagonals
        if board[0] and (board[0] == board[4] == board[8]):
            return board[0]
        elif board[2] and (board[2] == board[4] == board[6]):
            return board[2]

        # 0 means a draw
        return -1 if any([x is None for x in board]) else 0
