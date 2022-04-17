#!/usr/bin/env python3
'''
    Rio Hondo College
    CIT 128: Python Programming II
    Student Directed Project
'''
import tkinter as tk
from tkinter import Button, Label, ttk, Frame

class Room:
    def __init__(self, roomSize, doorLocations):
        self.roomSize = roomSize
        self.doorLocations = doorLocations

# Main app window
class LayoutGenerator(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Layout Generator')
        self.labeltext = 'Hello World'
        winSizeMulti = 0.5 # 0.25 for 1/4 screen, 0.5 for 1/2 screen, etc.
        self.screenWidth = (int(self.winfo_screenwidth() * winSizeMulti))
        self.screenHeight = (int(self.winfo_screenheight() * winSizeMulti))
        self.geometry(f"{self.screenWidth}x{self.screenHeight}")

        #Creating tabs for input, output, and help page.
        tabs = ttk.Notebook(self)
        tabs.pack()
        inputFrame = Frame(tabs, width=self.screenWidth, height=self.screenHeight)
        outputFrame = Frame(tabs, width=self.screenWidth, height=self.screenHeight)
        helpFrame = Frame(tabs, width=self.screenWidth, height=self.screenHeight)
        tabs.add(inputFrame, text='Input')
        tabs.add(outputFrame, text='Output')
        tabs.add(helpFrame, text='Help')

        gridFrame = Frame(inputFrame)
        gridFrame.grid(row=1, column=0)

        # Size, Door placement, and Confirm buttons.
        controlsFrame = Frame(inputFrame)
        controlsFrame.grid(row=0, column=1,)
        sizeBtn = Button(controlsFrame, height=3 , width=5, command=None)
        doorBtn = Button(controlsFrame, height=3 , width=5, command=None)
        confirmBtn = Button(controlsFrame, height=3 , width=5, command=None)
        sizeBtn.grid(row=0, column=0)
        doorBtn.grid(row=0, column=1)
        confirmBtn.grid(row=0, column=2)

        lbl = Label(inputFrame, text='Q1')
        lbl.grid(row=0, column=0)


        # Using nested for loops to generate a square grid.
        self.gridSize = 5
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                btn = Button(gridFrame, height=3 , width=5, command=None)
                btn.grid(row=i, column=j)




a = LayoutGenerator()
a.mainloop()

