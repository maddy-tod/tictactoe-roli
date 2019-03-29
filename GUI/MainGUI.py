# -*- coding: utf-8 -*-

# Copyright 2018 IBM.
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
import tkinter as tk
from tkinter import font as tkfont
from GUI import *


class NoughtsAndCrossesApp(tk.Tk):
    # start code from https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter

    def __init__(self, controller, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.controller = controller

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        tk.Canvas(self, width=150, height=70).grid(row=0, column=0)
        self.geometry("1500x800")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others

        # container contains the diff options
        # TODO make this dynamic
        player_container = tk.Frame(self, width=1100, height=600)#, bg='blue')
        player_container.grid(row=1, column=1)
        player_container.grid_propagate(False)

        self.frames = {}
        self.current_frame = None
        for F in (BasicPlayerGUI, GroverPlayerGUI, SVMPlayerGUI):
            page_name = F.__name__
            frame = F(parent=player_container, controller=self, width=1100, height=600,)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("BasicPlayerGUI")

        # Create the buttons for swapping between
        button_container = tk.Frame(self)
        button_container.grid(row=2, column=1, pady=10)
        basic_button = tk.Button(button_container, text="Basic Player",
                                 command=lambda: self.show_frame("BasicPlayerGUI"),
                                 height=2, width=20)
        basic_button.grid(row=0, column=0, padx=10)
        grover_button = tk.Button(button_container, text="Grover Player",
                                  command=lambda:self.show_frame("GroverPlayerGUI"),
                                  height=2, width=20)
        grover_button.grid(row=0, column=1, padx=10)
        svm_button = tk.Button(button_container, text="SVM Player",
                               command=lambda: self.show_frame("SVMPlayerGUI"),
                               height=2, width=20)
        svm_button.grid(row=0, column=2, padx=10)

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()
        self.current_frame = frame

    def draw_x(self, index):
        self.current_frame.draw_x(index)

    def draw_o(self, index):
        self.current_frame.draw_o(index)

    def computers_turn(self):
        self.qcomputer.take_turn()

    def reset(self):
        self.current_frame.reset()


if __name__ == "__main__":
    app = NoughtsAndCrossesApp()
    app.mainloop()
