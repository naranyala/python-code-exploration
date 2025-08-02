import pyray as pr
import rx
from rx import operators as ops
from rx.subject import Subject

class Player:
    def __init__(self):
        self.x = 400
        self.y = 300
        self.radius = 20

pr.init_window(800, 600, "RxPy: Debounce and Distinct Example")
pr.set_target_fps(60)

mouse_subject = Subject()

def poll_inputs():
    if pr.is_mouse_button_down(pr.MOUSE_BUTTON_LEFT):
        pos = pr.get_mouse_position()
        mouse_subject.on_next(('mouse', (pos.x, pos.y)))

player = Player()

mouse_stream = mouse_subject.pipe(
    ops.filter(lambda e: e[0] == 'mouse'),
    ops.debounce(0.05),  # Smooth out rapid mouse updates
    ops.distinct_until_changed(lambda e: e[1]),  # Only emit if position changes
    ops.map(lambda e: e[1])
)

mouse_stream.subscribe(lambda pos: (setattr(player, 'x', pos[0]), setattr(player, 'y', pos[1])))

while not pr.window_should_close():
    poll_inputs()
    pr.begin_drawing()
    pr.clear_background(pr.RAYWHITE)
    pr.draw_circle(int(player.x), int(player.y), player.radius, pr.PURPLE)
    pr.draw_text("Hold left mouse to move", 10, 10, 20, pr.BLACK)
    pr.end_drawing()

pr.close_window()
