import pyray as rl
from rx import operators as ops
from rx.subject import Subject

input_subject = Subject()

def input_emit():
    if rl.is_key_down(rl.KEY_W): 
        input_subject.on_next((0, -1))
    if rl.is_key_down(rl.KEY_S): 
        input_subject.on_next((0, 1))
    if rl.is_key_down(rl.KEY_A): 
        input_subject.on_next((-1, 0))
    if rl.is_key_down(rl.KEY_D): 
        input_subject.on_next((1, 0))

pos_stream = input_subject.pipe(
    ops.map(lambda delta: (delta[0] * 0.2, delta[1] * 0.2)),  # Changed from 4 to 1
    ops.scan(lambda acc, d: (acc[0] + d[0], acc[1] + d[1]), (100, 100))
)

current_pos = (100, 100)

def update_position(pos):
    global current_pos
    current_pos = pos

pos_stream.subscribe(update_position)

rl.init_window(640, 480, b"Merged Movement")

while not rl.window_should_close():
    input_emit()
    
    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)
    rl.draw_circle(int(current_pos[0]), int(current_pos[1]), 20, rl.MAROON)
    rl.end_drawing()

rl.close_window()
