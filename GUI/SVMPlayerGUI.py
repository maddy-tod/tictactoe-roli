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
from PIL import Image, ImageTk
from .BasePlayerGUI import BasePlayerGUI

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class SVMPlayerGUI(BasePlayerGUI):

    def __init__(self, parent, controller, **args):
        super().__init__(parent, controller, 'SVM Player', **args)

        self.potenial_moves_canvas_imgs = []
        self.potenial_moves_actual_imgs = []

        self.draw_canvas()

    def load_faded_image(self, file, alpha):
        img = Image.open(file)

        # resize to be the same size as the space
        img = img.resize((self.space_size - 5, self.space_size - 5), Image.ANTIALIAS)

        # make it fade
        img.putalpha(alpha)
        return ImageTk.PhotoImage(img)

    def reset(self):
        self.plays = []

        self.reset_potential_moves()
        self.canvas.itemconfigure(self.state_label, text="Player's turn!")

    def draw_potential_move(self, index, intensity=1):

        # scale the parameter out of 256
        alpha = int(intensity * 256)
        move_img = self.load_faded_image('GUI/imgs/players/potential_o.png', alpha)

        x = index % 3
        y = int(index / 3)
        img = self.canvas.create_image(((2 + self.x_offset + x * self.space_size), 2 + self.space_size * y),
                                       image=move_img,
                                       anchor=tk.NW)

        self.potenial_moves_actual_imgs.append(move_img)
        self.potenial_moves_canvas_imgs.append(img)

    def reset_potential_moves(self):
        for mv in self.potenial_moves_canvas_imgs:
            self.canvas.delete(mv)

        self.potenial_moves_canvas_imgs = []
        self.potenial_moves_actual_imgs = []

    def draw_canvas(self):

        # Add buttons for the different modes
        self.quantum_button = tk.Button(self.canvas, text="Show quantum view",
                                        command=lambda: self.controller.show_q_view(),
                                        height=2, width=20)
        self.quantum_button.place(x=10, y=0)
        self.classical_button = tk.Button(self.canvas, text="Show classical view",
                                          command=lambda: self.controller.show_c_view(),
                                          height=2, width=20)
        self.classical_button.place(x=10, y=50)
        self.result_button = tk.Button(self.canvas, text="Result",
                                       command=lambda: self.controller.show_result(),
                                       height=2, width=20)
        self.result_button.place(x=10, y=100)

        self.draw_grid()


