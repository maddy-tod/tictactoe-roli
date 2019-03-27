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
from qiskit.tools.visualization import plot_bloch_vector
from PIL import Image
from PIL import ImageTk

from .BasePlayer import BasePlayer

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class BasicPlayer(BasePlayer):

    def __init__(self, parent, controller, **args):
        tk.Frame.__init__(self, parent, **args)
        self.controller = controller
        label = tk.Label(self, text="Basic Player", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.canvas = tk.Canvas(self, width=1100, heigh=600)

        self.x_offset = 300
        self.space_size = 170

        # if we wanted to re draw the images
        # self.gen_images()

        # Allows for a bit of padding
        temp_x_offset = self.x_offset + 10
        # load the starting image
        self.starting_img = self.load_bloch_image('GUI/imgs/starting/tl.png')

        # add this image into all the grid spaces
        self.bloch_tl = self.canvas.create_image((temp_x_offset, 0), image=self.starting_img, anchor=tk.NW, tag='tl')
        self.bloch_tm = self.canvas.create_image((self.space_size + temp_x_offset, 0), image=self.starting_img, anchor=tk.NW, tag='tm')
        self.bloch_tr = self.canvas.create_image((self.space_size*2 + temp_x_offset, 0), image=self.starting_img, anchor=tk.NW, tag='tr')

        self.bloch_ml = self.canvas.create_image((temp_x_offset, self.space_size), image=self.starting_img, anchor=tk.NW, tag='ml')
        self.bloch_mm = self.canvas.create_image((self.space_size + temp_x_offset, self.space_size), image=self.starting_img, anchor=tk.NW, tag='mm')
        self.bloch_mr = self.canvas.create_image((self.space_size*2 + temp_x_offset, self.space_size), image=self.starting_img, anchor=tk.NW, tag='mr')

        self.bloch_bl = self.canvas.create_image((temp_x_offset, self.space_size*2), image=self.starting_img, anchor=tk.NW, tag='bl')
        self.bloch_bm = self.canvas.create_image((self.space_size + temp_x_offset, self.space_size*2), image=self.starting_img, anchor=tk.NW, tag='bm')
        self.bloch_br = self.canvas.create_image((self.space_size*2 + temp_x_offset, self.space_size*2), image=self.starting_img, anchor=tk.NW, tag='br')

        # Draw lines of the TicTacToe grid
        x1 = self.space_size + self.x_offset
        x2 = self.space_size*2 + self.x_offset
        self.canvas.create_line(x1, 0, x1, self.space_size*3, fill='black', width=6)
        self.canvas.create_line(x2, 0, x2, self.space_size*3, fill='black', width=6)

        self.canvas.create_line(self.x_offset, self.space_size, self.space_size*3 + self.x_offset, self.space_size, fill='black', width=6)
        self.canvas.create_line(self.x_offset, self.space_size*2, self.space_size*3 + self.x_offset, self.space_size*2, fill='black', width=6)
        self.canvas.pack()

        # stored the noughts and crosses images that have been played
        self.plays = []
        self.nought = self.load_other_image('GUI/imgs/players/o.png')
        self.cross = self.load_other_image('GUI/imgs/players/x.png')

    def load_bloch_image(self, file):
        img = Image.open(file)
        print(img.size)
        img = img.crop((50, 0, 480, 475))
        w, h = img.size
        img = img.resize((int(w * 0.35), int(h * 0.35)), Image.ANTIALIAS)
        return ImageTk.PhotoImage(img)

    def load_other_image(self, file):
        img = Image.open(file)
        img = img.resize((self.space_size, self.space_size), Image.ANTIALIAS)
        return ImageTk.PhotoImage(img)

    def gen_images(self):
        locations = ['tl', 'tm', 'tr',
                     'ml', 'mm', 'mr',
                     'bl', 'bm', 'br']

        for loc in locations:
            x = plot_bloch_vector([0, 0, 1])
            x.savefig('/Users/madeleinetod/Documents/NoughtsAndCrosses/GUI/imgs/starting/' + loc + '.png')

    def draw_x(self, index):
        self._draw_move(self.cross, index)

    def draw_o(self, index):
        self._draw_move(self.nought, index)

    def _draw_move(self, play, index):
        # need to store a ref to the image otherwise they get lost
        self.plays.append(play)

        x = index % 3
        y = int(index / 3)
        self.canvas.create_image(((self.x_offset + x*self.space_size), self.space_size*y), image=play, anchor=tk.NW, tag='ml')

        # TODO fade out the Bloch sphere in the given location
        # could just load a new faded image
        # self.current_frame.canvas.itemconfig(self.current_frame.bloch_tl, image = self.current_frame.nought)