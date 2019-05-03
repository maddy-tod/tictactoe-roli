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
from PIL import Image
from PIL import ImageTk

from .BasePlayerGUI import BasePlayerGUI

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class BasicPlayerGUI(BasePlayerGUI):

    def __init__(self, parent, controller, **args):
        super().__init__(parent, controller, 'Terra Player', **args)
        self.window = parent
        self.draw_canvas()

    def load_bloch_image(self, file):
        img = Image.open(file)
        img = img.crop((50, 0, 480, 475))
        w, h = img.size
        img = img.resize((int(w * 0.35), int(h * 0.35)), Image.ANTIALIAS)
        return ImageTk.PhotoImage(img)

    def load_other_image(self, file):
        img = Image.open(file)
        img = img.resize((self.space_size, self.space_size), Image.ANTIALIAS)
        return ImageTk.PhotoImage(img)

    def _draw_move(self, play, index):
        # need to store a ref to the image otherwise they get lost
        self.plays.append(play)

        x = index % 3
        y = int(index / 3)
        img = self.canvas.create_image(((self.x_offset + x*self.space_size), self.space_size*y), image=play, anchor=tk.NW)

        self.plays_imgs.append(img)

    def draw_bloch(self, bloch_id, loc_index):
        path = '/Users/madeleinetod/Documents/NoughtsAndCrosses/GUI/imgs/testing/bloch'
        self.bloch_imgs[loc_index] = self.load_bloch_image(path + str(bloch_id) + '.png')

        self.canvas.itemconfig(self.bloch_canvas_objs[loc_index], image=self.bloch_imgs[loc_index])

    def show_states_pressed(self):

        self.showing_states = not self.showing_states

        text = "Show setup states"
        # Update the text
        if self.showing_states:
            text = "Pause"

        self.states_button.configure(text=text)

        if self.showing_states:
            self._animate_states()

    def _animate_states(self):

        # check you are still animating
        if self.showing_states:
            # get the next thing to draw from the controller
            self.controller.get_next_blochs()

            # loop
            self.window.after(600, self._animate_states)

    def reset(self):
        self.plays = []

        # reset the Bloch sphere pictures
        for bloch in self.bloch_canvas_objs:
            self.canvas.itemconfig(bloch, image=self.starting_img)

        for img in self.plays_imgs:
            self.canvas.delete(img)

        self.canvas.itemconfigure(self.state_label, text="Player's turn!")

    def draw_canvas(self):
        # if we wanted to re draw the images
        # self.gen_images()

        # Add buttons for the different modes
        self.states_button = tk.Button(self.canvas, text="Show setup states",
                                       command=lambda: self.show_states_pressed(),
                                       height=2, width=20)
        self.states_button.place(x=10, y=0)
        # We are not currently showing how the states change
        self.showing_states = False
        self.final_button = tk.Button(self.canvas, text="Show final states",
                                      command=lambda: self.controller.get_final_blochs(),
                                      height=2, width=20)
        self.final_button.place(x=10, y=50)
        self.result_button = tk.Button(self.canvas, text="Result",
                                       command=lambda: self.controller.show_result(),
                                       height=2, width=20)
        self.result_button.place(x=10, y=100)

        # Allows for a bit of padding
        temp_x_offset = self.x_offset + 10
        # load the starting image
        self.starting_img = self.load_bloch_image('GUI/imgs/starting/tl.png')

        # add this image into all the grid spaces
        self.bloch_tl = self.canvas.create_image((temp_x_offset, 0), image=self.starting_img, anchor=tk.NW, tag='tl')
        self.bloch_tm = self.canvas.create_image((self.space_size + temp_x_offset, 0), image=self.starting_img,
                                                 anchor=tk.NW, tag='tm')
        self.bloch_tr = self.canvas.create_image((self.space_size * 2 + temp_x_offset, 0), image=self.starting_img,
                                                 anchor=tk.NW, tag='tr')

        self.bloch_ml = self.canvas.create_image((temp_x_offset, self.space_size), image=self.starting_img,
                                                 anchor=tk.NW, tag='ml')
        self.bloch_mm = self.canvas.create_image((self.space_size + temp_x_offset, self.space_size),
                                                 image=self.starting_img, anchor=tk.NW, tag='mm')
        self.bloch_mr = self.canvas.create_image((self.space_size * 2 + temp_x_offset, self.space_size),
                                                 image=self.starting_img, anchor=tk.NW, tag='mr')

        self.bloch_bl = self.canvas.create_image((temp_x_offset, self.space_size * 2), image=self.starting_img,
                                                 anchor=tk.NW, tag='bl')
        self.bloch_bm = self.canvas.create_image((self.space_size + temp_x_offset, self.space_size * 2),
                                                 image=self.starting_img, anchor=tk.NW, tag='bm')
        self.bloch_br = self.canvas.create_image((self.space_size * 2 + temp_x_offset, self.space_size * 2),
                                                 image=self.starting_img, anchor=tk.NW, tag='br')

        self.bloch_canvas_objs = [self.bloch_tl, self.bloch_tm, self.bloch_tr,
                                  self.bloch_ml, self.bloch_mm, self.bloch_mr,
                                  self.bloch_bl, self.bloch_bm, self.bloch_br]
        self.bloch_imgs = [self.starting_img] * 9

        self.draw_grid()

    def moving_off(self):

        self.states_button.place_forget()
        self.states_button.destroy()
        self.final_button.place_forget()
        self.result_button.place_forget()

        self.canvas.place_forget()
        self.canvas.delete("all")
        self.canvas.pack()


