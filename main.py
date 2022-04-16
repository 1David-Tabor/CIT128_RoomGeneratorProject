#!/usr/bin/env python3
'''
    Rio Hondo College
    CIT 128: Python Programming II
    Student Directed Project
'''
import tkinter as tk

class Room():
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
        self.screen_width = (int(self.winfo_screenwidth() * winSizeMulti))
        self.screen_height = (int(self.winfo_screenheight() * winSizeMulti))
        self.geometry(f"{self.screen_width}x{self.screen_height}")

        self.greeting = tk.Label(self, text=self.labeltext)
        self.greeting.pack()



a = LayoutGenerator()
a.mainloop()

#Testing permutation
