import pyray as pr
import rx
from rx import operators as ops
from rx.subject import Subject

# Simple player state
class Player:
    def __init__(self):
        self.x = 400  # Center of 800x600 window
        self.y = 300
        self.speed = 5
        self.width = 40
        self.height = 40

# Initialize Raylib
pr.init_window(800, 600, "RxPy: Map and Filter Example")
pr.set_target_fps(60)

# Input subject
input_subject = Subject()

# Poll keyboard inputs
def poll_inputs():
    if pr.is_key_down(pr.KEY_W):
        input_subject.on_next(('key', 'W'))
    elif pr.is_key_down(pr.KEY_S):
        input_subject.on_next(('key', 'S'))
    elif pr.is_key_down(pr.KEY_A):
        input_subject.on_next(('key', 'A'))
    elif pr.is_key_down(pr.KEY_D):
        input_subject.on_next(('key', 'D'))

# Player instance
player = Player()

# Reactive pipeline: Map keys to movement vectors and filter valid inputs
input_stream = input_subject.pipe(
    ops.filter(lambda event: event[0] == 'key' and event[1] in ['W', 'S', 'A', 'D']),
    ops.map(lambda event: {
        'W': (0, -player.speed),
        'S': (0, player.speed),
        'A': (-player.speed, 0),
        'D': (player.speed, 0)
    }[event[1]]),
    ops.throttle_first(0.016)  # ~60 FPS
)

# Update player position
def update_player(dx_dy):
    dx, dy = dx_dy
    player.x += dx
    player.y += dy
    player.x = max(0, min(player.x, 800 - player.width))
    player.y = max(0, min(player.y, 600 - player.height))

input_stream.subscribe(update_player)

# Main loop
while not pr.window_should_close():
    poll_inputs()
    pr.begin_drawing()
    pr.clear_background(pr.RAYWHITE)
    pr.draw_rectangle(int(player.x), int(player.y), player.width, player.height, pr.BLUE)
    pr.draw_text("Use WASD to move", 10, 10, 20, pr.BLACK)
    pr.end_drawing()

pr.close_window()
