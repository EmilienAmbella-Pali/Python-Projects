# Poke The Dots Version 1
# This is a graphical game where two dots move around
# the screen, bouncing off the edges.

from uagame import Window
from pygame import QUIT, Color
from pygame.time import Clock
from pygame.event import get as get_events
from pygame.draw import circle as draw_circle

# User-defined functions

def main():
    window = create_window()
    # create game
    clock = Clock()
    small_color = 'red'
    small_radius = 30
    small_center = [50,75]
    small_velocity = [1,2]
    big_color = 'blue'
    big_radius = 40
    big_center = [200,100]
    big_velocity = [2,1]
    
    play_game(window, small_color, small_center, small_radius, small_velocity, big_color, big_center, big_radius, big_velocity, clock) 
    window.close()
    
def create_window():
    # Create a window for the game, open it, and return it.

    window = Window('Poke the Dots', 500, 400)
    window.set_bg_color('black')
    return window
                    
def play_game(window, small_color, small_center, small_radius, small_velocity, big_color, big_center, big_radius, big_velocity, clock):
    # Play the game until the player presses the close icon.
    # - window is the Window to play in
    # - small_color is the str color of the small dot
    # - small_center is the list of x int and y int coordinates
    # of the center of the small dot    
    # - small_radius is the int radius of the small dot
    # - small_velocity is the list of horizontal int and vertical
    # int speeds of the small dot
    # - big_color is the str color of the big dot
    # - big_center is the list of x int and y int coordinates
    # of the center of the big dot    
    # - big_radius is the int radius of the big dot
    # - big_velocity is the list of horizontal int and vertical
    # int speeds of the big dot
    # - clock is a Clock used to control game speed

    close_selected = False
    while not close_selected:
        # play frame
        close_selected = handle_events()
        draw_game(window, small_color, small_center, small_radius, big_color, big_center, big_radius)
        update_game(window, small_center, small_radius, small_velocity, big_center, big_radius, big_velocity, clock)
           
def handle_events():
    # Handle the current game events. Return True if the player
    # clicked the close icon and False otherwise.
    
    closed = False
    event_list = get_events()
    for event in event_list:
        # handle one event
        if event.type == QUIT:
            closed = True

    return closed
                
def draw_game(window, small_color, small_center, small_radius, big_color, big_center, big_radius):
    # Draw all game objects.
    # - window is the Window to draw in
    # - small_color is the str color of the small dot
    # - small_center is the list of x int and y int coordinates
    # of the center of the small dot    
    # - small_radius is the int radius of the small dot
    # - small_velocity is the list of horizontal int and vertical
    # int speeds of the small dot
    # - big_color is the str color of the big dot
    # - big_center is the list of x int and y int coordinates
    # of the center of the big dot    
    # - big_radius is the int radius of the big dot
    # - big_velocity is the list of horizontal int and vertical
    # int speeds of the big dot
    
    window.clear()
    draw_dot(window, small_color, small_center, small_radius)
    draw_dot(window, big_color, big_center, big_radius)
    window.update()
                    
def update_game(window, small_center, small_radius, small_velocity, big_center, big_radius, big_velocity, clock):
    # Update all game objects with state changes
    # that are not due to user events.
    # - window is the Window to move in
    # - small_center is the list of x int and y int coordinates
    # of the center of the small dot    
    # - small_radius is the int radius of the small dot
    # - small_velocity is the list of horizontal int and vertical
    # int speeds of the small dot
    # - big_center is the list of x int and y int coordinates
    # of the center of the big dot    
    # - big_radius is the int radius of the big dot
    # - big_velocity is the list of horizontal int and vertical
    # int speeds of the big dot
    # - clock is a Clock used to control game speed

    frame_rate = 90  # larger is faster game
    move_dot(window, small_center, small_radius, small_velocity)
    move_dot(window, big_center, big_radius, big_velocity)
    clock.tick(frame_rate)
                
def draw_dot(window, color_string, center, radius):
    # Draw the dot on the window.
    # - window is the Window to draw in
    # - color_string is the str color of the dot
    # - center is the list of x int and y int coordinates of the
    # center of the dot    
    # - radius is the int radius of the dot

    surface = window.get_surface()
    color = Color(color_string)
    draw_circle(surface, color, center, radius)

def move_dot(window, center, radius, velocity):
    # Change the location and the velocity of the dot so it
    # remains on the surface by bouncing from its edges.
    # - window is the Window to move in
    # - center is the list of x int and y int coordinates
    # of the center of the dot    
    # - radius is the int radius of the dot
    # - velocity is the list of horizontal int and vertical
    # int speeds of the dot

    size = (window.get_width(), window.get_height())
    for index in range(0, 2):
        # update center at index
        center[index] = center[index] + velocity[index]
        # dot edge outside window?
        if (center[index] <= radius) or (center[index] + radius >= size[index]):
            # change direction
            velocity[index] = - velocity[index]

main()