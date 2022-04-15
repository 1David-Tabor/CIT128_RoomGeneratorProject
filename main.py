#!/usr/bin/env python3
'''
    Rio Hondo College
    CIT 128: Python Programming II
    Student Directed Project
'''
import tkinter as tk

# Main app window
class LayoutGenerator(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title = 'Layout Generator'
        self.labeltext = 'Hello World'
        self.greeting = tk.Label(self, text=self.labeltext)
        self.greeting.pack()


a = LayoutGenerator()
a.mainloop()
