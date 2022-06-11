#!/usr/bin/env python3
'''
    Rio Hondo College
    CIT 128: Python Programming II
    Student Directed Project
'''
import tkinter as tk
from itertools import permutations
from tkinter import ttk, Frame, Button, PhotoImage, Label, messagebox, Scrollbar
from PIL import Image, ImageDraw, ImageTk
import time
import random

BTN_L_CLICK = '<Button-1>' #Binds buttons to left click.
BTN_R_CLICK = '<Button-2>' #binds buttons to right click.

def abs(val):
    """
    Function to return absolute value of a number

    Parameters:
        val(int)
    
    Returns:
        Absolute value of number
    """
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
        updatePosition: updates room and children(doors) relative positions for placement.
        draw: creates representative image of the room and it's door positions.
    '''

    def __init__(self, roomSize, doorPositions):
        self.roomSize = roomSize
        self.relativeX = roomSize['x']
        self.relativeY = roomSize['y']
        self.doorPositions = doorPositions
        self.img = self.draw()

    def updatePosition(self, placedDoor):
        """
        Updates room and children(doors) relative positions for placement.
        
        Parameters:
            placedDoor (door): door object which has already been "placed" i.e. it's relative position is already updated.
        """
        deltaX = (placedDoor.relativeX - placedDoor.xpos)
        deltaY = (placedDoor.relativeY - placedDoor.ypos)
        self.relativeX += deltaX
        self.relativeY += deltaY

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
                draw.rectangle(shape, fill=color, outline='black', width=1)
        img = ImageTk.PhotoImage(img)
        return img

class Door:
    '''
    Object to serve as children to rooms and may pair up to form connection points between rooms.
    
    Parameters:
        x (int): x coordinate of door within it's parent room.
        y (int): y coordinate of door within it's parent room.
        direction (int): representative number of the door's cardinal direction. (N, S, W, E)->(0, 1, 3, 4)
    '''

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
        validDoorConnections(roomList): Finds list of valid door pairs (N->S, E->W)and returns it.
        doorMath(door1, door2): Determines if two doors make a valid pair using their direction value.
        drawLayout(permList): Creates representative image of a permutation.
        nextPerm(): Gets next permutation and calls drawLayout to create image.
        resetBtn(): Resets grid, permutation list, and created rooms.
        permuteBtn(): Creates list of permutations from created rooms.
        isValidPerm(perm): Checks to ensure a permutation does not contain the same room twice or an impossible combination.
        confirmRoom(): Adds current room to list for use in a permutation.
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
        self.roomLbls = []
        self.screenSetup()
        
    def makeButtonGrid(self, size, frame):
        '''
        Creates a grid of buttons for size selection and door placement.

        Parameters:
            size (Tuple): x and y size for the button grid.
            frame (Frame): frame where button grid will be created.
        '''
        self.icons = {
            'default'  : PhotoImage(file='images/tanbox.png'),
            'white'    : PhotoImage(file='images/image2.png'),
            'selected' : PhotoImage(file='images/redbox.png'),
            'door'     : PhotoImage(file='images/door.png'),
            'hl_door'  : PhotoImage(file='images/hl_door.png'),
            'nmp'      : PhotoImage(file='images/nmp.png'),
            'perms'    : PhotoImage(file='images/permsready.png')
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
        '''
        Sets up tabs, frames, labels, and some buttons.
        
        Parameters:
            None
        '''
        self.screenWidth = (int(self.winfo_screenwidth() * self.winSizeMulti))
        self.screenHeight = (int(self.winfo_screenheight() * self.winSizeMulti))
        self.geometry(f"{self.screenWidth}x{self.screenHeight}")

        #Creating tabs for input, output, and help page.
        tabs = ttk.Notebook(self)
        tabs.pack()
        inputFrame = Frame(tabs, width=self.screenWidth, height=self.screenHeight)
        self.outputFrame = Frame(tabs, width=self.screenWidth, height=self.screenHeight)
        helpFrame = Frame(tabs, width=self.screenWidth, height=self.screenHeight)
        tabs.add(inputFrame, text='Input')
        tabs.add(self.outputFrame, text='Output')
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
        doorConfirmBtn = Button(controlsFrame, height=btnHeight, width=btnWidth, text='Door\nConfirm', command=self.confirmDoor)
        confirmBtn = Button(controlsFrame, height=btnHeight, width=btnWidth,text='Room\nConfirm', command=self.confirmRoom)
        resetBtn = Button(controlsFrame, height=btnHeight, width=btnWidth,text='Reset', command=self.resetBtn)
        doorConfirmBtn.grid(row=0, column=1)
        confirmBtn.grid(row=0, column=2)
        resetBtn.grid(row=0, column=3)
        # Quadrant 3: room editing grid.
        gridFrame = Frame(inputFrameL, padx=5, pady=5)
        gridFrame.grid(row=1, column=0)
        self.makeButtonGrid(self.gridSize, gridFrame)
        
        # Quadrants 2 & 4: Room viewer.
        self.viewFrame = Frame(inputFrameR, padx=5, pady=5)
        self.viewFrame.grid(row=0, column=0)
        #TODO Add scrollbar to frame so grid doesn't move around.

        # Output Frame Setup
        permutationBtn = Button(self.outputFrame, height=btnHeight, width=btnWidth, text='Make\nPermutations',  command=self.permuteBtn)
        permutationBtn.grid(row=0, column=0)
        sizeBtn = Button(self.outputFrame, height=btnHeight, width=btnWidth, text='Next\nPermutation',  command=self.nextPerm)
        sizeBtn.grid(row=0, column=1)
        self.outputLabel = Label(self.outputFrame, anchor='e')
        self.outputLabel.grid(row=1,columnspan=2)

        # Help Frame Setup
        inputHelpTitle = 'Input Screen'
        inputHelpText1 = ('Left click a position on the grid to select the size of a room.\n'
                        'The minimum size for a room is 2x2.\n'
                        'Once you have chosen a size, right click on one of the highlighted edges to place a door.\n'
                        'Only one door may be placed per wall.\n'
                        'If you are happy with the placement of your door, click the \'Door Confirm\' Button.\n'
                        'To move a door simply place a new door on the same wall and the old one will be removed.')
        inputHelpLabel0 = Label(helpFrame, font=('arial bold', 20), text=inputHelpTitle)
        inputHelpLabel1 = Label(helpFrame, anchor='e', justify='left', text=inputHelpText1)
        inputHelpLabel0.grid(row=0)
        inputHelpLabel1.grid(row=1)
        inputHelpTitle = 'Output Screen'
        inputHelpText1 = ('After you have input at least 2 rooms you may proceed to the output screen.\n'
                        'On the output screen, click the \'Make Permutations\' Button.\n'
                        'This will come up with the possible combinations of rooms behind the scenes.\n'
                        'Then click the \'Next Permutation\' Button to see a permutation.\n'
                        'The \'Next Permutation\' Button will pick a random permutation for you and display it.\n'
                        'After you have viewed every permutation a graphic will appear alerting you.\n'
                        'If you would like to view the permutations again, press the \'Make Permutations\' Button.')
        inputHelpLabel2 = Label(helpFrame, font=('arial bold', 20), text=inputHelpTitle)
        inputHelpLabel3 = Label(helpFrame,anchor='e', justify='left', text=inputHelpText1)
        inputHelpLabel2.grid(row=2)
        inputHelpLabel3.grid(row=3)

    def validDoorConnections(self, roomList):
        '''
        Creates list of doors which can be paired together as a connection.

        Parameters:
            roomList (List): List containing all confirmed Rooms.

        Returns:
            tmp (List): List of tuples, each tuple being a valid connection from the confirmed rooms.
        '''
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
        '''
        Checks if two doors have compatible directions, i.e. North & South or East & West

        Parameters:
            door1 (Door): door object to have direction checked and compared.
            door2 (Door): door object to have direction checked and compared.

        Returns:
            Boolean.
        '''
        if abs(door1.direction) - abs(door2.direction) == 1:
            return True
        else:
            return False

    def drawLayout(self, permList):
        '''
        Creates representative image of next permutation in the permList.

        Parameters:
            permList (List): List of lists of door combinations.

        Returns:
            img (Image): Image of permutation, draws room and door locations.
        '''
        if len(permList) == 0:
            return self.icons['nmp'] #Returns "no more permutations" icon.
        randIndex = random.randrange(0, len(permList))
        tmp = list(permList.pop(randIndex)) # set tmp to a random permutaiton created.
        roomsPositioned = set()
        for doorPair in tmp: 
            if len(roomsPositioned) == 0: # if no rooms have been placed. place the first avaliable.
                roomsPositioned.add(doorPair[0].parent)
            currentRooms = set()
            currentRooms.add(doorPair[0].parent)
            currentRooms.add(doorPair[1].parent)
            currentRooms.difference(roomsPositioned) # Ensure rooms aren't being "placed" twice.
            if len(currentRooms.difference(roomsPositioned)) != 1:
                tmp.remove(doorPair)
                tmp.append(doorPair)# Puts the pair at the end of tmp.
                continue
            otherDoor = None # Otherdoor is a doorway which is already positioned.
            for door in doorPair:  # The other door's position will be used to position the new room.
                if door.parent in roomsPositioned:
                    otherDoor = door
            for door in doorPair:
                if door == otherDoor:
                    continue
                else: #Set newly placed door's position based on direction.
                    if door.direction == 0: # N
                        door.relativeX = otherDoor.relativeX
                        door.relativeY = otherDoor.relativeY+1
                    elif door.direction == 1: # S
                        door.relativeX = otherDoor.relativeX
                        door.relativeY = otherDoor.relativeY-1
                    elif door.direction == 3: # W
                        door.relativeX = otherDoor.relativeX+1
                        door.relativeY = otherDoor.relativeY 
                    elif door.direction == 4: # E
                        door.relativeX = otherDoor.relativeX-1
                        door.relativeY = otherDoor.relativeY
                    door.parent.updatePosition(door)
                    roomsPositioned.add(door.parent)
        parents = set()  #Parents is a set of all rooms used in the current permutaiton.
        for i in tmp:
            for j in i:
                parents.add(j.parent)
        xFactor = 0 # Amount to adjust each room's x position by.
        yFactor = 0 # Amount to adjust each room's y position by.
        xMax = 0 # find out how "large" the permutaiton is to create the canvas.
        yMax = 0
        for room in parents: #Updating all positions to be positive.
            if room.relativeX <= xFactor:
                xFactor = room.relativeX - room.roomSize['x']
            if room.relativeY <= yFactor:
                yFactor = room.relativeY - room.roomSize['y']
            if room.relativeX > xMax:
                xMax = room.relativeX 
            if room.relativeY > yMax:
                yMax = room.relativeY 
        xFactor = abs(xFactor) +3 # +3s and +2s create a little extra room which helps the
        yFactor = abs(yFactor) +3 # rooms draw more smoothly. Could be removed with effort. TODO
        xMax += xFactor +2
        yMax += yFactor +2
        for room in parents:  # Move each room by a factor of x and y factor.
            room.relativeX += xFactor
            room.relativeY += yFactor
            for door in room.doorPositions: # adjust the position of each room's doors.
                door.relativeX += xFactor
                door.relativeY += yFactor
        pixelsPerTile = 25 # Pixel size of each square tile in the image.
        self.oldPerms.append(tmp) # Add tmp to list of permutations already shown.
        img = Image.new('RGB', (xMax*pixelsPerTile+1, yMax*pixelsPerTile+1), (256, 256, 256)) #Create canvas.
        draw = ImageDraw.Draw(img) 
        doors = [] # Spot to place all the doors that need to be drawn.
        roomTiles = [] # Spot to place all the room tiles which need to be drawn.
        for room in parents:
            for door in room.doorPositions:
                x = (door.relativeX)
                y = (door.relativeY)
                doors.append((x, y))
            for i in range(room.relativeX-room.roomSize['x'], room.relativeX+1):
                for j in range(room.relativeY-room.roomSize['y'], room.relativeY+1):
                    roomTiles.append((i, j))
        for i in range(xMax): # Go through each tile up to the max size.
            for j in range(yMax):
                imod = i*pixelsPerTile # calculates tile position on the canvas
                jmod = j*pixelsPerTile
                if (i, j) in roomTiles: # If current tile is a room tile paint red.
                    shape = [(imod, jmod), (imod+pixelsPerTile, jmod+pixelsPerTile)]
                    color = '#ff785a' # red
                    draw.rectangle(shape, fill=color, outline='black')
                if (i, j) in doors: # if current tile is  a door paint green.
                    shape = [(imod, jmod), (imod+pixelsPerTile, jmod+pixelsPerTile)]
                    color = '#187225' # green
                    draw.rectangle(shape, fill=color, outline='black')
        for i in parents: # Outline all the rooms. Probably could combine these two loops. TODO 
            shape = [((i.relativeX-i.roomSize['x'])*pixelsPerTile, (i.relativeY-i.roomSize['y'])*pixelsPerTile), ((i.relativeX+1)*pixelsPerTile, (i.relativeY+1)*pixelsPerTile)]
            color = '#1C3144'
            draw.rectangle(shape, outline=color, width=3)
        img = ImageTk.PhotoImage(img)
        for room in parents:  # Reset door and room positions.
            room.relativeX = room.roomSize['x']
            room.relativeY = room.roomSize['y']
            for door in room.doorPositions:
                door.relativeX = door.xpos
                door.relativeY = door.ypos
        return img

    def nextPerm(self):
        '''
        Calls drawlayout to get next permutation image and displays the image.

        Parameters:
            None
        '''
        img = self.drawLayout(self.allPerms)
        self.outputLabel.configure(image = img)
        self.outputLabel.image = img
        
    #LEFT CLICK BUTTON ACTION
    def gridButtonLeftWrapper(self, i, j): 
        return lambda Button: self.gridButtonLeft(self.btns[i][j])
    def gridButtonLeft(self, btn):
        '''
        Activates on left click, updates grid to show size of selection and adds size to current room.

        Parameters:
            btn (Button): button which is clicked gets passed in to get location.
        '''
        if self.roomSize != {'x':0,'y':0}:
            self.currDoor = None
            self.clearSize()
        self.roomSize['x'] = btn['xpos']
        self.roomSize['y'] = btn['ypos']
        self.updateIcons(btn['xpos'], btn['ypos'], self.icons['selected'])
        
    #RIGHT CLICK BUTTON ACTION
    def gridButtonRightWrapper(self, i, j):
        return lambda Button: self.gridButtonRight(self.btns[i][j])
    def gridButtonRight(self, btn):
        '''
        Activates on right click. Checks if location is a valid spot for a door, places the door.
        
        Parameters:
            btn (Button): button which is clicked gets passed in to get location.
        '''
        validDoor = False
        direction = None
        x = btn['xpos']
        y = btn['ypos']
        #TODO Currently corners aren't handled.  Prioritizes vertical travel.
        #Directions: 0=North, 1=South, 4=East, 3=West.
        if y == 0 and x <= self.roomSize['x']: #North wall,
            validDoor = True
            direction = 0
        elif y == self.roomSize['y'] and x <= self.roomSize['x']: #South wall,
            validDoor = True
            direction = 1
        elif x == 0 and y <= self.roomSize['y']: #West wall,
            validDoor = True
            direction = 3
        elif x == self.roomSize['x'] and y <= self.roomSize['y']: #East wall,
            validDoor = True
            direction = 4

        if validDoor:
            if self.currDoor is not None: #if door already selected, delete prev selection.
                self.updateIcons(self.currDoor['x'], self.currDoor['y'], self.icons['selected'], batch=False, updateDoors=True)
                self.currDoor = dict({})
            self.currDoor = {'x':x,'y':y,'direction':direction}
            self.updateIcons(x, y, self.icons['hl_door'], batch=False)

    def updateIcons(self, x, y, icon, batch=True, updateDoors=False):
        '''
        Updates icons on the button grid.

        Parameters:
            x (int): x coordinate of furthest right button to be updated.
            y (int): y coordinate of furthest down button to be updated.
            icon (Image): icon which should replace all updated buttons.
            batch (Boolean): determines whether all tiles through the x,y shoud be updated or the singular tile.
            updateDoors (Boolean): determines whether doors should be removed from button grid or updated.            
        '''
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

    def resetBtn(self):
        '''
        Clears size of current room, resets permutations and rooms. Clears grid.

        Parameters:
            None
        '''
        self.clearSize()
        self.allPerms = []
        self.allRooms = []
        self.oldPerms = []
        self.outputLabel.configure(image=self.icons['white'])
        self.updateViewFrame()

    def clearSize(self):
        '''
        Removes all doors, current door, updates icons, and sets room size to 0.

        Parameters:
            None
        '''
        self.allDoors = []
        self.currDoor = None
        self.updateIcons(self.roomSize['x'], self.roomSize['y'], self.icons['default'])
        self.roomSize['x'] = 0
        self.roomSize['y'] = 0
    
    def updateViewFrame(self):
        '''
        Displays created rooms on the right hand side of input screen.

        Parameters:
            None
        '''
        
        for label in self.roomLbls:
            label.destroy()
        for i in range(len(self.allRooms)):
            img = self.allRooms[i].img
            label = Label(self.viewFrame, image=img)
            label.image = img
            label.grid(row = i) 
            self.roomLbls.append(label)

    def permuteBtn(self):
        '''
        Sets allperms to a list of valid permutations based on all created rooms.

        Parameters:
            None
        '''
        
        if len(self.allRooms) <= 1:
            messagebox.showinfo("Invalid Submission","Must have at least 2 rooms created.")
        else:
            valids = self.validDoorConnections(self.allRooms)
            perms = permutations(valids, len(self.allRooms)-1)
            goodPerms = set()
            t1 = time.time()
            for i in perms:
                if self.isValidPerm(i):
                    goodPerms.add(frozenset(i))
            goodPerms = list(goodPerms)
            t2 = time.time() 
            self.allPerms = goodPerms
            self.outputLabel.configure(image=self.icons['perms'])

    def isValidPerm(self, perm):
        '''
        Determines if a permutation contains impossble combinations.

        Parameters:
            perm (List): List of tuples containing door pairs.

        Returns:
            Boolean
        '''
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
        '''
        Checks if a room is properly created and then submits it too the list of all rooms.

        Parameters:
            None
        '''
        check1 = False
        check2 = False
        if self.roomSize['x'] != 0 and self.roomSize['y'] != 0:
            check1 = True
        if len(self.allDoors) > 0:
            check2 = True
        if check1 and check2:
            r = Room(roomSize=dict(self.roomSize), doorPositions=self.allDoors)
            for i in r.doorPositions:
                i.parent = r # adding reference to parent.
            self.allRooms.append(r)
            r.roomIndex = len(self.allRooms) - 1
            self.updateViewFrame()
            self.clearSize()
        else: 
            messagebox.showinfo("Invalid Submission","Minimum room size is 2x2\nAnd rooms must contain at least one door.")

    def confirmDoor(self):
        '''
        Submits door as a valid door to the Room's list of doors.

        Parameters:
            None
        '''
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