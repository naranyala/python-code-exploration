import pyray as pr
import rx
from rx import operators as ops
from rx.subject import Subject

class Player:
    def __init__(self):
        self.x = 400
        self.y = 300
        self.speed = 5
        self.radius = 20

pr.init_window(800, 600, "RxPy: Merge Example")
pr.set_target_fps(60)

# Subjects for keyboard and mouse
key_subject = Subject()
mouse_subject = Subject()

# Poll inputs
def poll_inputs():
    if pr.is_key_down(pr.KEY_W):
        key_subject.on_next(('key', (0, -5)))
    elif pr.is_key_down(pr.KEY_S):
        key_subject.on_next(('key', (0, 5)))
    elif pr.is_key_down(pr.KEY_A):
        key_subject.on_next(('key', (-5, 0)))
    elif pr.is_key_down(pr.KEY_D):
        key_subject.on_next(('key', (5, 0)))
    if pr.is_mouse_button_pressed(pr.MOUSE_BUTTON_LEFT):
        mouse_pos = pr.get_mouse_position()
        mouse_subject.on_next(('mouse', (mouse_pos.x, mouse_pos.y)))

player = Player()

# Merge keyboard and mouse streams
combined_stream = rx.merge(
    key_subject.pipe(
        ops.filter(lambda e: e[0] == 'key'),
        ops.throttle_first(0.016)
    ),
    mouse_subject.pipe(
        ops.filter(lambda e: e[0] == 'mouse'),
        ops.throttle_first(0.1)  # Slower for mouse clicks
    )
)

# Update player based on event type
def update_player(event):
    if event[0] == 'key':
        dx, dy = event[1]
        player.x += dx
        player.y += dy
    elif event[0] == 'mouse':
        player.x, player.y = event[1]
    player.x = max(0, min(player.x, 800))
    player.y = max(0, min(player.y, 600))

combined_stream.subscribe(update_player)

# Main loop
while not pr.window_should_close():
    poll_inputs()
    pr.begin_drawing()
    pr.clear_background(pr.RAYWHITE)
    pr.draw_circle(int(player.x), int(player.y), player.radius, pr.GREEN)
    pr.draw_text("WASD to move, click to teleport", 10, 10, 20, pr.BLACK)
    pr.end_drawing()

pr.close_window()
