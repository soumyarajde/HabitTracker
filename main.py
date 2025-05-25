import sys
import tkinter as tk
import logging
from habittracker.gui import ApplicationGui

if __name__=='__main__':
    
    logger = logging.getLogger()              
    logger.setLevel(logging.DEBUG)

    # setup logging formatting
    fmt = '%(asctime)s %(name)s %(levelname)s: %(message)s'
    datefmt = '%d-%m-%Y %H:%M:%S'
    formatter = logging.Formatter(fmt, datefmt=datefmt)

    # setup logging to file
    fh = logging.FileHandler("habittracker.log")
    fh.setLevel(logging.DEBUG)                        
    fh.setFormatter(formatter)

    # logging to stdout
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)                 
    ch.setFormatter(formatter)

    # Attach both handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    gui=tk.Tk()
    app=ApplicationGui(gui)
    gui.mainloop()
