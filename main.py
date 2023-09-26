import tkinter as tk
from tkinter import simpledialog

# Function to toggle the button state
def toggle_button_state():
    if button.config('text')[-1] == 'On':
        button.config(text='Off', relief=tk.RAISED, bg='red')
        #This will be used to 
    else:
        button.config(text='On', relief=tk.SUNKEN, bg='green')
        

# Function to update the counter
def update_count():
    global counter, timer_seconds
    counter += 1
    timer_seconds += 5
    counter_label.config(text=f"Count: {counter}")
    update_timer_label()

# Function to update the timer label
def update_timer_label():
    global timer_seconds
    timer_label.config(text=f"Timer: {timer_seconds} seconds")

# Function to update the timer
def update_timer():
    global timer_seconds
    if timer_running:
        timer_seconds += 1
        update_timer_label()
        timer_label.after(1000, update_timer)

# Function to stop the timer (Game Over)
def game_over():
    global timer_running, timer_seconds
    timer_running = False
    save_to_leaderboard(timer_seconds)

# Function to save time to the leaderboard
def save_to_leaderboard(time):
    global leaderboard
    name = simpledialog.askstring("Leaderboard", "Enter your name:")
    if name:
        leaderboard.append({'name': name, 'time': time})
        leaderboard.sort(key=lambda x: x['time'])  # Sort the leaderboard by time
        display_leaderboard()

# Function to display the leaderboard
def display_leaderboard():
    global leaderboard
    leaderboard_window = tk.Toplevel(root)
    leaderboard_window.title("Leaderboard")

    leaderboard_label = tk.Label(leaderboard_window, text="Leaderboard")
    leaderboard_label.pack()

    for entry in leaderboard:
        entry_label = tk.Label(leaderboard_window, text=f"{entry['name']}: {entry['time']} seconds")
        entry_label.pack()

# Initialize the counter, timer, and timer status
counter = 0
timer_seconds = 0
timer_running = True
leaderboard = []

# Create the main window
root = tk.Tk()
root.title("On/Off Button with Counter, Timer, and Leaderboard")

# Create a button with initial state 'On'
button = tk.Button(root, text='On', relief=tk.SUNKEN, bg='green', command=toggle_button_state)
button.pack(padx=20, pady=10)

# Create a label to display the counter
counter_label = tk.Label(root, text=f"Count: {counter}")
counter_label.pack()

# Create a button to update the counter
update_button = tk.Button(root, text='Update Count', command=update_count)
update_button.pack(padx=20, pady=10)

# Create a label to display the timer
timer_label = tk.Label(root, text=f"Timer: {timer_seconds} seconds")
timer_label.pack()

# Create a "Game Over" button
game_over_button = tk.Button(root, text='Game Over', command=game_over)
game_over_button.pack(padx=20, pady=10)

# Start the timer counting up when the program starts
update_timer()

# Start the Tkinter event loop
root.mainloop()
