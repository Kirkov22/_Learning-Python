# Week 01 project - Rock Paper Scissors Lizard Spock
# Paste code into www.codeskulptor.org to see it run

import random # generate random numbers

#Convert name string to number per these rules:
# 0 <- rock
# 1 <- Spock
# 2 <-  paper
# 3 <- lizard
# 4 <- scissors
def name_to_number(name):
  if (name == 'rock'):
    return 0
  elif (name == 'Spock'):
    return 1
  elif (name == 'paper'):
    return 2
  elif (name == 'lizard'):
    return 3
  elif (name == 'scissors'):
    return 4
  else:
    return -1

#Convert number to name string per these rules:
# 0 -> rock
# 1 -> Spock
# 2 -> paper
# 3 -> lizard
# 4 -> scissors
def number_to_name(num):
  if (num == 0):
    return 'rock'
  elif (num == 1):
    return 'Spock'
  elif (num == 2):
    return 'paper'
  elif (num == 3):
    return 'lizard'
  elif (num == 4):
    return 'scissors'
  else:
    return -1

#Play a game of Rock-Paper-Scissors-Lizard-Spock against a computer
def rpsls(name):
  #convert player's choice to number
  player = name_to_number(name)
  print "Player chooses", name
    
  #make sure player made a valid choice
  if (player == -1):
    print "Invalid player choice.  Should be one of ['rock' 'paper' 'scissors' 'lizard' 'Spock']"
  else:
    #get computer's choice
    comp = random.randrange(0, 5, 1)
    print "Computer chooses", number_to_name(comp)
    
    #calculate & print result
    result = (player - comp) % 5
    if (result == 0): #tie
      print "Player and computer tie!"
    elif (result < 3):
      print "Player wins!"
    else:
      print "Computer wins!"
    
  print

# test the function code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
