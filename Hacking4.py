# Hacking Version 4
# This is a graphical password guessing game that displays a 
# list of potential computer passwords. The player is allowed 
# 1 attempt to guess the password. The game indicates whether 
# the player successfully guessed the password or not.

from uagame import Window
from time import sleep

# create window
window = Window('Hacking', 600, 500)
window.set_font_name('couriernew')
window.set_font_size(18)
window.set_font_color('green')
window.set_bg_color('black')
    
# display header
pause_time = 0.3
line_x = 0
line_y = 0
string_height = window.get_font_height()
header = ['DEBUG MODE', '1 ATTEMPT(S) LEFT', '']
for header_line in header:
    # display header line
    window.draw_string(header_line, line_x, line_y)
    window.update()
    sleep(pause_time)
    line_y = line_y + string_height

# display password list
#   create password list
password_list = ['PROVIDE', 'SETTING', 'CANTINA', 'CUTTING', 'HUNTERS', 'SURVIVE',  'HEARING', 'HUNTING', 'REALIZE', 'NOTHING', 'OVERLAP', 'FINDING', 'PUTTING', '']
for password in password_list:
    # display password line
    window.draw_string(password, line_x, line_y)
    window.update()
    sleep(pause_time)
    line_y = line_y + string_height

#   choose password
password = password_list[7]
    
# prompt for guess
prompt = 'ENTER PASSWORD >'
guess = window.input_string(prompt, line_x, line_y)
line_y = line_y + string_height
    
# end game
#   clear window
window.clear()

#   create outcome
if guess == password:
    # create success
    outcome = [guess, '', 'EXITING DEBUG MODE', '', 'LOGIN SUCCESSFUL - WELCOME BACK', '']
    prompt = 'PRESS ENTER TO CONTINUE'
else:
    # create failure
    outcome = [guess, '', 'LOGIN FAILURE - TERMINAL LOCKED', '','PLEASE CONTACT AN ADMINISTRATOR', '']
    prompt = 'PRESS ENTER TO EXIT'
        
#   display outcome 
#      compute y coordinate
outcome_height = (len(outcome) + 1)*string_height
y_space = window.get_height() - outcome_height
line_y = y_space // 2

for outcome_line in outcome:
    # display centered outcome line
    #    compute x coordinate
    x_space = window.get_width() - window.get_string_width(outcome_line)
    line_x = x_space // 2
    
    window.draw_string(outcome_line, line_x, line_y)
    window.update()
    sleep(pause_time)
    line_y = line_y + string_height   

#   prompt for end
x_space = window.get_width() - window.get_string_width(prompt)
line_x = x_space // 2
window.input_string(prompt, line_x, line_y)

#   close window
window.close()