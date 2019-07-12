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
from GUI import *
from tkinter import font as tkfont


class NoughtsAndCrossesApp(tk.Tk):
    # start code from https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter

    def __init__(self, controller, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title('TicTacQ!')
        self.button_font = tkfont.Font(family='IBM Plex Sans', size=15)

        self.controller = controller

        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.running = True

        self.geometry("1500x800")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others

        # container contains the diff options
        # TODO make this dynamic
        self.player_container = tk.Frame(self, width=1500, height=600)
        self.player_container.grid(row=1, column=0)
        self.player_container.grid_propagate(False)

        self.frames = {}
        self.current_frame = None
        for F in (BasicPlayerGUI, GroverPlayerGUI, VQCPlayerGUI):
            page_name = F.__name__
            frame = F(parent=self.player_container, controller=self, width=1500, height=600)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        # Create the buttons for swapping between
        self.name_to_button = {}
        button_container = tk.Frame(self)
        button_container.grid(row=2, column=0, pady=50)
        basic_button = tk.Button(button_container, text="Basic Player",
                                 font=self.button_font,
                                 command=lambda: self.show_frame("BasicPlayerGUI"),
                                 height=2, width=12,
                                 borderwidth=100,
                                 highlightbackground='yellow')
        basic_button.grid(row=0, column=0, ipadx=31, sticky='W')
        self.name_to_button['BasicPlayerGUI'] = basic_button
        grover_button = tk.Button(button_container, text="Grover Player",
                                  font=self.button_font,
                                  command=lambda: self.show_frame("GroverPlayerGUI"),
                                  height=2, width=12,
                                  borderwidth=100,
                                  highlightbackground='grey')
        grover_button.grid(row=0, column=1, padx=60, ipadx=31)
        self.name_to_button['GroverPlayerGUI'] = grover_button
        svm_button = tk.Button(button_container, text="VQC Player",
                               font=self.button_font,
                               command=lambda: self.show_frame("VQCPlayerGUI"),
                               height=2, width=12,
                               borderwidth=100,
                               highlightbackground='light grey')
        svm_button.grid(row=0, column=2, ipadx=31)
        self.name_to_button['VQCPlayerGUI'] = svm_button

        self.show_frame("BasicPlayerGUI")

    def _on_closing(self):
        self.running = False
        self.destroy()

    def show_frame(self, page_name):
        """Show a frame for the given page name"""

        # deal with toggling the buttons
        pressed_button = self.name_to_button[page_name]
        for button in self.name_to_button.values():
            if button == pressed_button:
                button.config(highlightbackground='light blue')
            else:
                button.config(highlightbackground='grey')

        frame = self.frames[page_name]
        frame.tkraise()

        if self.current_frame:
            self.current_frame.moving_off()
        self.current_frame = frame
        self.current_frame.moving_to()
        self.controller.change_computer(page_name)

    def draw_x(self, index):
        self.current_frame.draw_x(index)

    def draw_o(self, index):
        self.current_frame.draw_o(index)

    def computers_turn(self):
        self.qcomputer.take_turn()

    def reset(self):
        logger.info("Reset the GUI")
        self.current_frame.reset()

    def set_winner(self, winner):
        self.current_frame.show_winner(winner)

    def get_next_blochs(self):
        blochs = self.controller.get_next_blochs()

        if blochs :
            # draw the updated blochs
            for bloch, qubit in blochs:
                self.current_frame.draw_bloch(bloch, qubit)
        else :
            # reset the button
            self.current_frame.show_states_pressed()

    def get_final_blochs(self):
        blochs = self.controller.get_final_blochs()

        if blochs:
            # draw the updated blochs
            for bloch, qubit in blochs:
                self.current_frame.draw_bloch(bloch, qubit)

    def show_result(self):
        self.controller.show_result()

    def show_matrices(self):
        self.controller.show_matrices()

    def show_q_view(self):
        self._show_view(size=3)

    def show_c_view(self):
        self._show_view(size=9)

    def _show_view(self, size):
        counts_dict = self.controller.get_svm_counts(size=size)

        # returns None if clicked when not computers turn
        if counts_dict:
            total_moves = sum(counts_dict.values())

            self.current_frame.reset_potential_moves()

            for move, count in counts_dict.items():
                self.current_frame.draw_potential_move(int(move), intensity=count / total_moves)

    def get_counts(self):
        return self.controller.get_counts()
