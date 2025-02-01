import pygame
import time
import random

# Initialize pygame
pygame.init()

# Set up the game window
window_width = 600
window_height = 400
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Hangman Game')

# Set up fonts
font = pygame.font.SysFont('Arial', 40)
small_font = pygame.font.SysFont('Arial', 30)

# Set up colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# List of possible 6-letter words
words_list = ["python", "yellow", "orange", "planet", "friend", "winter", "summer", "guitar", "office", "forest"]

# Set up game variables
word = random.choice(words_list)  # Choose a random word
guesses = ''
turns = 10

# Function to display text on the screen
def draw_text(text, font, color, x, y):
    text_obj = font.render(text, True, color)
    window.blit(text_obj, (x, y))

# Function to display the word with guessed and unguessed characters
def display_word():
    word_display = ''
    for char in word:
        if char in guesses:
            word_display += char + ' '
        else:
            word_display += '_ '  # Show an underscore for unguessed characters
    draw_text(word_display, font, WHITE, 50, 150)

# Function to display incorrect guesses and remaining turns
def display_incorrect_guesses():
    draw_text(f'Incorrect guesses: {", ".join([g for g in guesses if g not in word])}', small_font, RED, 50, 200)
    draw_text(f'You have {turns} turns left', small_font, WHITE, 50, 250)

# Game loop
def game():
    global turns, guesses, word
    running = True
    guessed_incorrectly = False  # Flag to track incorrect guesses

    while running:
        window.fill(BLACK)  # Fill the screen with black

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                guess = pygame.key.name(event.key)  # Get the character of the pressed key
                if guess.isalpha() and len(guess) == 1:  # Only accept single alphabetic characters
                    if guess not in guesses:  # Make sure the guess is not repeated
                        guesses += guess.lower()

        # Display the word
        display_word()

        # Display incorrect guesses and turns left
        display_incorrect_guesses()

        # Check if the player has won
        if all(char in guesses for char in word):
            draw_text('You Won!', font, WHITE, 200, 300)
            pygame.display.update()
            time.sleep(2)
            running = False

        # Check if the player has lost
        if turns == 0:
            draw_text(f'You Lose! The word was: {word}', font, RED, 100, 300)
            pygame.display.update()
            time.sleep(2)
            running = False

        # Check if the guess is incorrect and update turns
        if len(guesses) > 0 and guesses[-1] not in word and guesses[-1] not in [g for g in word] and not guessed_incorrectly:
            turns -= 1  # Reduce turns if the guess is incorrect
            guessed_incorrectly = True  # Set flag to true so it doesn't reduce turns again for the same incorrect guess

        # Reset the flag after each loop to allow deduction for new incorrect guesses
        if guessed_incorrectly and guesses[-1] in word:
            guessed_incorrectly = False

        # Update the display
        pygame.display.update()

        # Set the game's speed
        pygame.time.Clock().tick(30)  # 30 frames per second

# Main entry point
def main():
    # Welcome screen
    window.fill(BLACK)
    draw_text('Welcome to Hangman!', font, WHITE, 150, 100)
    draw_text('Press any key to start...', small_font, WHITE, 150, 200)
    pygame.display.update()
    waiting = True

    # Wait for a key press to start the game
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            elif event.type == pygame.KEYDOWN:
                waiting = False
                game()  # Start the game when a key is pressed

# Run the game
if __name__ == "__main__":
    main()

    # Quit pygame when the game ends
    pygame.quit()
