import pyray as pr
import rx
from rx import operators as ops
from rx.subject import Subject
import math

class Entity:
    def __init__(self, x, y, speed, radius):
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = radius

pr.init_window(800, 600, "RxPy: Combine Latest Example")
pr.set_target_fps(60)

player = Entity(400, 300, 5, 20)
enemy = Entity(100, 100, 3, 15)

key_subject = Subject()

def poll_inputs():
    if pr.is_key_down(pr.KEY_W):
        key_subject.on_next(('key', (0, -player.speed)))
    elif pr.is_key_down(pr.KEY_S):
        key_subject.on_next(('key', (0, player.speed)))
    elif pr.is_key_down(pr.KEY_A):
        key_subject.on_next(('key', (-player.speed, 0)))
    elif pr.is_key_down(pr.KEY_D):
        key_subject.on_next(('key', (player.speed, 0)))

# Player movement stream
player_stream = key_subject.pipe(
    ops.filter(lambda e: e[0] == 'key'),
    ops.throttle_first(0.016),
    ops.scan(lambda acc, dx_dy: (
        max(0, min(acc[0] + dx_dy[1][0], 800)),
        max(0, min(acc[1] + dx_dy[1][1], 600))
    ), (player.x, player.y))  # Accumulate position
)

# Enemy follows player
def enemy_follow(p_pos):
    dx = p_pos[0] - enemy.x
    dy = p_pos[1] - enemy.y
    dist = math.sqrt(dx**2 + dy**2)
    if dist > 0:
        enemy.x += (dx / dist) * enemy.speed
        enemy.y += (dy / dist) * enemy.speed

# Combine player and enemy positions
interaction_stream = player_stream.pipe(
    ops.combine_latest(rx.of((enemy.x, enemy.y))),
    ops.throttle_first(0.016)
)

# Update game state
def update_game(positions):
    player.x, player.y = positions[0]
    enemy_follow(positions[0])

interaction_stream.subscribe(update_game)

# Main loop
while not pr.window_should_close():
    poll_inputs()
    pr.begin_drawing()
    pr.clear_background(pr.RAYWHITE)
    pr.draw_circle(int(player.x), int(player.y), player.radius, pr.BLUE)
    pr.draw_circle(int(enemy.x), int(enemy.y), enemy.radius, pr.RED)
    pr.draw_text("WASD to move, enemy follows", 10, 10, 20, pr.BLACK)
    pr.end_drawing()

pr.close_window()
