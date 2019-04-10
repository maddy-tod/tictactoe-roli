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


class BasePlayerGUI(tk.Frame):
    def __init__(self, parent, controller, labeltxt, **args):
        tk.Frame.__init__(self, parent, **args)
        self.controller = controller
        label = tk.Label(self, text=labeltxt, font=controller.title_font)
        label.pack(side="top", fill="x", pady=5)

        self.canvas = tk.Canvas(self, width=1100, height=600)
        self.canvas.pack()

    def draw_x(self, index):
        pass

    def draw_o(self, index):
        pass

    def moving_off(self):
        self.canvas.pack_forget()
        self.canvas.delete("all")
        self.canvas.pack()

    def pack(self):
        self.canvas.pack()

    def moving_to(self):
        self.draw_canvas()

    def draw_canvas(self):
        pass
