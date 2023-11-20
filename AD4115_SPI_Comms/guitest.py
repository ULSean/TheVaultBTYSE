
from time import sleep
import time
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import Label, StringVar

# Create a Tkinter window
root = tk.Tk()
root.title("Laser Break Detector")

# Variables to store timer and laser breaks
timer_var = StringVar()
laser_break_var = StringVar()

def update_labels():
    timer_label.config(text="Timer: " + str(round(timer, 2)) + " seconds")
    laser_break_label.config(text="Laser Breaks: " + str(laser_break))
    root.after(1000, update_labels)  # Update every second
    
# Labels to display timer and laser breaks
timer_label = Label(root, textvariable=timer_var, font=("Helvetica", 16))
timer_label.pack(pady=10)
laser_break_label = Label(root, textvariable=laser_break_var, font=("Helvetica", 16))
laser_break_label.pack(pady=10)

timer = 0
penalty = 0
threshold = -80000
laser_break = 0

for x in range(40000):
    start = time.time()
    print(timer)
    end = time.time()
    timer = timer+(end-start)+penalty
    
    # Update GUI variables
    timer_var.set("Timer: " + str(round(timer, 2)) + " seconds")
    laser_break_var.set("Laser Breaks: " + str(laser_break))
    root.update()
        
print("number of lasers tripped = ", laser_break)
    
    
update_labels()

# Run the Tkinter main loop
root.mainloop()