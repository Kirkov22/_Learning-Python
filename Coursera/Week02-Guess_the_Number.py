# Week 02 Project - Guess the Number
# Paste code into www.codeskulptor.org to see it run

import random
import simplegui
import math

# Global Variables
secret_number = random.randrange(0, 100, 1)
range_low = 0
range_high = 100
guess_left = 0

# Start the game over with a new random number
def new_game():
   global secret_number, guess_left
    
   #reset guesses left
   guess_left = math.log((range_high - range_low) + 1, 2)
   guess_left = int(math.ceil(guess_left))
   print "Choosing new number"
   print "You have", guess_left, "guesses, good luck!"
   
   # Pick a new random number
   secret_number = random.randrange(range_low, range_high, 1)
   pass


# Change range to [0, 100) and restart
def range100():
   global range_low, range_high
   range_low = 0
   range_high = 100
   new_game()
   pass

# Change range to [0, 1000) and restart
def range1000():
   global range_low, range_high
   range_low = 0
   range_high = 1000
   new_game()
   pass

# Handle a guess from the user
def input_guess(guess):
  global guess_left
  
  # Convert guess string to int
  guess_num = int(guess)

  # Compare to the secret number
  if (guess_num == secret_number):
    print "Winner!"
    print
    new_game()
  elif (guess_left > 1):
    guess_left -= 1
    if (guess_num > secret_number):
      print "Lower ..."
    else:
      print "Higher ..."
      print "Guesses Left:", guess_left
  else:
    print "You lose - please try again."
    print
    new_game()

  pass

    
# create frame
frame = simplegui.create_frame("Guess the Number!", 100, 200)

# register event handlers for control elements
new_button100 = frame.add_button("New Game - [0, 100)", range100, 175)
new_button1000 = frame.add_button("New Game - [0, 1000)", range1000, 175)
guess_field = frame.add_input("Guess:", input_guess, 100)

# call new_game and start frame
frame.start
