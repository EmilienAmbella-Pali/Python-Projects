import pygame
from random import randint
from pygame import QUIT, MOUSEBUTTONUP
from pygame.time import get_ticks
import math

# User-defined functions
def main():
    game = Game()
    game.play()

# User-defined classes
class Game:
    # An object in this class represents a complete game.

    def __init__(self):
        # Initialize a Game.
        # - self is the Game to initialize
        
        pygame.init()
        self._window = pygame.display.set_mode((500, 400))
        pygame.display.set_caption('Poke the Dots')
        self._frame_rate = 90  # larger is faster game
        self._close_selected = False
        self._game_over = False
        self._clock = pygame.time.Clock()
        self._small_dot = Dot('red', [50, 75], 30, [1, 2], self._window)
        self._big_dot = Dot('blue', [200, 100], 40, [2, 1], self._window)
        self._small_dot.randomize()
        self._big_dot.randomize()
        self._score = 0
        self._font = pygame.font.SysFont('Arial', 64)
        
    def play(self):
        # Play the game until the player presses the close icon
        # and then close the window.
        # - self is the Game to play

        while not self._close_selected and not self._game_over:
            # play frame
            self.handle_events()
            self.draw()
            self.update()
        if self._game_over:
            self.display_game_over()
        pygame.quit()
           
    def handle_events(self):
        # Handle the current game events by changing the game
        # state appropriately.
        # - self is the Game whose events will be handled

        event_list = pygame.event.get()
        for event in event_list:
            self.handle_one_event(event)
            
    def handle_one_event(self, event):
        # Handle one event by changing the game state
        # appropriately.
        # - self is the Game whose event will be handled
        # - event is the Event object to handle
            
        if event.type == QUIT:
            self._close_selected = True
        elif event.type == MOUSEBUTTONUP:
            self.handle_mouse_up(event)

    def handle_mouse_up(self, event):
        # Respond to the player releasing the mouse button by
        # taking appropriate actions.
        # - self is the Game where the mouse up occurred
        # - event is the Event object to handle

        self._small_dot.randomize()
        self._big_dot.randomize()
 
    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw
        
        self._window.fill((0, 0, 0))  # fill the window with black
        self.draw_score()
        self._small_dot.draw()
        self._big_dot.draw()
        pygame.display.update()
                        
    def update(self):
        # Update all game objects with state changes
        # that are not due to user events.
        # - self is the Game to update

        self._small_dot.move()
        self._big_dot.move()
        self._clock.tick(self._frame_rate)
        self._score = get_ticks() // 1000 

        if self.check_collision():
            self._game_over = True
        self.increase_difficulty()

    def draw_score(self):
        # Draw the time since the game began as a score.
        # - self is the Game to draw for
        
        score_text = self._font.render(f'Score: {self._score}', True, (255, 255, 255))
        self._window.blit(score_text, (0, 0))
        
    def check_collision(self):
        # Check if the two dots collide.
        # - self is the Game to check the collision for
        
        small_dot_center = self._small_dot.get_center()
        big_dot_center = self._big_dot.get_center()
        
        # Calculate the distance between the centres of the dots
        distance = math.sqrt((small_dot_center[0] - big_dot_center[0])**2 +
                             (small_dot_center[1] - big_dot_center[1])**2)
        
        # Sum of the radii of both dots
        radius_sum = self._small_dot.get_radius() + self._big_dot.get_radius()
        
        # If the distance is less than the sum of the radii, there is a collision
        return distance < radius_sum
    
    def increase_difficulty(self):
        # Increase the difficulty over time by gradually increasing the dot speeds.
        # - self is the Game to increase the difficulty for
        
        if self._score % 10 == 0 and self._score > 0:  # Increase speed every 10 seconds
            self._small_dot.increase_speed()
            self._big_dot.increase_speed()

    def display_game_over(self):
        # Display the Game Over screen with the final score.
        # - self is the Game to display the game over for
        
        self._window.fill((0, 0, 0))
        game_over_text = self._font.render(f"Game Over! Final Score: {self._score}", True, (255, 255, 255))
        self._window.blit(game_over_text, (100, 150))
        pygame.display.update()

class Dot:
    # An object in this class represents a coloured circle
    # that can move.

    def __init__(self, color, center, radius, velocity, window):
        # Initialize a Dot.
        # - self is the Dot to initialize
        # - color is the str colour of the dot
        # - center is a list containing the x and y int
        # coords of the centre of the dot
        # - radius is the int pixel radius of the dot
        # - velocity is a list containing the x and y components
        # - window is the game's Window

        self._color = color
        self._center = center
        self._radius = radius
        self._velocity = velocity
        self._window = window

    def move(self):
        # Change the location and the velocity of the Dot so it
        # remains on the surface by bouncing from its edges.
        # - self is the Dot

        size = (self._window.get_width(), self._window.get_height())
        for index in range(0, 2):
            # update centre at index
            self._center[index] = self._center[index] + self._velocity[index]
            # dot perimeter outside window?
            if (self._center[index] < self._radius) or (self._center[index] + self._radius > size[index]):
                # change direction
                self._velocity[index] = -self._velocity[index]

    def draw(self):
        # Draw the dot on the surface.
        # - self is the Dot

        pygame.draw.circle(self._window, pygame.Color(self._color), self._center, self._radius)

    def randomize(self):
        # Change the dot so that its centre is at a random
        # point on the surface. Ensure that no part of a dot
        # extends beyond the surface boundary.
        # - self is the Dot

        size = (self._window.get_width(), self._window.get_height())
        for index in range(0, 2):
            self._center[index] = randint(self._radius, size[index] - self._radius)
    
    def get_center(self):
        # Get the current centre of the dot
        return self._center
    
    def get_radius(self):
        # Get the radius of the dot
        return self._radius

    def get_rect(self):
        # Return a pygame Rect object representing the dot's area
        # - self is the Dot

        return pygame.Rect(self._center[0] - self._radius, self._center[1] - self._radius, self._radius * 2, self._radius * 2)

    def increase_speed(self):
        # Increase the dot's speed over time.
        # - self is the Dot to increase speed for

        self._velocity[0] += 1 if self._velocity[0] > 0 else -1
        self._velocity[1] += 1 if self._velocity[1] > 0 else -1

main()
