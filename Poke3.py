# Poke The Dots Version 3
# This is a graphical game where two dots move around
# the screen, bouncing off the edges. The user tries 
# to prevent the dots from colliding by pressing and 
# releasing the mouse button to teleport the dots to 
# a random location. The score is the number of seconds 
# from the start of the game.

from uagame import Window
from random import randint
from pygame import QUIT, Color, MOUSEBUTTONUP
from pygame.time import Clock, get_ticks
from pygame.event import get as get_events
from pygame.draw import circle as draw_circle

# User-defined functions

def main():
    window = create_window()
    game = create_game(window)
    play_game(game) 
    window.close()
    
def create_window():
    # Create a window for the game, open it, and return it.

    window = Window('Poke the Dots', 500, 400)
    window.set_font_name('ariel')
    window.set_font_size(64)
    window.set_font_color('white')
    window.set_bg_color('black')
    return window

def create_game(window):
    # Create a Game object for Poke the Dots.
    # - window is the Window that the game is played in
    
    game = Game()
    game.window = window
    game.frame_rate = 90  # larger is faster game
    game.close_selected = False
    game.clock = Clock()
    game.small_dot = create_dot('red', [50,75], 30, [1,2], window)
    game.big_dot = create_dot('blue', [200,100], 40, [2,1], window)
    randomize_dot(game.small_dot)
    randomize_dot(game.big_dot)
    game.score = 0
    return game

def create_dot(color, center, radius, speed, window):
    # Create a Dot object for Poke the Dots.
    # - color is the str color of the dot
    # - center is a list containing the x and y int
    # coords of the center of the dot
    # - radius is the int pixel radius of the dot
    # - speed is a list containing the x and y components
    # - window is the Window that the game is played in

    dot = Dot()
    dot.color = color
    dot.center = center
    dot.radius = radius
    dot.velocity = speed
    dot.window = window
    return dot
                    
def play_game(game):
    # Play the game until the player presses the close icon.
    # - game is the Game to play

    while not game.close_selected:
        # play frame
        handle_events(game)
        draw_game(game)
        update_game(game)
           
def handle_events(game):
    # Handle the current game events by changing the game
    # state appropriately.
    # - game is the Game whose events will be handled
    
    event_list = get_events()
    for event in event_list:
        #handle one event
        if event.type == QUIT:
            game.close_selected = True
        elif event.type == MOUSEBUTTONUP:
            handle_mouse_up(game)
                                
def handle_mouse_up(game):
    # Respond to the player releasing the mouse button by
    # taking appropriate actions.
    # - game is the Game where the mouse up occured
    # - event is the Event object to handle

    randomize_dot(game.small_dot)
    randomize_dot(game.big_dot)
 
def draw_game(game):
    # Draw all game objects.
    # - game is the Game to draw for
    
    game.window.clear()
    draw_score(game)
    draw_dot(game.small_dot)
    draw_dot(game.big_dot)
    game.window.update()

def draw_score(game):
    # Draw the time since the game began as a score.
    # - game is the Game to draw for
    
    string = 'Score: ' + str(game.score)
    game.window.draw_string(string, 0, 0)
                    
def update_game(game):
    # Update all game objects with state changes
    # that are not due to user events.
    # - game is the Game to update

    move_dot(game.small_dot)
    move_dot(game.big_dot)
    game.clock.tick(game.frame_rate)
    game.score = get_ticks() // 1000 

def draw_dot(dot):
    # Draw the dot on the window.
    # - dot is the Dot to draw

    surface = dot.window.get_surface()
    color = Color(dot.color)
    draw_circle(surface, color, dot.center, dot.radius)

def move_dot(dot):
    # Change the location and the velocity of the Dot so it
    # remains on the surface by bouncing from its edges.
    # - dot is the Dot to move

    size = (dot.window.get_width(), dot.window.get_height())
    for index in range(0, 2):
        # update center at index
        dot.center[index] = dot.center[index] + dot.velocity[index]
        # dot edge outside window?
        if (dot.center[index] < dot.radius) or (dot.center[index] + dot.radius > size[index]):
            # change direction
            dot.velocity[index] = - dot.velocity[index]
                 
def randomize_dot(dot):
    # Change the dot so that its center is at a random
    # point on the surface. Ensure that no part of a dot
    # extends beyond the surface boundary.
    # - dot is the Dot to randomize

    size = (dot.window.get_width(), dot.window.get_height())
    for index in range(0, 2):
        dot.center[index] = randint(dot.radius, size[index] - dot.radius)

class Game:
    # An object in this class represents a complete game.
    # - window
    # - frame_rate
    # - close_selected
    # - clock
    # - small_dot
    # - big_bot
    # - score
    
    pass

class Dot:
    # An object in this class represents a colored circle
    # that can move.
    # - color
    # - center
    # - radius
    # - velocity
    # - window

    pass
        
main()