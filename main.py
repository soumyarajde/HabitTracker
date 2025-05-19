import tkinter as tk
from habittracker.gui import ApplicationGui

if __name__=='__main__':
    gui=tk.Tk()
    app=ApplicationGui(gui)
    gui.mainloop()
