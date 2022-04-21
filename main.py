#!/usr/bin/env python3
'''
    Rio Hondo College
    CIT 128: Python Programming II
    Student Directed Project
'''
import tkinter as tk
from tkinter import ttk, Frame, Button

class Room:
    def __init3__(self, roomSize, doorLocations):
        self.roomSize = roomSize
        self.doorLocations = doorLocations
BTN_CLICK = '<Button-1>'
# Main app window
class LayoutGenerator(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.btns = dict({})
        self.title('Layout Generator')
        self.labeltext = 'Hello World'
        self.winSizeMulti = 0.5 # 0.25 for 1/4 screen, 0.5 for 1/2 screen, etc.
        self.screenSetup()
    
    def screenSetup(self):
        self.screenWidth = (int(self.winfo_screenwidth() * self.winSizeMulti))
        self.screenHeight = (int(self.winfo_screenheight() * self.winSizeMulti))
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

        # Quadrant 1: Size, Door placement, and Confirm buttons.
        controlsFrame = Frame(inputFrame, padx=5, pady=5)
        controlsFrame.grid(row=0, column=0)
        btnHeight, btnWidth = 5, 10
        sizeBtn = Button(controlsFrame, height=btnHeight, width=btnWidth, text='Size', command=None)
        doorBtn = Button(controlsFrame, height=btnHeight, width=btnWidth, text='Doors', command=None)
        confirmBtn = Button(controlsFrame, height=btnHeight, width=btnWidth,text='Confirm', command=self.btnMthd)

        sizeBtn.grid(row=0, column=0)
        doorBtn.grid(row=0, column=1)
        confirmBtn.grid(row=0, column=2)

        # Quadrant 3: room editing grid.
        gridFrame = Frame(inputFrame, padx=5, pady=5)
        gridFrame.grid(row=1, column=0)

                # Using nested for loops to generate a square grid.
        self.gridSize = 5
        # ALMOST WORKING. Currently bugged so that each button is just a clone of the last
        # Button created.  Not sure how to fix this yet.  TODO.
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                if j == 0:
                    self.btns[i] = {}

                btn = {
                    "position": {
                        "row": i,
                        "column": j },
                    "button": Button(gridFrame, height=3, width=5)
                }
                btn["button"].bind(BTN_CLICK, self.gridButtonWrapper(i, j))
                #btn = Button(gridFrame, height=3 , width=5, command = self.gridButton(gridLocation))
                #btn.grid(row=i, column=j)
                btn["button"].grid(row = i, column = j)
                self.btns[i][j] = btn

        # Quadrants 2 & 4: Room viewer.
        viewFrame = Frame(inputFrame, padx=5, pady=5)
        viewFrame.grid(rowspan=2, column=1)
        
    def gridButtonWrapper(self, i, j):
        return lambda Button: self.gridButton(self.btns[i][j]) #self.btns[i][j]

    def gridButton(self, btn):
        print(btn["position"])

    def btnMthd(self):
        print(self.btns)
    

a = LayoutGenerator()
a.mainloop()

