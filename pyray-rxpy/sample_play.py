import pyray as rl
from rx.subject import Subject
from rx import operators as ops
from typing import NamedTuple

# Data structures
class Vec2(NamedTuple):
    x: int
    y: int

# Initialize Raylib
rl.init_window(800, 600, "Hot Observable RxPy Game")
rl.set_target_fps(60)

# Hot subjects - always emitting
input_stream = Subject()
position_stream = Subject()

# Game state
current_position = Vec2(400, 300)

# Movement deltas
movements = {
    rl.KEY_D: Vec2(15, 0),
    rl.KEY_A: Vec2(-15, 0),
    rl.KEY_W: Vec2(0, -15),
    rl.KEY_S: Vec2(0, 15)
}

# Process input stream and update position
input_stream.pipe(
    ops.filter(lambda key: key in movements),
    ops.map(lambda key: movements[key]),
    ops.scan(lambda pos, delta: Vec2(
        max(0, min(750, pos.x + delta.x)),
        max(0, min(550, pos.y + delta.y))
    ), current_position)
).subscribe(
    on_next=lambda pos: position_stream.on_next(pos)
)

# Subscribe to position updates
position_stream.subscribe(
    on_next=lambda pos: globals().update({'current_position': pos})
)

# Game loop
while not rl.window_should_close():
    # Emit input events to hot stream
    for key in movements.keys():
        if rl.is_key_pressed(key):
            input_stream.on_next(key)
    
    # Render
    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)
    rl.draw_rectangle(current_position.x, current_position.y, 50, 50, rl.MAROON)
    rl.end_drawing()

rl.close_window()
