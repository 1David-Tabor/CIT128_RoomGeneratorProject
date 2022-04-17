#!/usr/bin/env python3
'''
    Rio Hondo College
    CIT 128: Python Programming II
    Student Directed Project
'''
import tkinter as tk
from tkinter import ttk, Frame

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
        self.screen_width = (int(self.winfo_screenwidth() * winSizeMulti))
        self.screen_height = (int(self.winfo_screenheight() * winSizeMulti))
        self.geometry(f"{self.screen_width}x{self.screen_height}")

        #Creating tabs for input, output, and help page.
        tabs = ttk.Notebook(self)
        tabs.pack()
        
        inputFrame = Frame(tabs, width=self.screen_width, height=self.screen_width)
        inputFrame.pack(fill='both', expand=True)
        outputFrame = Frame(tabs, width=self.screen_width, height=self.screen_width)
        outputFrame.pack(fill='both', expand=True)
        helpFrame = Frame(tabs, width=self.screen_width, height=self.screen_width)
        helpFrame.pack(fill='both', expand=True)

        tabs.add(inputFrame, text='Input')
        tabs.add(outputFrame, text='Output')
        tabs.add(helpFrame, text='Help')


        self.labeltext = "hi"
        self.greeting = tk.Label(inputFrame, text=self.labeltext)
        self.greeting.pack()




a = LayoutGenerator()
a.mainloop()

