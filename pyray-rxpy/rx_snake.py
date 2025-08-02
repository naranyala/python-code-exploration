#!/usr/bin/env python3
"""
Snake Game - Python Raylib Version
Classic snake game with imperative style
"""

import raylib as rl
from raylib import colors
import random
from typing import List, Tuple
from enum import Enum


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class GameState(Enum):
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2


class SnakeGame:
    """Snake game with imperative state management"""

    def __init__(self):
        # Game configuration
        self.grid_width = 25
        self.grid_height = 20
        self.cell_size = 25
        self.screen_width = self.grid_width * self.cell_size
        self.screen_height = self.grid_height * self.cell_size + 50

        # Game state
        self.game_state = GameState.MENU
        self.snake_body = []
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.food_pos = (0, 0)
        self.score = 0
        self.game_over_reason = ""

        # Game timing
        self.move_timer = 0.0
        self.move_interval = 0.15

        self.init_game()

    def init_game(self):
        """Initialize game state"""
        self.snake_body = [(self.grid_width // 2, self.grid_height // 2)]
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.food_pos = self.generate_food_position()
        self.score = 0
        self.game_over_reason = ""
        self.move_interval = 0.15

    def generate_food_position(self) -> Tuple[int, int]:
        """Generate random food position not occupied by snake"""
        while True:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            if (x, y) not in self.snake_body:
                return (x, y)

    def handle_input(self):
        """Handle keyboard input"""
        if self.game_state == GameState.MENU:
            if rl.IsKeyPressed(rl.KEY_SPACE):
                self.init_game()
                self.game_state = GameState.PLAYING

        elif self.game_state == GameState.PLAYING:
            if rl.IsKeyPressed(rl.KEY_UP) and self.direction != Direction.DOWN:
                self.next_direction = Direction.UP
            elif rl.IsKeyPressed(rl.KEY_DOWN) and self.direction != Direction.UP:
                self.next_direction = Direction.DOWN
            elif rl.IsKeyPressed(rl.KEY_LEFT) and self.direction != Direction.RIGHT:
                self.next_direction = Direction.LEFT
            elif rl.IsKeyPressed(rl.KEY_RIGHT) and self.direction != Direction.LEFT:
                self.next_direction = Direction.RIGHT

        elif self.game_state == GameState.GAME_OVER:
            if rl.IsKeyPressed(rl.KEY_SPACE):
                self.game_state = GameState.MENU

    def update(self, delta_time: float):
        """Update game logic"""
        if self.game_state != GameState.PLAYING:
            return

        self.move_timer += delta_time

        if self.move_timer >= self.move_interval:
            self.move_timer = 0.0
            self.move_snake()

    def move_snake(self):
        """Move snake and handle game logic"""
        # Update direction
        self.direction = self.next_direction

        # Calculate new head position
        head_x, head_y = self.snake_body[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)

        # Check wall collision
        if (new_head[0] < 0 or new_head[0] >= self.grid_width or
            new_head[1] < 0 or new_head[1] >= self.grid_height):
            self.game_over_reason = "Hit wall!"
            self.game_state = GameState.GAME_OVER
            return

        # Check self collision
        if new_head in self.snake_body:
            self.game_over_reason = "Hit yourself!"
            self.game_state = GameState.GAME_OVER
            return

        # Add new head
        self.snake_body.insert(0, new_head)

        # Check food collision
        if new_head == self.food_pos:
            # Snake grows (don't remove tail)
            self.score += 10
            self.food_pos = self.generate_food_position()

            # Increase speed slightly
            self.move_interval = max(0.08, self.move_interval - 0.005)
        else:
            # Normal movement (remove tail)
            self.snake_body.pop()

    def render(self):
        """Render current game state"""
        rl.BeginDrawing()
        rl.ClearBackground(colors.BLACK)

        if self.game_state == GameState.MENU:
            self.render_menu()
        elif self.game_state == GameState.PLAYING:
            self.render_game()
        elif self.game_state == GameState.GAME_OVER:
            self.render_game_over()

        rl.EndDrawing()

    def render_menu(self):
        """Render main menu"""
        title = "SNAKE GAME"
        title_bytes = title.encode('utf-8')
        title_width = rl.MeasureText(title_bytes, 40)
        rl.DrawText(title_bytes,
                   (self.screen_width - title_width) // 2,
                   self.screen_height // 2 - 60,
                   40,
                   colors.GREEN)

        instruction = "Press SPACE to start"
        instruction_bytes = instruction.encode('utf-8')
        instruction_width = rl.MeasureText(instruction_bytes, 20)
        rl.DrawText(instruction_bytes,
                   (self.screen_width - instruction_width) // 2,
                   self.screen_height // 2 + 20,
                   20,
                   colors.WHITE)

        controls = "Use arrow keys to control"
        controls_bytes = controls.encode('utf-8')
        controls_width = rl.MeasureText(controls_bytes, 16)
        rl.DrawText(controls_bytes,
                   (self.screen_width - controls_width) // 2,
                   self.screen_height // 2 + 50,
                   16,
                   colors.GRAY)

    def render_game(self):
        """Render active game"""
        # Draw grid lines
        for x in range(0, self.screen_width, self.cell_size):
            rl.DrawLine(x, 0, x, self.grid_height * self.cell_size, colors.DARKGRAY)
        for y in range(0, self.grid_height * self.cell_size, self.cell_size):
            rl.DrawLine(0, y, self.screen_width, y, colors.DARKGRAY)

        # Draw snake
        for i, (x, y) in enumerate(self.snake_body):
            pixel_x = x * self.cell_size
            pixel_y = y * self.cell_size

            # Head is brighter than body
            snake_color = colors.LIME if i == 0 else colors.GREEN
            rl.DrawRectangle(pixel_x + 1, pixel_y + 1,
                           self.cell_size - 2, self.cell_size - 2,
                           snake_color)

        # Draw food
        food_x, food_y = self.food_pos
        food_pixel_x = food_x * self.cell_size
        food_pixel_y = food_y * self.cell_size
        rl.DrawRectangle(food_pixel_x + 2, food_pixel_y + 2,
                        self.cell_size - 4, self.cell_size - 4,
                        colors.RED)

        # Draw score
        score_text = f"Score: {self.score}"
        score_bytes = score_text.encode('utf-8')
        rl.DrawText(score_bytes, 10, self.grid_height * self.cell_size + 10, 20, colors.WHITE)

        # Draw length
        length_text = f"Length: {len(self.snake_body)}"
        length_bytes = length_text.encode('utf-8')
        rl.DrawText(length_bytes, 200, self.grid_height * self.cell_size + 10, 20, colors.WHITE)

    def render_game_over(self):
        """Render game over screen with overlay"""
        # Draw game state first (dimmed background)
        self.render_game()

        # Draw semi-transparent overlay
        rl.DrawRectangle(0, 0, self.screen_width, self.screen_height, colors.BLACK)

        # Game over title
        game_over = "GAME OVER"
        game_over_bytes = game_over.encode('utf-8')
        game_over_width = rl.MeasureText(game_over_bytes, 32)
        rl.DrawText(game_over_bytes,
                   (self.screen_width - game_over_width) // 2,
                   self.screen_height // 2 - 80,
                   32,
                   colors.RED)

        # Game over reason
        reason_bytes = self.game_over_reason.encode('utf-8')
        reason_width = rl.MeasureText(reason_bytes, 20)
        rl.DrawText(reason_bytes,
                   (self.screen_width - reason_width) // 2,
                   self.screen_height // 2 - 40,
                   20,
                   colors.WHITE)

        # Final score
        final_score = f"Final Score: {self.score}"
        final_score_bytes = final_score.encode('utf-8')
        final_score_width = rl.MeasureText(final_score_bytes, 20)
        rl.DrawText(final_score_bytes,
                   (self.screen_width - final_score_width) // 2,
                   self.screen_height // 2,
                   20,
                   colors.YELLOW)

        # Final length
        final_length = f"Final Length: {len(self.snake_body)}"
        final_length_bytes = final_length.encode('utf-8')
        final_length_width = rl.MeasureText(final_length_bytes, 20)
        rl.DrawText(final_length_bytes,
                   (self.screen_width - final_length_width) // 2,
                   self.screen_height // 2 + 25,
                   20,
                   colors.YELLOW)

        # Return to menu instruction
        restart = "Press SPACE to return to menu"
        restart_bytes = restart.encode('utf-8')
        restart_width = rl.MeasureText(restart_bytes, 16)
        rl.DrawText(restart_bytes,
                   (self.screen_width - restart_width) // 2,
                   self.screen_height // 2 + 60,
                   16,
                   colors.GRAY)


def main():
    # Initialize game
    game = SnakeGame()

    # Initialize raylib window
    rl.InitWindow(game.screen_width, game.screen_height, b"Snake Game")
    rl.SetTargetFPS(60)

    # Main game loop
    while not rl.WindowShouldClose():
        delta_time = rl.GetFrameTime()

        # Process input
        game.handle_input()

        # Update game state
        game.update(delta_time)

        # Render frame
        game.render()

    # Cleanup
    rl.CloseWindow()


if __name__ == "__main__":
    main()
