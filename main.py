#!/usr/bin/env python3
'''
    Rio Hondo College
    CIT 128: Python Programming II
    Student Directed Project
'''
import tkinter as tk
from tkinter import ttk, Frame, Button, PhotoImage

BTN_L_CLICK = '<Button-1>' #Binds buttons to left click.
BTN_R_CLICK = '<Button-2>' #binds buttons to right click.

class Room:
    """data structure to store each room."""
    def __init__(self, roomSize, doorPositions):
        self.roomSize = roomSize
        self.doors = doorPositions
        print('room created of size:', self.roomSize)
        #self.doorLocations = doorLocations

# Main app window
class LayoutGenerator(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.btns = dict({})
        self.title('Layout Generator')
        self.winSizeMulti = 0.5 # 0.25 for 1/4 screen, 0.5 for 1/2 screen, etc.
        self.roomSize = {'x':0, 'y':0}
        self.currDoor = None
        self.allDoors = []
        self.screenSetup()
        
    def makeButtonGrid(self, size, frame):
        self.icons = {
            'default'  : PhotoImage(file='images/tanbox.png'),
            'white'    : PhotoImage(file='images/image2.png'),
            'selected' : PhotoImage(file='images/redbox.png'),
            'door' : PhotoImage(file='images/door.png')
        }
        for i in range(size):
            for j in range(size):
                if j == 0:
                    self.btns[i] = {}
                btn = {
                    'ypos'  : i,
                    'xpos'  : j,
                    'button': Button(frame, height=50, width=50, image=self.icons['default']),
                    'image' : self.icons['default']
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
        doorConfirmBtn = Button(controlsFrame, height=btnHeight, width=btnWidth, text='Door\nConfirm', command=self.confirmDoor)
        confirmBtn = Button(controlsFrame, height=btnHeight, width=btnWidth,text='Confirm', command=self.confirmRoom)

        sizeBtn.grid(row=0, column=0)
        doorConfirmBtn.grid(row=0, column=1)
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
        print("L Click") # DELETE
        if self.roomSize != {'x':0,'y':0}:
            self.currDoor = None
            self.clearSize()
        self.roomSize['x'] = btn['xpos']
        self.roomSize['y'] = btn['ypos']
        self.updateIcons(btn['xpos'], btn['ypos'], self.icons['selected'])
        print(self.roomSize) # DELETE
        
    #RIGHT CLICK BUTTON ACTION
    def gridButtonRightWrapper(self, i, j):
        return lambda Button: self.gridButtonRight(self.btns[i][j])
    def gridButtonRight(self, btn):
        print("R Click") # DELETE
        validDoor = False
        direction = None
        x = btn['xpos']
        y = btn['ypos']
        #TODO Currently corners aren't handled.  Simply prioritizeds vertical travel.
        #Direction 0 = north south doorway.  Direction 1 = east west doorway.
        if y == 0 and x <= self.roomSize['x']: #North wall,
            print("NORTH WALL") # DELETE
            validDoor = True
            direction = 0
        elif y == self.roomSize['y'] and x <= self.roomSize['x']: #South wall,
            print("SOUTH WALL") # DELETE
            validDoor = True
            direction = 0
        elif x == 0 and y <= self.roomSize['y']: #West wall,
            print("WEST WALL") # DELETE
            validDoor = True
            direction = 1
        elif x == self.roomSize['x'] and y <= self.roomSize['y']: #East wall,
            print("EAST WALL") # DELETE
            validDoor = True
            direction = 1

        if validDoor:
            if self.currDoor is not None: #if door already selected, delete prev selection.
                self.updateIcons(self.currDoor['x'], self.currDoor['y'], self.icons['selected'], batch=False, allDoors=True)
                self.currDoor = dict({})
            self.currDoor = {'x':x,'y':y,'direction':direction}
            self.updateIcons(x, y, self.icons['white'], batch=False)
            print(self.currDoor)

    def updateIcons(self, x, y, icon, batch=True, allDoors=False):
        print("Updating Icons:",x, y) # DELETE
        if batch == True:
            for i in range(y+1):
                for j in range(x+1):
                    currBtn = self.btns[i][j]
                    currBtn['button'].configure(image=icon)
                    currBtn['button'].image = icon
        else:
            currBtn = self.btns[y][x]
            currBtn['button'].configure(image=icon)
            currBtn['button'].image = icon
        if allDoors:
            for i in self.allDoors:
                currBtn = self.btns[i['y']][i['x']]
                currBtn['button'].configure(image=self.icons['door'])
                currBtn['button'].image = self.icons['door']

    def clearSize(self):
        #Resets all icons on grid and sets room size to 0.
        self.allDoors = []
        self.currDoor = None
        self.updateIcons(self.roomSize['x'], self.roomSize['y'], self.icons['default'])
        self.roomSize['x'] = 0
        self.roomSize['y'] = 0

    def confirmRoom(self):
        if self.roomSize['x'] != 0 and self.roomSize['y'] != 0 and len(self.allDoors) < 0:
            r = Room(roomSize=self.roomSize)
            print("Room Successfully created.") 
        else: print("Room creation error")

    def confirmDoor(self):
        if self.currDoor != None:
            if not self.allDoors:
                self.allDoors.append(self.currDoor)
                self.updateIcons(self.currDoor['x'], self.currDoor['y'], self.icons['door'], batch=False)
                print("Door created...") # DELETE
                print(self.allDoors) # DELETE
            else:
                for i in self.allDoors:
#If both doors are updown doors and have the same Y coordinate then they must be on the same wall.
                    if i['direction'] == 0 and i['y'] == self.currDoor['y']:
                        print("Same wall, vertical") # DELETE
                        return
                    if i['direction'] == 1 and i['x'] == self.currDoor['x']:
                        print("Same wall, horizontal") # DELETE
                        return
                    else: 
                        print("Door created...")
                        self.allDoors.append(self.currDoor)
                        self.updateIcons(self.currDoor['x'], self.currDoor['y'], self.icons['door'], batch=False)
                        return

a = LayoutGenerator()
a.mainloop()

