# Week 05 Project - Memory Match
# Paste into www.codeskulptor.org to see it run

# ------------------------
# --- Import Libraries ---
# ------------------------
import random
import simplegui

# ---------------------------
# --- Define Global State ---
# ---------------------------

set = range(8)
deck = set + set
card_space = 0
exposed = [False] * len(deck)
game_state = 0
first_exposed_index = 0
second_exposed_index = 0
matches = 0
turns = 0

#Canvas
HEIGHT = 100
WIDTH = 600
FONT_SIZE = 28
FONT_FACE = 'monospace'

# ------------------------
# --- Helper Functions ---
# ------------------------

# Restart the game
def new_game():
    global deck, card_space, exposed, game_state, matches, turns
    random.shuffle(deck)
    card_space = get_card_space(deck)
    exposed = [False] * len(deck)
    game_state = 0
    matches = 0
    turns = 0
    pass

# Increment the game state machine
def next_step(index):
    global deck, exposed, game_state, matches, turns
    global first_exposed_index, second_exposed_index
    
    # new game
    if (game_state == 0):
        if (not exposed[index]):
          
            exposed[index] = True
            first_exposed_index = index
            game_state = 1
    
    # 1 'new' exposed card
    elif (game_state == 1):
        
        if (index != first_exposed_index and \
            not exposed[index]):
            
            exposed[index] = True
            second_exposed_index = index
            turns += 1
            if (deck[first_exposed_index] == \
                deck[second_exposed_index]):
                
                matches += 1
            game_state = 2
    
    # 2 exposed cards
    elif (game_state == 2):
        
        if (deck[first_exposed_index] != \
            deck[second_exposed_index]):
            
            if (not exposed[index] or \
                index == first_exposed_index or \
                index == second_exposed_index):
                
                exposed[first_exposed_index] = False
                exposed[second_exposed_index] = False
                exposed[index] = True
                first_exposed_index = index
                game_state = 1
                
        else:
            
            if (matches >= len(deck) // 2):
                
                game_state = 3
            elif (not exposed[index]):
                
                exposed[index] = True
                first_exposed_index = index
                game_state = 1
    else:
        game_state = 3
    pass

#Calculate the spacing to give each card
def get_card_space(deck):
    return WIDTH // len(deck)

#Return the X coordinate of text such that the text is centered
# within the width given by space
def center(text, space):
    return (space - frame.get_canvas_textwidth(text, FONT_SIZE, FONT_FACE)) // 2

# Return a rectangle with the lower left-corner given by x,y
#  and the width given by space
def rectangle(x, y, space):
    lwr_left = [x + 2, y + 2]
    lwr_right = [x + space - 2, y + 2]
    upr_right = [x + space - 2, y - FONT_SIZE - 2]
    upr_left = [x + 2, y - FONT_SIZE - 2]
    return [lwr_left, lwr_right, upr_right, upr_left]

# -----------------------
# --- Define Handlers ---
# -----------------------

# draw the deck and frames
def draw_handler(canvas):
    global deck, card_space, matches, turns
    
    space = (WIDTH - card_space * len(deck)) // 2
    
    card_y = (HEIGHT + FONT_SIZE) // 2
    for index, card in enumerate(deck):
        if (exposed[index]):
            text = str(card)
            card_x = space + center(text, card_space)
            canvas.draw_text(text, [card_x, card_y - 4], FONT_SIZE, 'red', FONT_FACE)
            canvas.draw_polygon(rectangle(space, card_y, card_space), 1, 'green')
        else:
            canvas.draw_polygon(rectangle(space, card_y, card_space), 1, 'green', 'green')
        space += card_space
        
    label.set_text('Turns Taken: ' + str(turns))
    pass

# mouse handler
def mouse_handler(position):
    global deck, card_space
    
    if (position[1] >= ((HEIGHT - FONT_SIZE) // 2 - 2) and \
        position[1] < ((HEIGHT + FONT_SIZE) // 2 + 2)):
        
        offset_x = position[0] - (WIDTH - card_space * len(deck)) // 2
        index = offset_x / card_space
        
        if (index >= 0 and index < len(deck)):
            
            margin = offset_x % card_space
            if (margin > 2 and margin < (card_space - 2)):
                next_step(index)
    pass

# resets the timer, # attempts, and # successes to 0
def reset():
    new_game()    
    pass

# --------------------
# --- Create Frame ---
# --------------------

frame = simplegui.create_frame('Memory', WIDTH, HEIGHT)

# -------------------------
# --- Register Handlers ---
# -------------------------

frame.set_draw_handler(draw_handler)
frame.set_mouseclick_handler(mouse_handler)
label = frame.add_label('Turns Taken: 0')
frame.add_button('RESET', reset, 75)


# ----------------------------
# --- Start Frame & Timers ---
# ----------------------------

frame.start()
new_game()
