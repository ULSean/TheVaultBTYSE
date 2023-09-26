import tkinter as tk
from tkinter import simpledialog

# Function to toggle the game state
def toggle_game_state():
    global timer_running, counter, timer_seconds
    if timer_running:
        # Game is running, so stop it
        timer_running = False
        game_over()
        button.config(text='Start', relief=tk.RAISED, bg='green')
    else:
        # Game is not running, so start it
        timer_running = True
        button.config(text='Stop', relief=tk.SUNKEN, bg='red')
        update_timer()

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
    
# Function to update the counter label
def update_counter_label():
    global counter
    counter_label.config(text=f"Laser Hit Count: {counter}")

# Function to update the timer
def update_timer():
    global timer_seconds
    if timer_running:
        timer_seconds += 1
        update_timer_label()
        timer_label.after(1000, update_timer)

# Function to stop the timer (Game Over)
def game_over():
    global timer_seconds, counter
    save_to_leaderboard(timer_seconds)
    timer_seconds = 0  # Reset the timer
    update_timer_label()  # Update the timer label
    counter = 0
    update_counter_label()

# Function to save time to the leaderboard and keep only the top 5 scores
def save_to_leaderboard(time):
    global leaderboard
    name = simpledialog.askstring("Leaderboard", "Enter your name:")
    if name:
        leaderboard.append({'name': name, 'time': time})
        leaderboard.sort(key=lambda x: x['time'])  # Sort the leaderboard by time
        leaderboard = leaderboard[:5]  # Keep only the top 5 scores
        display_leaderboard()

# Function to update the leaderboard display with the top 5 scores
def display_leaderboard():
    global leaderboard, leaderboard_frame
    leaderboard_frame.grid_forget()  # Hide the previous leaderboard frame

    leaderboard_frame = tk.Frame(root)
    leaderboard_frame.grid(row=0, column=1, padx=20)  # Place it on the right side

    leaderboard_label = tk.Label(leaderboard_frame, text="Leaderboard")
    leaderboard_label.pack()

    # Display only the top 5 scores
    for i, entry in enumerate(leaderboard):
        if i >= 5:
            break
        entry_label = tk.Label(leaderboard_frame, text=f"{entry['name']}: {entry['time']} seconds")
        entry_label.pack()

# Initialize the counter, timer, and timer status
counter = 0
timer_seconds = 0
timer_running = False  # Game is initially not running
leaderboard = []

# Create the main window
root = tk.Tk()
root.title("On/Off Button with Counter, Timer, and Leaderboard")

# Create a frame to hold the leaderboard
leaderboard_frame = tk.Frame(root)
leaderboard_frame.grid(row=0, column=1, padx=20)  # Place it on the right side

# Create a button with initial state 'Start'
button = tk.Button(root, text='Start', relief=tk.RAISED, bg='green', command=toggle_game_state)
button.grid(row=0, column=0, padx=20, pady=10)

# Create a label to display the counter
counter_label = tk.Label(root, text=f"Laser Hit Count: {counter}")
counter_label.grid(row=1, column=0, padx=20)

# Create a button to update the counter
update_button = tk.Button(root, text='Update Count', command=update_count)
update_button.grid(row=2, column=0, padx=20, pady=10)

# Create a label to display the timer
timer_label = tk.Label(root, text=f"Timer: {timer_seconds} seconds")
timer_label.grid(row=3, column=0, padx=20)

# Create a "Game Over" button
game_over_button = tk.Button(root, text='Game Over', command=game_over)
game_over_button.grid(row=4, column=0, padx=20, pady=10)

# Start the Tkinter event loop
root.mainloop()
