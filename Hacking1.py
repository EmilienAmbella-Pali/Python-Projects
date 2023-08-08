# Hacking Version 1
# This is a text-based password guessing game that displays a
# list of potential computer passwords. The player is allowed
# 1 attempt to guess the password. The game indicates that the
# player failed to guess the password correctly

# display header
print('DEBUG MODE')
print('1 ATTEMPT(S) LEFT')
print('')

# display password
print('PROVIDE')
print('CAREFUL')
print('BELEIVE')
print('HUNTING')
print('SETTING')
print('COOKING')
print('FASTING')
print('DESTROY')
print('CAPTURE')
print('IMAGINE')
print('CREATOR')
print('PROVOKE')
print('ADVANCE')
print('')

# prompt for guess
import sys
valid_passwords = ['HUNTING']
password = input('ENTER PASSWORD > ')
if password in valid_passwords:
     print('')
     print('ACCESS DENIED')
     print('YOU HAVE 0 ATTEMPT(S) LEFT')
     print('PRESS ENTER FOR EXIT')
else:
     print('')
     print('ACCESS DENIED')
     print('YOU HAVE 0 ATTEMPT(S) LEFT')
     print('PRESS ENTER FOR EXIT')