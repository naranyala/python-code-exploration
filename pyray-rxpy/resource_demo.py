import pyray as rl
from rx.subject import Subject
from rx import operators as ops
from rx import create, interval
import random

rl.init_window(800, 600, "Resource Management")
rl.set_target_fps(60)

# Reactive particle system
particles = []
particle_stream = Subject()
disposer = Subject()

# Create particle stream with automatic cleanup
create(lambda observer, scheduler:
    interval(0.1).pipe(
        ops.take_until(disposer),
        ops.map(lambda _: {
            "x": 400,
            "y": 300,
            "vx": random.uniform(-2, 2),
            "vy": random.uniform(-2, 2),
            "life": 100
        })
    ).subscribe(observer)
).subscribe(
    on_next=lambda p: particles.append(p),
    on_error=lambda e: print(f"Particle error: {e}")
)

# Update particles reactively
particle_stream.pipe(
    ops.map(lambda p: {
        **p,
        "x": p["x"] + p["vx"],
        "y": p["y"] + p["vy"],
        "life": p["life"] - 1
    }),
    ops.filter(lambda p: p["life"] > 0)
).subscribe(
    on_next=lambda p: particles.append(p),
    on_error=lambda e: print(f"Update error: {e}")
)

# Game loop
while not rl.window_should_close():
    # Clear particles and update
    particles.clear()
    particle_stream.on_next(None)  # Trigger update
    
    # Cleanup on key press
    if rl.is_key_pressed(rl.KEY_SPACE):
        disposer.on_next(None)  # Dispose stream
        particles.clear()
    
    # Drawing
    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)
    for p in particles:
        rl.draw_circle(int(p["x"]), int(p["y"]), 5, rl.MAROON)
    rl.end_drawing()

rl.close_window()
