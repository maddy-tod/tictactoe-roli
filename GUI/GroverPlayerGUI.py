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
import tkinter as tk
from .BasePlayerGUI import BasePlayerGUI
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class GroverPlayerGUI(BasePlayerGUI):

    def __init__(self, parent, controller, **args):
        super().__init__(parent, controller, 'Grover Player', **args)

        self.canvas.pack()

    def draw_canvas(self):
        # Add buttons for the different modes
        self.result_button = tk.Button(self.canvas, text="Result",
                                       command=lambda: self.controller.show_result(),
                                       height=2, width=20)
        self.result_button.place(x=10, y=0)

        self.canvas.create_rectangle(10, 20, 50, 100, outline="")
        self.draw_grid()


