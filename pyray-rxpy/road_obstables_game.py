#!/usr/bin/env python3
"""
Car Escape Game - Python Port
A simple car escape game where the player avoids falling obstacles.
"""

import pyray as rl
import random
import math
from dataclasses import dataclass
from typing import List

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 80
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 50
MAX_OBSTACLES = 10
PLAYER_SPEED = 5
INITIAL_OBSTACLE_SPEED = 3

@dataclass
class Player:
    x: float
    y: float
    color: rl.Color

@dataclass
class Obstacle:
    x: float
    y: float
    active: bool
    color: rl.Color
    speed: float

# Initialize window
rl.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Car Escape Game")
rl.set_target_fps(60)

# Initialize player
player = Player(
    x=SCREEN_WIDTH / 2 - PLAYER_WIDTH / 2,
    y=SCREEN_HEIGHT - PLAYER_HEIGHT - 20,
    color=rl.SKYBLUE
)

# Initialize obstacles
obstacles: List[Obstacle] = []
for i in range(MAX_OBSTACLES):
    obstacles.append(Obstacle(
        x=0,
        y=-OBSTACLE_HEIGHT,
        active=False,
        color=rl.RED,
        speed=INITIAL_OBSTACLE_SPEED
    ))

score = 0
game_over = False
obstacle_speed = float(INITIAL_OBSTACLE_SPEED)

# Game loop
while not rl.window_should_close():
    # Update
    if not game_over:
        # Player movement (all 4 directions)
        if rl.is_key_down(rl.KeyboardKey.KEY_LEFT) and player.x > 0:
            player.x -= PLAYER_SPEED
        if rl.is_key_down(rl.KeyboardKey.KEY_RIGHT) and player.x < SCREEN_WIDTH - PLAYER_WIDTH:
            player.x += PLAYER_SPEED
        if rl.is_key_down(rl.KeyboardKey.KEY_UP) and player.y > 0:
            player.y -= PLAYER_SPEED
        if rl.is_key_down(rl.KeyboardKey.KEY_DOWN) and player.y < SCREEN_HEIGHT - PLAYER_HEIGHT:
            player.y += PLAYER_SPEED
        
        # Spawn obstacles
        for i in range(MAX_OBSTACLES):
            if not obstacles[i].active:
                if random.randint(0, 99) < 2:  # 2% chance to spawn each frame
                    obstacles[i].active = True
                    obstacles[i].x = random.randint(0, SCREEN_WIDTH - OBSTACLE_WIDTH)
                    obstacles[i].y = -OBSTACLE_HEIGHT
                    obstacles[i].speed = obstacle_speed
                    break
        
        # Update obstacles
        for i in range(MAX_OBSTACLES):
            if obstacles[i].active:
                obstacles[i].y += obstacles[i].speed
                
                # Check collision
                if rl.check_collision_recs(
                    (player.x, player.y, PLAYER_WIDTH, PLAYER_HEIGHT),
                    (obstacles[i].x, obstacles[i].y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
                ):
                    game_over = True
                
                # Check if obstacle passed bottom
                if obstacles[i].y > SCREEN_HEIGHT:
                    obstacles[i].active = False
                    score += 1
                    # Increase difficulty
                    if score % 5 == 0:
                        obstacle_speed += 0.5
    else:
        if rl.is_key_pressed(rl.KeyboardKey.KEY_SPACE):
            # Reset game
            game_over = False
            score = 0
            obstacle_speed = INITIAL_OBSTACLE_SPEED
            for i in range(MAX_OBSTACLES):
                obstacles[i].active = False
    
    # Draw
    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)
    
    # Draw road
    rl.draw_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, rl.DARKGRAY)
    
    # Draw road markings
    for i in range(0, SCREEN_HEIGHT, 40):
        rl.draw_rectangle(
            SCREEN_WIDTH // 2 - 5,
            i,
            10,
            20,
            rl.YELLOW
        )
    
    # Draw player
    rl.draw_rectangle_rounded(
        (player.x, player.y, PLAYER_WIDTH, PLAYER_HEIGHT),
        0.2, 5, player.color
    )
    
    # Draw obstacles
    for i in range(MAX_OBSTACLES):
        if obstacles[i].active:
            rl.draw_rectangle_rounded(
                (obstacles[i].x, obstacles[i].y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT),
                0.2, 5, obstacles[i].color
            )
    
    # Draw score and controls
    score_text = f"Score: {score}"
    rl.draw_text(score_text, 10, 10, 20, rl.WHITE)
    rl.draw_text("Use arrow keys to move", 10, 35, 16, rl.LIGHTGRAY)
    
    if game_over:
        game_over_text = "GAME OVER"
        restart_text = "Press SPACE to restart"
        
        game_over_width = rl.measure_text(game_over_text, 40)
        restart_width = rl.measure_text(restart_text, 20)
        
        rl.draw_text(
            game_over_text,
            SCREEN_WIDTH // 2 - game_over_width // 2,
            SCREEN_HEIGHT // 2 - 50,
            40,
            rl.RED
        )
        rl.draw_text(
            restart_text,
            SCREEN_WIDTH // 2 - restart_width // 2,
            SCREEN_HEIGHT // 2 + 20,
            20,
            rl.WHITE
        )
    
    rl.end_drawing()

# Cleanup
rl.close_window()
