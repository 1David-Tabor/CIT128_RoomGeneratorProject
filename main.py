#!/usr/bin/env python3
'''
    Rio Hondo College
    CIT 128: Python Programming II
    Student Directed Project
'''
import tkinter as tk
from tkinter import ttk, Frame, Button

BTN_L_CLICK = '<Button-1>' #Binds buttons to left click.
BTN_R_CLICK = '<Button-2>' #binds buttons to right click.

class Room:
    """Currently not used, data structure to store each room."""
    def __init__(self, roomSize, doorLocations):
        self.roomSize = roomSize
        self.doorLocations = doorLocations

# Main app window
class LayoutGenerator(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.btns = dict({})
        self.title('Layout Generator')
        self.labeltext = 'Hello World'
        self.winSizeMulti = 0.5 # 0.25 for 1/4 screen, 0.5 for 1/2 screen, etc.
        self.curr_roomsize = {'x':0, 'y':0}
        self.screenSetup()

    def makeButtonGrid(self, size, frame):
        for i in range(size):
            for j in range(size):
                if j == 0:
                    self.btns[i] = {}
                btn = {
                    'ypos': i,
                    'xpos': j,
                    'button': Button(frame, height=3, width=5)
                }
                btn['button'].bind(BTN_L_CLICK, self.gridButtonLeftWrapper(i, j))
                btn['button'].bind(BTN_R_CLICK, self.gridButtonRightWrapper(i, j))
                """Binds the gridButtonWrapper command to left click with inputs i and j. Gridbuttonwrapper
                returns a lambda with a button command "gridButton" based on the position of the button"""
                btn["button"].grid(row = i, column = j)
                self.btns[i][j] = btn

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
        sizeBtn = Button(controlsFrame, height=btnHeight, width=btnWidth, text='Size',  command=None)
        doorBtn = Button(controlsFrame, height=btnHeight, width=btnWidth, text='Doors', command=None)
        confirmBtn = Button(controlsFrame, height=btnHeight, width=btnWidth,text='Confirm', command=self.btnMthd)

        sizeBtn.grid(row=0, column=0)
        doorBtn.grid(row=0, column=1)
        confirmBtn.grid(row=0, column=2)

        # Quadrant 3: room editing grid.
        gridFrame = Frame(inputFrame, padx=5, pady=5)
        gridFrame.grid(row=1, column=0)
        gridSize = 5
        self.makeButtonGrid(gridSize, gridFrame)
        
        # Quadrants 2 & 4: Room viewer.
        viewFrame = Frame(inputFrame, padx=5, pady=5)
        viewFrame.grid(rowspan=2, column=1)


    #LEFT CLICK BUTTON ACTION
    def gridButtonLeftWrapper(self, i, j): 
        return lambda Button: self.gridButtonLeft(self.btns[i][j])
    def gridButtonLeft(self, btn):
        self.curr_roomsize['x'] = btn['xpos']
        self.curr_roomsize['y'] = btn['ypos']
        print(self.curr_roomsize)
        
    #RIGHT CLICK BUTTON ACTION
    def gridButtonRightWrapper(self, i, j): 
        return lambda Button: self.gridButtonRight(self.btns[i][j])
    def gridButtonRight(self, btn):
        print('Right Clicked')

    def btnMthd(self):
        print(self.btns)

a = LayoutGenerator()
a.mainloop()

