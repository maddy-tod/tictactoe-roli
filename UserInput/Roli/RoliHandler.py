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
import pygame
from pygame.midi import time
from UserInput.UserInputHandler import UserInputHandler

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class RoliBlockHandler(UserInputHandler):

    def __init__(self, controller):
        super().__init__(controller)
        pygame.init()
        pygame.midi.init()

        logger.info("Looking for devices")
        for i in range(4):
            logger.info(str(i) + " : " + str(pygame.midi.get_device_info(i)))

        input_id = 1
        logger.info("using input_id : %s" % input_id)
        self.midi_input = pygame.midi.Input(input_id)

        # sending midi to the output
        output_id = 3
        logger.info("using output_id : %s" % output_id)
        self.midi_output = pygame.midi.Output(output_id)

        # clear the display
        self.midi_output.write([[[0xc0, 0, 0], 0]])

    def run(self):

        if self.midi_input.poll():
            midi_events = self.midi_input.read(10)

            for event in midi_events:
                # event is [[status,data1,data2,data3],timestamp]
                data = event[0]

                # 0xa0 means a move has been made
                if data[0] == 0xa0:
                    # data[1] contains the index 0-9
                    self.controller.draw_x(data[1])
                    self.controller.computer_take_turn()

                # 0xcc means the button has been pressed - start again
                if data[0] == 0xcc:
                    self.reset()

        self.controller.gui.after(100, self.run)

    def send_move(self, move):
        self.midi_output.write([[[0xa0, move, 0], 0]])

    def send_winner(self, winner):
        self.midi_output.write([[[0xb0, winner, 0], 0]])





