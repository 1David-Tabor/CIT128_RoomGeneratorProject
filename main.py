#!/usr/bin/env python3
'''
    Rio Hondo College
    CIT 128: Python Programming II
    Student Directed Project
'''
import tkinter as tk
from tkinter import ttk, Frame, Button, PhotoImage, Label
from PIL import Image, ImageDraw, ImageTk

BTN_L_CLICK = '<Button-1>' #Binds buttons to left click.
BTN_R_CLICK = '<Button-2>' #binds buttons to right click.

class Layout:
    def __init__(self):
        self.rooms = []
        self.size = {'x':0, 'y':0}

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
        self.doorPositions = doorPositions
        self.img = self.draw()
        print('room created of size:', self.roomSize) # DELETE
        print('doors located at:', self.doorPositions) # DELETE
    
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
            doors.append((i['x']*pixelsPerTile, i['y']*pixelsPerTile))
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
        permutationBtn = Button(outputFrame, height=btnHeight, width=btnWidth, text='Permute',  command=self.permutateRooms)
        permutationBtn.grid(row=0, column=0)

    def debugMethod(self):
        for i in self.allRooms:
            print(i.roomSize)
        print("Button Works")

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
        #Directions: 0=North, 1=South, 2=East, 3=West.
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
            direction = 2

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
    
    def updateViewFrame(self):
        for i in range(len(self.allRooms)):
            img = self.allRooms[i].img
            label = Label(self.viewFrame, image=img)
            label.image = img
            label.grid(row = i)

    def confirmRoom(self):
        if self.roomSize['x'] != 0 and self.roomSize['y'] != 0 and len(self.allDoors) > 0:
            r = Room(roomSize=dict(self.roomSize), doorPositions=self.allDoors)
            self.allRooms.append(r)
            print(r.roomSize)
            self.updateViewFrame()
            self.clearSize()
            print(r.roomSize)

    def confirmDoor(self):
        if self.currDoor != None:
            if self.allDoors == []:
                self.allDoors.append(self.currDoor)
                self.updateIcons(self.currDoor['x'], self.currDoor['y'], self.icons['door'], batch=False)
            else: #if allDoors contains items.
                for i in range(len(self.allDoors)):
                    #Two doors with the same "direction" are always on the same wall.
                    #When the loop finds a door on the same wall it gets replaced with the more recent door.
                    if self.currDoor['direction'] == self.allDoors[i]['direction']:
                        tmpX, tmpY = self.allDoors[i]['x'], self.allDoors[i]['y']
                        self.allDoors.pop(i)
                        self.allDoors.append(self.currDoor)
                        self.updateIcons(tmpX, tmpY, self.icons['selected'], batch=False, updateDoors=True)
                        return
                self.allDoors.append(self.currDoor)
                self.updateIcons(self.currDoor['x'], self.currDoor['y'], self.icons['door'], batch=False)
    
    def permutateRooms(self):
        gridSize = 0
        max_X = 0
        max_Y = 0
        for i in self.allRooms:
            print(i.roomSize)
            max_X += i.roomSize['x']
            max_Y += i.roomSize['y']
        print("Maxes:",max_X, max_Y)

        Python_2D_list = [[0 for j in range(gridSize)]for i in range(gridSize)]

a = LayoutGenerator()
a.mainloop()