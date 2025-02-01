import tkinter as tk
import random

def play_game(user_choice):
    possible_actions = ["rock", "paper", "scissors"]
    computer_choice = random.choice(possible_actions)
    
    # Show user and computer choices
    label_choice.config(text=f"You chose {user_choice}, computer chose {computer_choice}.")
    
    # Determine the winner
    if user_choice == computer_choice:
        result = f"Both players selected {user_choice}. It's a tie!"
    elif user_choice == "rock":
        if computer_choice == "scissors":
            result = "Rock smashes scissors! You win!"
        else:
            result = "Paper covers rock! You lose."
    elif user_choice == "paper":
        if computer_choice == "rock":
            result = "Paper covers rock! You win!"
        else:
            result = "Scissors cuts paper! You lose."
    elif user_choice == "scissors":
        if computer_choice == "paper":
            result = "Scissors cuts paper! You win!"
        else:
            result = "Rock smashes scissors! You lose."
    
    label_result.config(text=result)

# Set up the window
window = tk.Tk()
window.title("Rock, Paper, Scissors")
window.geometry("400x300")
window.config(bg="#f0f0f0")

# Create and place widgets
label_instructions = tk.Label(window, text="Choose rock, paper, or scissors:", bg="#f0f0f0", font=("Helvetica", 14))
label_instructions.pack(pady=10)

# Create buttons for user choices
button_rock = tk.Button(window, text="Rock", font=("Helvetica", 12), command=lambda: play_game("rock"))
button_rock.pack(pady=5)

button_paper = tk.Button(window, text="Paper", font=("Helvetica", 12), command=lambda: play_game("paper"))
button_paper.pack(pady=5)

button_scissors = tk.Button(window, text="Scissors", font=("Helvetica", 12), command=lambda: play_game("scissors"))
button_scissors.pack(pady=5)

# Labels to show choices and result
label_choice = tk.Label(window, text="", bg="#f0f0f0", font=("Helvetica", 12))
label_choice.pack(pady=10)

label_result = tk.Label(window, text="", bg="#f0f0f0", font=("Helvetica", 14, "bold"))
label_result.pack(pady=10)

# Run the window loop
window.mainloop()
