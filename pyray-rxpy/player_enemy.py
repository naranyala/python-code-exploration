import pyray as pr
import rx
from rx import operators as ops
from rx.subject import Subject
import random
import math

# Simple data structures
class Player:
    def __init__(self):  # Fixed: double underscores
        self.x = 400
        self.y = 300
        self.speed = 5
        self.radius = 20

class Enemy:
    def __init__(self, x, y):  # Fixed: double underscores
        self.x = x
        self.y = y
        self.speed = 2
        self.radius = 15

# Initialize Raylib
pr.init_window(800, 600, b"RxPy: Reactive Game Demo")  # Added 'b' prefix
pr.set_target_fps(60)

# Game state
player = Player()
enemies = []
game_over = False

# Subjects
key_subject = Subject()
game_over_subject = Subject()

# Poll keyboard inputs
def poll_inputs():
    global game_over
    if not game_over:
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
    ops.map(lambda e: e[1]),  # Extract movement delta
    ops.scan(lambda acc, delta: (
        max(player.radius, min(acc[0] + delta[0], 800 - player.radius)),
        max(player.radius, min(acc[1] + delta[1], 600 - player.radius))
    ), (player.x, player.y)),
    ops.take_until(game_over_subject)
)

# Update player position
def update_player_pos(pos):
    player.x, player.y = pos

player_stream.subscribe(update_player_pos)

# Enemy spawn stream (every 2 seconds)
spawn_stream = rx.interval(2.0).pipe(
    ops.map(lambda _: Enemy(
        random.randint(50, 750), 
        random.randint(50, 550)
    )),
    ops.take_until(game_over_subject)
)

# Add enemy to list
def add_enemy(enemy):
    enemies.append(enemy)

spawn_stream.subscribe(add_enemy)

# Collision detection function
def check_collision():
    global game_over
    if game_over:
        return
    
    for enemy in enemies:
        distance = math.sqrt((player.x - enemy.x)**2 + (player.y - enemy.y)**2)
        if distance < (player.radius + enemy.radius):
            game_over = True
            game_over_subject.on_next(None)
            break

# Enemy movement function
def update_enemies():
    if game_over:
        return
    
    for enemy in enemies:
        dx = player.x - enemy.x
        dy = player.y - enemy.y
        dist = math.sqrt(dx**2 + dy**2)
        if dist > 0:
            enemy.x += (dx / dist) * enemy.speed
            enemy.y += (dy / dist) * enemy.speed

# Main loop
while not pr.window_should_close():
    poll_inputs()
    update_enemies()
    check_collision()
    
    pr.begin_drawing()
    pr.clear_background(pr.RAYWHITE)
    
    # Render player
    pr.draw_circle(int(player.x), int(player.y), player.radius, pr.BLUE)
    
    # Render enemies
    for enemy in enemies:
        pr.draw_circle(int(enemy.x), int(enemy.y), enemy.radius, pr.RED)
    
    # Render text
    if game_over:
        pr.draw_text(b"Game Over!", 300, 280, 40, pr.BLACK)
    else:
        pr.draw_text(b"WASD to move, avoid enemies!", 10, 10, 20, pr.BLACK)
    
    pr.end_drawing()

pr.close_window()
