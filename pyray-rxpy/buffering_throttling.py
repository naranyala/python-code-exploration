import pyray as rl
from rx.subject import Subject
from rx import operators as ops
from rx import interval
import time

rl.init_window(800, 600, "Buffering and Throttling")
rl.set_target_fps(60)

# Mouse position tracking
mouse_stream = Subject()

# Buffer mouse positions every second
mouse_stream.pipe(
    ops.buffer(interval(1.0)),
    ops.map(lambda positions: {
        "count": len(positions),
        "avg_x": sum(p.x for p in positions) / len(positions) if positions else 0,
        "avg_y": sum(p.y for p in positions) / len(positions) if positions else 0
    })
).subscribe(
    on_next=lambda stats: print(f"Mouse stats: {stats}"),
    on_error=lambda e: print(f"Buffer error: {e}")
)

# Throttled keyboard input
keyboard_stream = Subject()

keyboard_stream.pipe(
    ops.throttle_first(0.5),  # Minimum 500ms between events
    ops.scan(lambda acc, key: acc + [key], [])
).subscribe(
    on_next=lambda history: print(f"Key history: {history}"),
    on_error=lambda e: print(f"Throttle error: {e}")
)

# Game loop
while not rl.window_should_close():
    # Emit mouse position
    mouse_stream.on_next(rl.get_mouse_position())
    
    # Emit keyboard events
    if rl.is_key_pressed(rl.KEY_SPACE):
        keyboard_stream.on_next(rl.KEY_SPACE)
    
    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)
    rl.draw_text("Move mouse and press SPACE", 190, 200, 20, rl.MAROON)
    rl.draw_text("Check console for stats", 190, 230, 20, rl.MAROON)
    rl.end_drawing()

rl.close_window()
