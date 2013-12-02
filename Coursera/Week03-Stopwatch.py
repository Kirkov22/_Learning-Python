# Week 03 Project - Stopwatch Game
# Paste into www.codeskulptor.org to see it run

# ------------------------
# --- Import Libraries ---
# ------------------------
import simplegui

# ---------------------------
# --- Define Global State ---
# ---------------------------
timer = None #assigned later
tenths = 0
attempts = 0
successes = 0
#GUI globals
interval = 100 #ms
canvas_width = 200
canvas_height = 200
font_size = 28
font_face = 'monospace'

# ------------------------
# --- Helper Functions ---
# ------------------------

# return a string representing time in the form M:SS.t
def format_tenths_to_string(tenth_s):
    #calculate component numbers
    tnths = tenth_s % 10
    secs = (tenth_s / 10) % 60
    mins = (tenth_s / 600)
    
    #return formatted string
    return str(mins) + ":" + str(secs / 10) + str(secs % 10) \
            + "." + str(tnths)

# return whether or not the counter is a whole second
def whole_second():
    return ((tenths % 10) == 0)

# return a set of coordinates to center text
def center(text):
    global canvas_width, canvas_height, font_size, font_face
    
    text_width = frame.get_canvas_textwidth(text, font_size, font_face)
    x = (canvas_width - text_width) / 2
    y = canvas_height / 2
    
    return [x, y]

# return a set of coordinates to place text in the upper right corner
def upr_right(text):
    global canvas_width, font_size, font_face
    
    text_width = frame.get_canvas_textwidth(text, font_size, font_face)
    x = (canvas_width - text_width)
    y = font_size
    
    return [x, y]

# -----------------------
# --- Define Handlers ---
# -----------------------

# increment the counter
def timer_handler():
    global tenths
    
    tenths += 1
    pass

# display the elapsed time in the center of the canvas
#  and the no. of success/attempts in the upper right
def draw_handler(canvas):
    global tenths, attempts, successes
    
    #draw timer
    timer_text = format_tenths_to_string(tenths)
    canvas.draw_text(timer_text, center(timer_text), font_size, 'Red', font_face)
    
    #draw successes/attempts
    game_text = str(successes) + "/" + str(attempts)
    canvas.draw_text(game_text, upr_right(game_text), font_size, 'Red', font_face)
    pass

# reset the counter and start the timer
def start():
    global timer
    
    timer.start()
    pass

# stop the timer, check if stopped on a whole second
def stop():
    global timer, running, attempts, successes
    
    if (timer.is_running()):
        if (whole_second()):
            successes += 1
        timer.stop()
        attempts += 1
    pass

# resets the timer, # attempts, and # successes to 0
def reset():
    global timer, tenths, attempts, successes
    
    timer.stop()
    tenths = 0
    attempts = 0
    successes = 0
    pass

# --------------------
# --- Create Frame ---
# --------------------

frame = simplegui.create_frame('Stopwatch', canvas_height, canvas_width)

# -------------------------
# --- Register Handlers ---
# -------------------------

timer = simplegui.create_timer(interval, timer_handler)
frame.set_draw_handler(draw_handler)
frame.add_button('START', start, 100)
frame.add_button('STOP', stop, 100)
frame.add_button('RESET', reset, 100)

# ----------------------------
# --- Start Frame & Timers ---
# ----------------------------

frame.start()
