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
from .BasePlayerGUI import BasePlayerGUI
from qiskit.visualization import plot_histogram
from PIL import Image
from PIL import ImageTk
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class GroverPlayerGUI(BasePlayerGUI):

    matrix = """ 
    ⎡1                     ⎤
    ⎢  -1                  ⎥
    ⎢      1               ⎥
    ⎢        -1            ⎥
    ⎢            1         ⎥
    ⎢              -1      ⎥
    ⎢                  1   ⎥
    ⎣                    -1⎦ 	  
    """

    def __init__(self, parent, controller, **args):
        super().__init__(parent, controller, 'Grover Player', **args)

        self.canvas.pack()

    def draw_canvas(self):
        # Add buttons for the different modes
        self.maths_button = tk.Button(self.canvas, text="Matrices",
                                       command=lambda: self.controller.show_matrices(),
                                       height=2, width=20)
        self.maths_button.place(x=110, y=50)

        self.result_button = tk.Button(self.canvas, text="Result",
                                       command=lambda: self.show_result(),
                                       height=2, width=20)
        self.result_button.place(x=110, y=100)

        self.canvas.create_rectangle(10, 20, 50, 100, outline="")

        label_font = tkfont.Font(family='Helvetica', size=18, weight="bold")

        self.canvas.coords(self.state_label, (1200, 40))
        self.oracle_label = self.canvas.create_text((1200, 160), text=GroverPlayerGUI.matrix, font=label_font)
        self.init_vector_label = self.canvas.create_text((1275, 160), text="", font=label_font)
        self.final_vector_label = self.canvas.create_text((1400, 160), text="", font=label_font)

        self.draw_grid()

    def show_result(self):
        self.controller.show_result()

        # show the mpl image
        counts = self.controller.get_counts()

        img = plot_histogram(counts)
        img.savefig('counts.png')

        img = Image.open('counts.png')
        img = img.resize((400, 320), Image.ANTIALIAS)
        img = img.crop((0, 30, 400, 320))
        img = ImageTk.PhotoImage(img)

        self.counts_img_canvas = self.canvas.create_image((1250, 400), image=img)
        self.counts_img = img

    def update_matrix(self, vector):
        start_amplitudes = """ 
⎡{0:.2f}⎤
⎢{1:.2f}⎥
⎢{2:.2f}⎥
⎢{3:.2f}⎥
⎢{4:.2f}⎥
⎢{5:.2f}⎥
⎢{6:.2f}⎥
⎣{7:.2f}⎦ 	  
""".format(*vector)

        end_amplitudes = """ 
      ⎡ {0:.2f}⎤
      ⎢-{1:.2f}⎥
      ⎢ {2:.2f}⎥
 =   ⎢-{3:.2f}⎥
      ⎢ {4:.2f}⎥
      ⎢-{5:.2f}⎥
      ⎢ {6:.2f}⎥
      ⎣-{7:.2f}⎦ 	  
""".format(*vector)

        self.canvas.itemconfigure(self.init_vector_label, text=start_amplitudes)
        self.canvas.itemconfigure(self.final_vector_label, text=end_amplitudes)

        print(start_amplitudes)
        print('*'*20)
        print(end_amplitudes)

    def reset(self):
        label_font = tkfont.Font(family='Helvetica', size=18, weight="bold")
        self.state_label = self.canvas.create_text((1200, 40), text="Player's turn!", font=label_font)

