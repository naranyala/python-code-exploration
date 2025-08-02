
import pyray as rl
from rx.subject import Subject
from rx import interval
from rx import operators as ops
import random

rl.init_window(800, 600, b"Reactive Particles")
rl.set_target_fps(60)

particle_subject = Subject()
frame_tick = Subject()
particles = []

# Particle structure
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-4, -1)
        self.life = 60  # 1 second at 60 FPS

# Emit particles on click
def spawn_particles():
    if rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON):
        pos = rl.get_mouse_position()
        for _ in range(10):
            particle_subject.on_next(Particle(pos.x, pos.y))

# Push tick each frame
def tick():
    frame_tick.on_next(1)

# Handle new particles
particle_subject.subscribe(lambda p: particles.append(p))

# Animate particles
frame_tick.subscribe(lambda _: [
    setattr(p, 'x', p.x + p.vx) or
    setattr(p, 'y', p.y + p.vy) or
    setattr(p, 'vy', p.vy + 0.1) or  # gravity
    setattr(p, 'life', p.life - 1)
    for p in particles
])

while not rl.window_should_close():
    spawn_particles()
    tick()

    particles[:] = [p for p in particles if p.life > 0]

    rl.begin_drawing()
    rl.clear_background(rl.BLACK)

    for p in particles:
        alpha = int(255 * p.life / 60)
        rl.draw_circle(int(p.x), int(p.y), 4, rl.fade(rl.YELLOW, alpha / 255))

    rl.draw_text("Click to spawn particles", 10, 10, 20, rl.LIGHTGRAY)
    rl.end_drawing()

rl.close_window()
