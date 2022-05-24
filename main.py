#!/usr/bin/env python3
'''
    Rio Hondo College
    CIT 128: Python Programming II
    Student Directed Project
'''
import tkinter as tk
from itertools import permutations
from tkinter import ttk, Frame, Button, PhotoImage, Label
from PIL import Image, ImageDraw, ImageTk
import time
import random

BTN_L_CLICK = '<Button-1>' #Binds buttons to left click.
BTN_R_CLICK = '<Button-2>' #binds buttons to right click.

def abs(val):
    if val < 0:
        return val * (-1)
    else: return val

class Room:
    '''
    Object to store a room as size and door locations.
    
    Parameters:
        roomSize (dict): the 'x' and 'y' dimensions of the room.

        doorPositions (dict): 'x' and 'y' coordinates of where the door is in relation
        to the room size, and the 'direction' of the door.
    
    Methods: 
        draw: creates representative image of the room and it's door positions.
    '''

    def __init__(self, roomSize, doorPositions):
        self.roomSize = roomSize
        self.relativeX = roomSize['y']
        self.relativeY = roomSize['x']
        self.doorPositions = doorPositions
        self.img = self.draw()
        print('room created of size:', self.roomSize) # DELETE
        print('doors located at:', self.doorPositions) # DELETE

    def print(self):
        print(f'\nRoomsize: {self.roomSize}')
        for i in self.doorPositions:
            print(f'Door: x:{i.xpos}, y:{i.ypos}')
        print('\n')

    def updatePosition(self, placedDoor):
        deltaX = (placedDoor.xpos - placedDoor.relativeX) +1
        deltaY = (placedDoor.ypos - placedDoor.relativeY) +1
        self.relativeX += self.roomSize['x'] + deltaX
        self.relativeY += self.roomSize['y'] + deltaY
        for i in self.doorPositions:
            if i == placedDoor:
                continue
            else:
                i.relativeX = i.xpos + deltaX
                i.relativeY = i.ypos + deltaY
    
    def draw(self):
        '''
        Creates representative image of the room and it's door positions.

        Parameters:
            None, creates image based on object properties defined in __init__. 

        Returns:
            ImageTk.PhotoImage object which can be displayed using Tkinter.
        '''
        xSize = self.roomSize['x'] + 1
        ySize = self.roomSize['y'] + 1
        pixelsPerTile = 25 #Can be modified to adjust tile size.
        doors = []
        for i in self.doorPositions:
            doors.append((i.xpos*pixelsPerTile, i.ypos*pixelsPerTile))
        img = Image.new('RGB', (xSize*pixelsPerTile+1, ySize*pixelsPerTile+1), (125, 125, 125))
        draw = ImageDraw.Draw(img)
        for i in range(0, pixelsPerTile*xSize, pixelsPerTile):
            for j in range(0, ySize*pixelsPerTile, pixelsPerTile):
                if (i, j) in doors: # If current coordinate is a door tile, change the color.
                    shape = [(i, j), (i+pixelsPerTile, j+pixelsPerTile)]
                    color = '#187225' # green
                else:
                    shape = [(i, j), (i+pixelsPerTile, j+pixelsPerTile)]
                    color = '#ff785a' # red
                draw.rectangle(shape, fill=color, outline='black')
        img = ImageTk.PhotoImage(img)
        return img

class Door:
    def __init__(self, x, y, direction):
        self.xpos = x
        self.ypos = y
        self.relativeX = x
        self.relativeY = y
        self.direction = direction
        self.parent = None

# Main app window
class LayoutGenerator(tk.Tk):
    '''
    Object to create rooms and generate layouts from permutations of the rooms.

    Methods:
        makeButtonGrid(size, frame): Creates a square grid of 'size' buttons in specified frame.
        screenSetup(): Sets up frames, tabs, and buttons for the program.
        gridButtonLeftWrapper(i, j): Gets button at coordinates [i][j] and passes it to gridButtonLeft.
        gridButtonLeft(btn): Sets the size (x, y) of the room in progress.
        gridButtonRightWrapper(i, j): Gets button at coordinates [i][j] and passes it to gridButtonRight.
        gridButtonRight(btn): Attempts to set passed button as the current door if it would be a valid door.
        updateIcons(x, y, icon, batch, updateDoors): Updates a set of buttons or a singular button to
            set their image to icon.
        clearSize(): Resets icons to default, deletes room in progress.
        updateViewFrame(): Displays room images to the right of the grid.
        confirmDoor(): Adds the current door to the current room. Deletes older door if there is a conflict.
    '''
    def __init__(self):
        tk.Tk.__init__(self)
        self.btns = dict({})
        self.title('Layout Generator')
        self.winSizeMulti = 0.5 # 0.25 for 1/4 screen, 0.5 for 1/2 screen, etc.
        self.gridSize = 5
        self.numRooms = 5
        self.roomSize = {'x':0, 'y':0}
        self.currDoor = None
        self.allDoors = []
        self.allRooms = []
        self.allPerms = []
        self.oldPerms = []
        self.screenSetup()
        
    def makeButtonGrid(self, size, frame):
        self.icons = {
            'default'  : PhotoImage(file='images/tanbox.png'),
            'white'    : PhotoImage(file='images/image2.png'),
            'selected' : PhotoImage(file='images/redbox.png'),
            'door'     : PhotoImage(file='images/door.png'),
            'hl_door'  : PhotoImage(file='images/hl_door.png')
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

        # Input Frame Setup
        inputFrameL = Frame(inputFrame, width=self.screenWidth, height=self.screenHeight)
        inputFrameR = Frame(inputFrame, width=self.screenWidth, height=self.screenHeight)
        inputFrameL.grid(column=0, row=0)
        inputFrameR.grid(column=1, row=0)
        
        # Quadrant 1: Size, Door placement, and Confirm buttons.
        controlsFrame = Frame(inputFrameL, padx=5, pady=5)
        controlsFrame.grid(row=0, column=0)
        btnHeight, btnWidth = 5, 10
        sizeBtn = Button(controlsFrame, height=btnHeight, width=btnWidth, text='Size',  command=self.debugMethod)
        doorConfirmBtn = Button(controlsFrame, height=btnHeight, width=btnWidth, text='Door\nConfirm', command=self.confirmDoor)
        confirmBtn = Button(controlsFrame, height=btnHeight, width=btnWidth,text='Confirm', command=self.confirmRoom)
        sizeBtn.grid(row=0, column=0)
        doorConfirmBtn.grid(row=0, column=1)
        confirmBtn.grid(row=0, column=2)

        # Quadrant 3: room editing grid.
        gridFrame = Frame(inputFrameL, padx=5, pady=5)
        gridFrame.grid(row=1, column=0)
        self.makeButtonGrid(self.gridSize, gridFrame)
        
        # Quadrants 2 & 4: Room viewer.
        self.viewFrame = Frame(inputFrameR, padx=5, pady=5)
        self.viewFrame.grid(row=0, column=0)

        # Output Frame Setup
        permutationBtn = Button(outputFrame, height=btnHeight, width=btnWidth, text='Permute',  command=self.permuteBtn)
        permutationBtn.grid(row=0, column=0)

    def validDoorConnections(self, roomList):
        doorList = []
        validPairs = set()
        for i in roomList:
            doorList.append(i.doorPositions)
        for rowi in doorList: #All these nested for loops get the possible
            for doori in rowi:#different combinations for each door to each other door.
                for rowj in doorList:
                    if rowj == rowi:
                        continue
                    else: 
                        for doorj in rowj:
                            if self.doorMath(doori, doorj):
                                doorset = (doori, doorj)
                                validPairs.add(frozenset(doorset))
        tmp = []
        for i in validPairs:
            mt = tuple(i)
            tmp.append(mt)
        return tmp
    
    def doorMath(self, door1, door2):
        if abs(door1.direction) - abs(door2.direction) == 1:
            return True
        else:
            return False

    def drawLayout(self, permList):
        randIndex = random.randrange(0, len(permList))
        tmp = permList.pop(randIndex)
        roomsChecked = set()
        for doorPair in tmp: 
            currentRooms = set()
            currentRooms.add(doorPair[0].parent)
            currentRooms.add(doorPair[1].parent)
            currentRooms.difference(roomsChecked)
            for i in doorPair:
                if len(roomsChecked) == 0:
                    roomsChecked.add(i.parent)
                    continue
                if i.parent in currentRooms: # If the door's parent is in current rooms then the door hasn't had its position updated.
                    i.parent.updatePosition(i)
        print("type for tmp:", type(tmp))  # DELETE
        self.oldPerms.append(tmp)

    def debugMethod(self):
        self.drawLayout(self.allPerms)
        counter = 0
        
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
        #TODO Currently corners aren't handled.  Prioritizes vertical travel.
        #Directions: 0=North, 1=South, 4=East, 3=West.
        if y == 0 and x <= self.roomSize['x']: #North wall,
            print("NORTH WALL") # DELETE
            validDoor = True
            direction = 0
        elif y == self.roomSize['y'] and x <= self.roomSize['x']: #South wall,
            print("SOUTH WALL") # DELETE
            validDoor = True
            direction = 1
        elif x == 0 and y <= self.roomSize['y']: #West wall,
            print("WEST WALL") # DELETE
            validDoor = True
            direction = 3
        elif x == self.roomSize['x'] and y <= self.roomSize['y']: #East wall,
            print("EAST WALL") # DELETE
            validDoor = True
            direction = 4

        if validDoor:
            if self.currDoor is not None: #if door already selected, delete prev selection.
                self.updateIcons(self.currDoor['x'], self.currDoor['y'], self.icons['selected'], batch=False, updateDoors=True)
                self.currDoor = dict({})
            self.currDoor = {'x':x,'y':y,'direction':direction}
            self.updateIcons(x, y, self.icons['hl_door'], batch=False)

    def updateIcons(self, x, y, icon, batch=True, updateDoors=False):
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
        if updateDoors:
            for i in self.allDoors:
                currBtn = self.btns[i.ypos][i.xpos]
                currBtn['button'].configure(image=self.icons['door'])
                currBtn['button'].image = self.icons['door']

    def clearSize(self):
        #Resets all icons on grid and sets room size to 0.
        self.allDoors = []
        self.currDoor = None
        self.updateIcons(self.roomSize['x'], self.roomSize['y'], self.icons['default'])
        self.roomSize['x'] = 0
        self.roomSize['y'] = 0
    
    def updateViewFrame(self):
        for i in range(len(self.allRooms)):
            img = self.allRooms[i].img
            label = Label(self.viewFrame, image=img)
            label.image = img
            label.grid(row = i)

    def permuteBtn(self):
        valids = self.validDoorConnections(self.allRooms)
        print("valids len:", len(valids)) # DELETE
        perms = permutations(valids, len(self.allRooms)-1)
        goodPerms = []
        t1 = time.time() # DELETE
        for i in perms:
            if self.isValidPerm(i):
                print("was valid")
                goodPerms.append(i)
        t2 = time.time() # DELETE
        print("Time:", t2-t1) # DELETE
        self.allPerms = goodPerms
        counter = 0
        print("Len:", len(goodPerms)) # DELETE
        for i in goodPerms: # DELETE
            print(f"\nPerm {counter}")
            counter += 1
            for j in i:
                print(f'({j[0].parent.roomIndex}, {j[0].direction}) -> ({j[1].parent.roomIndex}, {j[1].direction})')

    def isValidPerm(self, perm):
        for i in perm:
            for j in perm:
                if i == j:
                    continue
                elif i[0] == j[0]:
                    return False
                elif i[0] == j[1]:
                    return False
                elif i[1] == j[0]:
                    return False
                elif i[1] == j[1]:
                    return False
                elif i[0].parent == j[0].parent and i[1].parent == j[1].parent:
                    return False
                elif i[0].parent == j[1].parent and i[1].parent == j[0].parent:
                    return False
                else: return True
        return True

    def confirmRoom(self):
        if self.roomSize['x'] != 0 and self.roomSize['y'] != 0 and len(self.allDoors) > 0:
            r = Room(roomSize=dict(self.roomSize), doorPositions=self.allDoors)
            for i in r.doorPositions:
                i.parent = r # adding reference to parent.
            self.allRooms.append(r)
            r.roomIndex = len(self.allRooms) - 1
            self.updateViewFrame()
            self.clearSize()

    def confirmDoor(self):
        if self.currDoor != None:
            door = Door(self.currDoor['x'], self.currDoor['y'], self.currDoor['direction'])
            if self.allDoors == []:
                self.allDoors.append(door)
                self.updateIcons(self.currDoor['x'], self.currDoor['y'], self.icons['door'], batch=False)
            else: #if allDoors contains items.
                for i in range(len(self.allDoors)):
                    #Two doors with the same "direction" are always on the same wall.
                    #When the loop finds a door on the same wall it gets replaced with the more recent door.
                    if self.currDoor['direction'] == self.allDoors[i].direction:
                        tmpX, tmpY = self.allDoors[i].xpos, self.allDoors[i].ypos
                        self.allDoors.pop(i)
                        self.allDoors.append(door)
                        self.updateIcons(tmpX, tmpY, self.icons['selected'], batch=False, updateDoors=True)
                        return
                self.allDoors.append(door)
                self.updateIcons(self.currDoor['x'], self.currDoor['y'], self.icons['door'], batch=False)

a = LayoutGenerator()
a.mainloop()