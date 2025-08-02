import pyray as rl
from rx.subject import Subject
from rx import operators as ops
from typing import NamedTuple
import random

# Data structures
class Vec2(NamedTuple):
    x: float
    y: float

class GameState(NamedTuple):
    ball_pos: Vec2
    ball_vel: Vec2
    paddle1_y: float
    paddle2_y: float
    score1: int
    score2: int

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
PADDLE_SPEED = 8
BALL_SIZE = 15
BALL_SPEED = 6

# Initialize Raylib
rl.init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "RxPy Pong Fixed")
rl.set_target_fps(60)

# Hot subjects
input_stream = Subject()
game_state_stream = Subject()

# Initial game state
def reset_ball():
    return Vec2(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), Vec2(
        BALL_SPEED if random.random() > 0.5 else -BALL_SPEED,
        random.uniform(-BALL_SPEED/2, BALL_SPEED/2)
    )

ball_pos, ball_vel = reset_ball()
current_state = GameState(
    ball_pos=ball_pos,
    ball_vel=ball_vel,
    paddle1_y=WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2,
    paddle2_y=WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2,
    score1=0,
    score2=0
)

# Input mappings
player_inputs = {
    rl.KEY_W: ("p1", -PADDLE_SPEED),
    rl.KEY_S: ("p1", PADDLE_SPEED),
    rl.KEY_UP: ("p2", -PADDLE_SPEED),
    rl.KEY_DOWN: ("p2", PADDLE_SPEED)
}

def update_paddles_only(state: GameState, player_input) -> GameState:
    player, delta = player_input
    new_paddle1_y = state.paddle1_y
    new_paddle2_y = state.paddle2_y
    
    if player == "p1":
        new_paddle1_y = max(0, min(WINDOW_HEIGHT - PADDLE_HEIGHT, state.paddle1_y + delta))
    elif player == "p2":
        new_paddle2_y = max(0, min(WINDOW_HEIGHT - PADDLE_HEIGHT, state.paddle2_y + delta))
    
    # Keep ball physics unchanged
    return GameState(
        ball_pos=state.ball_pos,
        ball_vel=state.ball_vel,
        paddle1_y=new_paddle1_y,
        paddle2_y=new_paddle2_y,
        score1=state.score1,
        score2=state.score2
    )

def update_ball_physics(state: GameState) -> GameState:
    # Update ball position
    new_x = state.ball_pos.x + state.ball_vel.x
    new_y = state.ball_pos.y + state.ball_vel.y
    vel_x, vel_y = state.ball_vel.x, state.ball_vel.y
    
    # Top/bottom wall collision
    if new_y <= BALL_SIZE:
        vel_y = abs(vel_y)
        new_y = BALL_SIZE
    elif new_y >= WINDOW_HEIGHT - BALL_SIZE:
        vel_y = -abs(vel_y)
        new_y = WINDOW_HEIGHT - BALL_SIZE
    
    # Left paddle collision
    paddle1_left = 50
    paddle1_right = paddle1_left + PADDLE_WIDTH
    paddle1_top = state.paddle1_y
    paddle1_bottom = state.paddle1_y + PADDLE_HEIGHT
    
    if (new_x - BALL_SIZE <= paddle1_right and 
        new_x + BALL_SIZE >= paddle1_left and
        new_y + BALL_SIZE >= paddle1_top and 
        new_y - BALL_SIZE <= paddle1_bottom and
        vel_x < 0):
        vel_x = abs(vel_x)
        new_x = paddle1_right + BALL_SIZE
        vel_y += random.uniform(-1, 1)
    
    # Right paddle collision
    paddle2_left = WINDOW_WIDTH - 50 - PADDLE_WIDTH
    paddle2_right = paddle2_left + PADDLE_WIDTH
    paddle2_top = state.paddle2_y
    paddle2_bottom = state.paddle2_y + PADDLE_HEIGHT
    
    if (new_x + BALL_SIZE >= paddle2_left and 
        new_x - BALL_SIZE <= paddle2_right and
        new_y + BALL_SIZE >= paddle2_top and 
        new_y - BALL_SIZE <= paddle2_bottom and
        vel_x > 0):
        vel_x = -abs(vel_x)
        new_x = paddle2_left - BALL_SIZE
        vel_y += random.uniform(-1, 1)
    
    # Limit ball speed
    vel_y = max(-BALL_SPEED * 1.5, min(BALL_SPEED * 1.5, vel_y))
    
    # Check for scoring
    new_score1, new_score2 = state.score1, state.score2
    
    if new_x < -BALL_SIZE:
        new_score2 += 1
        ball_pos, ball_vel = reset_ball()
        new_x, new_y = ball_pos.x, ball_pos.y
        vel_x, vel_y = ball_vel.x, ball_vel.y
    elif new_x > WINDOW_WIDTH + BALL_SIZE:
        new_score1 += 1
        ball_pos, ball_vel = reset_ball()
        new_x, new_y = ball_pos.x, ball_pos.y
        vel_x, vel_y = ball_vel.x, ball_vel.y
    
    # Keep paddle positions unchanged
    return GameState(
        ball_pos=Vec2(new_x, new_y),
        ball_vel=Vec2(vel_x, vel_y),
        paddle1_y=state.paddle1_y,
        paddle2_y=state.paddle2_y,
        score1=new_score1,
        score2=new_score2
    )

# Single state stream that handles both input and physics
game_state_stream.pipe(
    ops.scan(lambda state, update_func: update_func(state), current_state)
).subscribe(
    on_next=lambda state: globals().update({'current_state': state})
)

# Game loop
while not rl.window_should_close():
    # Emit input updates
    for key in player_inputs.keys():
        if rl.is_key_down(key):
            player, delta = player_inputs[key]
            game_state_stream.on_next(lambda state: update_paddles_only(state, (player, delta)))
    
    # Always emit physics update
    game_state_stream.on_next(update_ball_physics)
    
    # Render
    rl.begin_drawing()
    rl.clear_background(rl.BLACK)
    
    # Draw paddles
    rl.draw_rectangle(50, int(current_state.paddle1_y), PADDLE_WIDTH, PADDLE_HEIGHT, rl.WHITE)
    rl.draw_rectangle(WINDOW_WIDTH - 50 - PADDLE_WIDTH, int(current_state.paddle2_y), PADDLE_WIDTH, PADDLE_HEIGHT, rl.WHITE)
    
    # Draw ball
    rl.draw_circle(int(current_state.ball_pos.x), int(current_state.ball_pos.y), BALL_SIZE, rl.WHITE)
    
    # Draw center line
    for i in range(0, WINDOW_HEIGHT, 20):
        rl.draw_rectangle(WINDOW_WIDTH // 2 - 2, i, 4, 10, rl.GRAY)
    
    # Draw scores
    rl.draw_text(str(current_state.score1), WINDOW_WIDTH // 4, 50, 60, rl.WHITE)
    rl.draw_text(str(current_state.score2), 3 * WINDOW_WIDTH // 4, 50, 60, rl.WHITE)
    
    # Draw controls
    rl.draw_text("Player 1: W/S", 10, WINDOW_HEIGHT - 40, 20, rl.GRAY)
    rl.draw_text("Player 2: UP/DOWN", WINDOW_WIDTH - 200, WINDOW_HEIGHT - 40, 20, rl.GRAY)
    
    rl.end_drawing()

rl.close_window()
