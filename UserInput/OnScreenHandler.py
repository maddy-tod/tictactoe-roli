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
import math
from UserInput.UserInputHandler import UserInputHandler
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# this just indicates that the on screen handler is being used
class OnScreenHandler(UserInputHandler):
    def __init__(self, controller):
        super().__init__(controller)

        self.controller.gui.bind("<Button-1>", self._click)
        self.controller.gui.bind("r", self.reset)

    def _click(self, event):
        """Triggered when mouse is clicked, if in range then draw cross"""

        # if not the users turn then return
        if self.controller.computers_turn:
            return

        # need to convert from mouse event to coord
        space_size = self.controller.gui.current_frame.space_size
        x_offset = self.controller.gui.current_frame.x_offset
        x_val = math.ceil((event.x - x_offset) / space_size) - 1
        y_val = math.ceil(event.y / space_size) - 1

        # Anything outside this range means it wasn't a click on the grid
        if 0 <= x_val <= 2 and 0 <= y_val <= 2:
            move = x_val + 3 * y_val
            self.controller.draw_x(int(move))
            self.controller.computer_take_turn()



