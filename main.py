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

        self.greeting = tk.Label(self, text=self.labeltext)
        #self.greeting.pack()

        #Creating tabs for input, output, and help page.
        tabs = ttk.Notebook(self)
        tabs.pack()
        
        frame1 = Frame(tabs, width=self.screen_width, height=self.screen_width)
        frame1.pack(fill='both', expand=True)
        frame2 = Frame(tabs, width=self.screen_width, height=self.screen_width)
        frame2.pack(fill='both', expand=True)
        frame3 = Frame(tabs, width=self.screen_width, height=self.screen_width)
        frame3.pack(fill='both', expand=True)

        tabs.add(frame1, text='Input')
        tabs.add(frame2, text='Output')
        tabs.add(frame3, text='Help')




a = LayoutGenerator()
a.mainloop()

