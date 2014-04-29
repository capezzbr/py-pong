# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# ball
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]

# paddle
PADDLE_VELOCITY = 4
paddle1_pos = HEIGHT / 2
paddle1_vel = 0
paddle2_pos = HEIGHT / 2
paddle2_vel = 0

# score
score1 = 0
score2 = 0

def is_ball_touching_paddle(paddle_pos):
    return ball_pos[1] >= paddle_pos - HALF_PAD_HEIGHT and ball_pos[1] <= paddle_pos + HALF_PAD_HEIGHT

def paddle_collision():
    # flip the ball
    ball_vel[0] = -ball_vel[0]
   
    # increment the ball velocity by 10%
    ball_vel[0] += ball_vel[0] * 0.1
    ball_vel[1] += ball_vel[1] * 0.1

def check_collision():
    global score1, score2
    
    # checking collision with horizontal line
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]

    # checking collision with left gutter / padder
    elif ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if is_ball_touching_paddle(paddle1_pos):
            paddle_collision()
        else:
            score2 += 1
            spawn_ball(RIGHT)

    # checking collision with left gutter / padder            
    elif ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH:
        if is_ball_touching_paddle(paddle2_pos):
            paddle_collision()
        else:
            score1 += 1
            spawn_ball(LEFT)

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    ball_vel = [random.randrange(120, 240) / 60, -(random.randrange(60, 180) / 60)]
    if direction == LEFT:
        ball_vel[0] = -ball_vel[0]
        
    ball_pos = [WIDTH / 2, HEIGHT / 2]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    score1 = score2 = 0
    
    if random.randrange(0, 2) == 0:
        spawn_ball(LEFT)
    else:
        spawn_ball(RIGHT)

def paddle_set_pos(new_position):
    # we limit the paddle position inside the screen
    new_position = min(new_position, HEIGHT - HALF_PAD_HEIGHT)
    new_position = max(new_position, HALF_PAD_HEIGHT)
    return new_position
        
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos = paddle_set_pos(paddle1_pos + paddle1_vel)
    paddle2_pos = paddle_set_pos(paddle2_pos + paddle2_vel)    
    
    # draw paddles
    canvas.draw_line([HALF_PAD_WIDTH, paddle1_pos-HALF_PAD_HEIGHT], 
                     [HALF_PAD_WIDTH, paddle1_pos+HALF_PAD_HEIGHT], PAD_WIDTH, "Blue")
    
    canvas.draw_line([WIDTH - HALF_PAD_WIDTH, paddle2_pos-HALF_PAD_HEIGHT], 
                     [WIDTH - HALF_PAD_WIDTH, paddle2_pos+HALF_PAD_HEIGHT], PAD_WIDTH, "Blue")
    
    # check collision
    check_collision()
    
    # draw scores
    canvas.draw_text(str(score1), [WIDTH*0.25, 100], 60, 'White', 'monospace')
    canvas.draw_text(str(score2), [WIDTH*0.75, 100], 60, 'White', 'monospace')
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = PADDLE_VELOCITY
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = -PADDLE_VELOCITY
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = PADDLE_VELOCITY
    elif key == simplegui.KEY_MAP['w']:
        paddle1_vel = -PADDLE_VELOCITY
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP['down'] or key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['s'] or key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0
        
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game, 200)

# start frame
new_game()
frame.start()
