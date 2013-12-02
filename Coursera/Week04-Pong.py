# Week 04 Project - Pong
# Paste into www.codeskulptor.org to see it run

# ------------------------
# --- Import Libraries ---
# ------------------------
import random
import simplegui

# ---------------------------
# --- Define Global State ---
# ---------------------------

# Field
FIELD_COLOR = 'gray'
GUTTER = 10

# Canvas
WIDTH = 600
HEIGHT = 400
FONT_SIZE = 64
FONT_FACE = 'monospace'

# General Constants
LEFT = -1
RIGHT = 1
UP = -1
DOWN = 1
X = 0
Y = 1

# Ball
BALL_RADIUS = 20
BALL_COLOR = 'white'
ball_position = [WIDTH // 2, HEIGHT // 2]
ball_direction = [RIGHT, UP] # up, to the right
ball_velocity = [150, 60] # pixels per second
ball_cum_err = [0, 0]

# Paddle
PADDLE_WIDTH = 8
PADDLE_LENGTH = 40
PADDLE_COLOR = 'white'
left_paddle = [GUTTER - PADDLE_WIDTH // 2, HEIGHT // 2]
left_paddle_dir = [0, 0]
left_paddle_step = [0, 0]
right_paddle = [WIDTH - (GUTTER -PADDLE_WIDTH // 2), HEIGHT // 2]
right_paddle_dir = [0, 0]
right_paddle_step = [0, 0]
PADDLE_VELOCITY = 240 # pixels per second

# Scores
left_score = 0
right_score = 0

# Bounds
LEFT_BOUNDS = GUTTER + BALL_RADIUS
RIGHT_BOUNDS = WIDTH - GUTTER - BALL_RADIUS - 1

# ------------------------
# --- Helper Functions ---
# ------------------------

# give new coordinates for the ball
def spawn_ball(direction):
    global ball_position, ball_direction, ball_velocity, ball_cum_err
    
    ball_position = [WIDTH // 2, HEIGHT // 2]
    ball_direction = [direction, UP]
    ball_velocity[X] = random.randrange(120, 240, 1)
    ball_velocity[Y] = random.randrange(60, 180, 1)
    ball_cum_err = [0, 0]
    pass

# start a new round
def new_round(direction):
    global left_paddle, right_paddle
    
    spawn_ball(direction)
    left_paddle = [GUTTER - PADDLE_WIDTH // 2, HEIGHT // 2]
    right_paddle = [WIDTH - (GUTTER -PADDLE_WIDTH // 2), HEIGHT // 2]
    
    pass

# return the step size facoring in subpixel error
#  track the cumulative error
def step_with_error(velocity, cum_err):
    err = round(velocity / 6) % 10
    step = velocity // 60
    cum_err += err
    if (cum_err > 10):
        cum_err = cum_err % 10
        step += 1
    
    return step

# move the paddle, do not let it cross the upper or lower
#  walls of the canvas
def move_paddle(position, direction):  
    step = direction[Y] * (PADDLE_VELOCITY // 60)
    position[Y] += step
    if (position[Y] <= PADDLE_LENGTH):
        position[Y] = PADDLE_LENGTH
    elif (position[Y] >= HEIGHT - PADDLE_LENGTH - 1):
        position[Y] = HEIGHT - PADDLE_LENGTH - 1


# move the ball, bounce of paddles and upper/lower walls
#  increment score if ball hits a gutter and restart the game
def move_ball(position, direction, velocity, cum_err):
    global left_paddle, right_paddle
    global left_score, right_score
    
    # Move Y first
    step_y = direction[Y] * step_with_error(velocity[Y], cum_err[Y])
    position[Y] += step_y
    
    # Check for reflections
    if (position[Y] <= BALL_RADIUS):
        direction[Y] = -direction[Y]
        position[Y] = 2 * BALL_RADIUS - position[Y]
    elif (position[Y] >= HEIGHT - BALL_RADIUS - 1):
        direction[Y] = -direction[Y]
        position[Y] = 2 * (HEIGHT - BALL_RADIUS -1) - position[Y] 
    
    # Move X
    step_x = direction[X] * step_with_error(velocity[X], cum_err[X])
    position[X] += step_x
    
    # Find nearest paddle
    if (position[X] < WIDTH // 2):
        nearest_paddle = left_paddle
    else:
        nearest_paddle = right_paddle
    
    # Check if ball will land on paddle
    if (position[Y] >= nearest_paddle[Y] - PADDLE_LENGTH and \
        position[Y] <= nearest_paddle[Y] + PADDLE_LENGTH - 1):
        
        # Reflect off paddle
        if (position[X] <= LEFT_BOUNDS):
            direction[X] = -direction[X]
            position[X] = 2 * LEFT_BOUNDS - position[X]
            velocity[X] = int(round(velocity[X] * 1.1))
            velocity[Y] = int(round(velocity[Y] * 1.1))
        elif (position[X] >= RIGHT_BOUNDS):
            direction[X] = -direction[X]
            position[X] = 2 * RIGHT_BOUNDS - position[X]
            velocity[X] = int(round(velocity[X] * 1.1))
            velocity[Y] = int(round(velocity[Y] * 1.1))
    else:
        
        # Stop on gutter
        if (position[X] <= LEFT_BOUNDS):
            direction[X] = 0
            direction[Y] = 0
            position[X] = LEFT_BOUNDS
            right_score += 1
            spawn_ball(RIGHT)
        elif (position[X] >= RIGHT_BOUNDS):
            direction[X] = 0
            direction[Y] = 0
            position[X] = RIGHT_BOUNDS
            left_score += 1
            spawn_ball(LEFT)
    pass

# return the X,Y coordinates for the left-side score
def position_left_score():
    global left_score
    
    txt_width = frame.get_canvas_textwidth(str(left_score), FONT_SIZE, FONT_FACE)
    x = (WIDTH * 3) // 8 - txt_width
    y = HEIGHT // 4
    return [x, y]

# return the X,Y coordinates for the right-side score
def position_right_score():
    global right_score
    
    x = (WIDTH * 5) // 8
    y = HEIGHT // 4
    return [x, y]

# -----------------------
# --- Define Handlers ---
# -----------------------

# display the field, two paddles, and the ball for Pong
#  update the position of the ball and paddles
def draw_handler(canvas):
    global left_score, right_score
    global left_paddle, left_paddle_dir
    global right_paddle, right_paddle_dir
    global ball_position, ball_direction, ball_velocity, ball_cum_err
 
    # field
    canvas.draw_line([WIDTH // 2, 0], [WIDTH // 2, HEIGHT - 1], 1, FIELD_COLOR)
    canvas.draw_line([GUTTER, 0], [GUTTER, HEIGHT - 1], 1, FIELD_COLOR)
    canvas.draw_line([WIDTH - GUTTER, 0], [WIDTH - GUTTER, HEIGHT - 1], 1, FIELD_COLOR)
    
    # scores
    canvas.draw_text(str(left_score), position_left_score(), FONT_SIZE, 'green', FONT_FACE)
    canvas.draw_text(str(right_score), position_right_score(), FONT_SIZE, 'green', FONT_FACE)

    
    # paddles
    move_paddle(left_paddle, left_paddle_dir)
    move_paddle(right_paddle, right_paddle_dir)    
    canvas.draw_line([left_paddle[X], left_paddle[Y] - PADDLE_LENGTH], \
                     [left_paddle[X], left_paddle[Y] + PADDLE_LENGTH], \
                     PADDLE_WIDTH, PADDLE_COLOR)
    canvas.draw_line([right_paddle[X], right_paddle[Y] - PADDLE_LENGTH], \
                     [right_paddle[X], right_paddle[Y] + PADDLE_LENGTH], \
                     PADDLE_WIDTH, PADDLE_COLOR)
    
    # ball
    move_ball(ball_position, ball_direction, ball_velocity, ball_cum_err)
    canvas.draw_circle(ball_position, BALL_RADIUS, 1, BALL_COLOR, BALL_COLOR)
    pass

# Move paddles in the direction given by the keys
def keydown_handler(key):
    global left_paddle_dir, right_paddle_dir
    if (key == simplegui.KEY_MAP['w']):
        left_paddle_dir[Y] += UP
    elif (key == simplegui.KEY_MAP['s']):
        left_paddle_dir[Y] += DOWN
    elif (key == simplegui.KEY_MAP['up']):
        right_paddle_dir[Y] += UP
    elif (key == simplegui.KEY_MAP['down']):
        right_paddle_dir[Y] += DOWN
    pass

# Stop moving paddles in the direction given by the keys
def keyup_handler(key):
    global left_paddle_dir, right_paddle_dir
    if (key == simplegui.KEY_MAP['w']):
        left_paddle_dir[Y] -= UP
    elif (key == simplegui.KEY_MAP['s']):
        left_paddle_dir[Y] -= DOWN
    elif (key == simplegui.KEY_MAP['up']):
        right_paddle_dir[Y] -= UP
    elif (key == simplegui.KEY_MAP['down']):
        right_paddle_dir[Y] -= DOWN
    pass

# resets the timer, # attempts, and # successes to 0
def reset(): 
    global left_score, right_score
    
    left_score = 0
    right_score = 0
    new_round(RIGHT)
    pass

# --------------------
# --- Create Frame ---
# --------------------

frame = simplegui.create_frame('Pong', WIDTH, HEIGHT)

# -------------------------
# --- Register Handlers ---
# -------------------------

frame.set_draw_handler(draw_handler)
frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)
frame.add_button('RESET', reset, 100)

# ----------------------------
# --- Start Frame & Timers ---
# ----------------------------

frame.start()
new_round(RIGHT)
