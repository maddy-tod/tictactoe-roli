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

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class BasicPlayer(tk.Frame):

    def __init__(self, parent, controller, **args):
        tk.Frame.__init__(self, parent, **args)
        self.controller = controller
        label = tk.Label(self, text="Basic Player", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.canvas = tk.Canvas(self, width=1100, heigh=600)

        x_offset = 300

        self.canvas.create_line(170 + x_offset, 0, 170 + x_offset, 510, fill='blue', width=8)
        self.canvas.create_line(340 + x_offset, 0, 340 + x_offset, 510, fill='blue', width=8)

        self.canvas.create_line(0 + x_offset, 170, 510 + x_offset, 170, fill='blue', width=8)
        self.canvas.create_line(0 + x_offset, 340, 510 + x_offset, 340, fill='blue', width=8)
        self.canvas.pack()
