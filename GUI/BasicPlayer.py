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

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class BasicPlayer(tk.Frame):

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
        self.starting_img = self.load_image('GUI/imgs/starting/tl.png')
        self.canvas.create_image((temp_x_offset, 0), image=self.starting_img, anchor=tk.NW, tag='tl')
        self.canvas.create_image((self.space_size + temp_x_offset, 0), image=self.starting_img, anchor=tk.NW, tag='tm')
        self.canvas.create_image((self.space_size*2 + temp_x_offset, 0), image=self.starting_img, anchor=tk.NW, tag='tr')

        self.canvas.create_image((temp_x_offset, self.space_size), image=self.starting_img, anchor=tk.NW, tag='ml')
        self.canvas.create_image((self.space_size + temp_x_offset, self.space_size), image=self.starting_img, anchor=tk.NW, tag='mm')
        self.canvas.create_image((self.space_size*2 + temp_x_offset, self.space_size), image=self.starting_img, anchor=tk.NW, tag='mr')

        self.canvas.create_image((temp_x_offset, self.space_size*2), image=self.starting_img, anchor=tk.NW, tag='bl')
        self.canvas.create_image((self.space_size + temp_x_offset, self.space_size*2), image=self.starting_img, anchor=tk.NW, tag='bm')
        self.canvas.create_image((self.space_size*2 + temp_x_offset, self.space_size*2), image=self.starting_img, anchor=tk.NW, tag='br')

        # Draw lines
        x1 = self.space_size + self.x_offset
        x2 = self.space_size*2 + self.x_offset
        self.canvas.create_line(x1, 0, x1, self.space_size*3, fill='blue', width=6)
        self.canvas.create_line(x2, 0, x2, self.space_size*3, fill='blue', width=6)

        self.canvas.create_line(self.x_offset, self.space_size, self.space_size*3 + self.x_offset, self.space_size, fill='blue', width=6)
        self.canvas.create_line(self.x_offset, self.space_size*2, self.space_size*3 + self.x_offset, self.space_size*2, fill='blue', width=6)
        self.canvas.pack()

    def load_image(self, file):
        img = Image.open(file)
        print(img.size)
        img = img.crop((50, 0, 480, 475))
        w, h = img.size
        img = img.resize((int(w * 0.35), int(h * 0.35)), Image.ANTIALIAS)
        return ImageTk.PhotoImage(img)

    def gen_images(self):
        locations = ['tl', 'tm', 'tr',
                     'ml', 'mm', 'mr',
                     'bl', 'bm', 'br']

        for loc in locations:
            x = plot_bloch_vector([0, 0, 1])
            x.savefig('/Users/madeleinetod/Documents/NoughtsAndCrosses/GUI/imgs/starting/' + loc + '.png')

