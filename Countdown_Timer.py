import tkinter as tk
import time

def start_timer():
    try:
        # Get the time input from the user
        my_time = int(entry.get())

        if my_time < 0:
            label_result.config(text="Please enter a positive number of seconds.")
        else:
            # Start the countdown
            for x in range(my_time, 0, -1):
                seconds = x % 60
                minutes = int(x / 60) % 60
                hours = int(x / 3600)
                time_string = f'{hours:02}:{minutes:02}:{seconds:02}'
                label_result.config(text=time_string)
                window.update()  # Update the GUI
                time.sleep(1)

            label_result.config(text="TIME'S UP!")
    
    except ValueError:
        label_result.config(text="Please enter a valid number of seconds.")

# Set up the window
window = tk.Tk()
window.title("Countdown Timer")

# Set window size and style
window.geometry("300x150")
window.config(bg="#f0f0f0")

# Create and place widgets
label_instruction = tk.Label(window, text="Enter time in seconds:", bg="#f0f0f0", font=("Helvetica", 12))
label_instruction.pack(pady=10)

entry = tk.Entry(window, font=("Helvetica", 14), width=10)
entry.pack(pady=5)

button_start = tk.Button(window, text="Start", font=("Helvetica", 12), command=start_timer)
button_start.pack(pady=10)

label_result = tk.Label(window, text="", bg="#f0f0f0", font=("Helvetica", 20, "bold"))
label_result.pack(pady=5)

# Run the window loop
window.mainloop()
