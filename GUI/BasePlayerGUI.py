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
from tkinter import font as tkfont

from PIL import Image, ImageTk

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class BasePlayerGUI(tk.Frame):

    def __init__(self, parent, controller, labeltxt, **args):
        tk.Frame.__init__(self, parent, **args)
        self.controller = controller

        self.title_font = tkfont.Font(family='IBM Plex Sans', size=40, weight="bold")
        self.label_font = tkfont.Font(family='IBM Plex Sans', size=22, weight="bold")
        self.button_font = tkfont.Font(family='IBM Plex Sans', size=15)

        label = tk.Label(self, text=labeltxt, font=self.title_font)
        label.pack(side="top", pady=20, anchor='w', padx=620-(len(labeltxt)))

        self.canvas = tk.Canvas(self, width=1500, height=600)
        self.cleaned = False

        self.state_label = self.canvas.create_text((240, 20), text="Player's turn!", font=self.label_font)
        self.canvas.pack()

        self.x_offset = 460
        self.space_size = 170

        # stored the noughts and crosses images that have been played
        self.plays = []
        self.plays_imgs = []
        self.nought = self.load_other_image('GUI/imgs/players/o.png')
        self.cross = self.load_other_image('GUI/imgs/players/x.png')

        self.button_x = 130

    def load_other_image(self, file):
        img = Image.open(file)
        img = img.resize((self.space_size, self.space_size), Image.ANTIALIAS)
        return ImageTk.PhotoImage(img)

    def draw_x(self, index):
        self._draw_move(self.cross, index)
        self.canvas.itemconfigure(self.state_label, text="Computer's turn")

    def draw_o(self, index):
        self._draw_move(self.nought, index)
        self.canvas.itemconfigure(self.state_label, text="Player's turn!")

    def _draw_move(self, play, index):
        # need to store a ref to the image otherwise they get lost
        self.plays.append(play)

        x = index % 3
        y = int(index / 3)
        img = self.canvas.create_image(((self.x_offset + x * self.space_size), self.space_size * y), image=play,
                                       anchor=tk.NW)

        self.plays_imgs.append(img)

    def draw_grid(self):
        # Draw lines of the TicTacToe grid
        x1 = self.space_size + self.x_offset
        x2 = self.space_size * 2 + self.x_offset

        self.canvas.create_line(x1, 0, x1, self.space_size * 3, fill='black', width=6)
        self.canvas.create_line(x2, 0, x2, self.space_size * 3, fill='black', width=6)

        self.canvas.create_line(self.x_offset, self.space_size, self.space_size * 3 + self.x_offset, self.space_size,
                                fill='black', width=6)
        self.canvas.create_line(self.x_offset, self.space_size * 2, self.space_size * 3 + self.x_offset,
                                self.space_size * 2, fill='black', width=6)

        self.canvas.pack()

    def moving_off(self):
        self.cleaned = True
        self.canvas.pack_forget()
        self.canvas.delete("all")
        self.canvas.pack()

    def show_winner(self, winner):
        self.canvas.itemconfigure(self.state_label, text=winner + " won!")

    def pack(self):
        self.canvas.pack()

    def moving_to(self):
        self.draw_canvas()

        if self.cleaned:
            self.state_label = self.canvas.create_text((240, 20), text="Player's turn!", font=self.label_font)
            self.cleaned = False

    def draw_canvas(self):
        pass

    def reset(self):
        self.plays = []
