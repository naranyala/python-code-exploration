import pyray as pr
import rx
from rx import operators as ops
from rx.subject import Subject
import time

# Game state struct-like class (simple, explicit)
class Player:
    def __init__(self):
        self.x = 400  # Center of 800x600 window
        self.y = 300
        self.speed = 5

# Initialize Raylib window
pr.init_window(800, 600, "Reactive PyRay Example")
pr.set_target_fps(60)

# Create a subject to emit input events
input_subject = Subject()

# Function to poll Raylib inputs and emit to subject
def poll_inputs():
    key_event = None
    if pr.is_key_down(pr.KEY_W):
        key_event = ('move', (0, -1))  # Up
    elif pr.is_key_down(pr.KEY_S):
        key_event = ('move', (0, 1))   # Down
    elif pr.is_key_down(pr.KEY_A):
        key_event = ('move', (-1, 0))  # Left
    elif pr.is_key_down(pr.KEY_D):
        key_event = ('move', (1, 0))   # Right
    if key_event:
        input_subject.on_next(key_event)

# Create player state
player = Player()

# Define reactive pipeline for player movement
def update_player_position(event):
    action, (dx, dy) = event
    if action == 'move':
        player.x += dx * player.speed
        player.y += dy * player.speed
        # Ensure player stays within window bounds
        player.x = max(0, min(player.x, 800))
        player.y = max(0, min(player.y, 600))

# Create observable for input events and process them
input_stream = input_subject.pipe(
    ops.throttle_first(0.016),  # Limit to ~60 FPS (16ms)
    ops.map(lambda event: event)  # Pass-through for clarity
)

# Subscribe to input stream to update player
input_stream.subscribe(update_player_position)

# Main game loop
while not pr.window_should_close():
    # Poll inputs and emit to subject
    poll_inputs()

    # Render
    pr.begin_drawing()
    pr.clear_background(pr.RAYWHITE)
    pr.draw_circle(int(player.x), int(player.y), 20, pr.RED)
    pr.draw_text("Use WASD to move", 10, 10, 20, pr.BLACK)
    pr.end_drawing()

# Cleanup
pr.close_window()
