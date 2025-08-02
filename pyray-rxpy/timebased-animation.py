import pyray as rl
from rx import interval, operators as ops
import math

rl.init_window(800, 600, "Reactive Animation")
rl.set_target_fps(60)

# Reactive animation using time-based emissions
animation_state = {"angle": 0}

interval(0.016).pipe(  # ~60 FPS
    ops.scan(lambda acc, _: acc + 0.05, 0),  # Increment angle
    ops.map(lambda angle: angle % (2 * math.pi))  # Keep angle in [0, 2π]
).subscribe(
    on_next=lambda angle: animation_state.update(angle=angle),
    on_error=lambda e: print(f"Animation error: {e}")
)

while not rl.window_should_close():
    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)
    
    # Draw rotating rectangle using reactive angle
    x = 400 + math.cos(animation_state["angle"]) * 100
    y = 300 + math.sin(animation_state["angle"]) * 100
    rl.draw_rectangle(int(x), int(y), 50, 50, rl.MAROON)
    
    rl.end_drawing()

rl.close_window()
