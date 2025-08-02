# smooth_sprinkles.py
import pyray as rl
import math
import random
from dataclasses import dataclass
from typing import List, Tuple
from collections import deque

@dataclass
class Vec2:
    x: float = 0.0
    y: float = 0.0
    
    def __add__(self, other: 'Vec2') -> 'Vec2':
        return Vec2(self.x + other.x, self.y + other.y)
    
    def __mul__(self, scalar: float) -> 'Vec2':
        return Vec2(self.x * scalar, self.y * scalar)
    
    def distance_to(self, other: 'Vec2') -> float:
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)

@dataclass
class Sprinkle:
    position: Vec2
    target: Vec2
    velocity: Vec2
    rotation: float
    rotation_speed: float
    life_time: float
    color: Tuple[int, int, int, int]
    size: float
    trail_alpha: float = 1.0
    
    def update(self, dt: float, mouse_pos: Vec2) -> None:
        # Update target to follow mouse with some lag
        self.target = mouse_pos
        
        # Smooth movement towards target
        to_target = Vec2(self.target.x - self.position.x, self.target.y - self.position.y)
        distance = self.position.distance_to(self.target)
        
        if distance > 1.0:
            # Smooth interpolation - closer sprinkles move faster
            lerp_factor = min(1.0, dt * (5.0 + distance * 0.01))
            self.position.x += to_target.x * lerp_factor
            self.position.y += to_target.y * lerp_factor
        
        # Add some floating motion
        self.position.x += math.sin(self.life_time * 2.0) * 0.5
        self.position.y += math.cos(self.life_time * 1.5) * 0.3
        
        # Update rotation
        self.rotation += self.rotation_speed * dt
        self.life_time += dt
        
        # Update trail effect
        self.trail_alpha = max(0.1, math.sin(self.life_time * 3.0) * 0.3 + 0.7)

class SprinkleSystem:
    SPRINKLE_COLORS = [
        (255, 100, 150),  # Pink
        (100, 200, 255),  # Blue  
        (150, 255, 100),  # Green
        (255, 255, 100),  # Yellow
        (200, 100, 255),  # Purple
        (255, 150, 100),  # Orange
        (100, 255, 200),  # Cyan
        (255, 200, 200),  # Light red
    ]
    
    def __init__(self, max_sprinkles: int = 60):
        self.sprinkles: List[Sprinkle] = []
        self.max_sprinkles = max_sprinkles
        self.spawn_timer = 0.0
        self.spawn_interval = 0.03  # Spawn every 30ms
        self.mouse_trail = deque(maxlen=10)  # Track recent mouse positions
        
    def add_mouse_position(self, pos: Vec2) -> None:
        self.mouse_trail.append(pos)
    
    def update(self, dt: float, mouse_pos: Vec2, mouse_in_window: bool) -> None:
        self.add_mouse_position(mouse_pos)
        
        # Spawn new sprinkles when mouse is in window
        if mouse_in_window and len(self.sprinkles) < self.max_sprinkles:
            self.spawn_timer += dt
            if self.spawn_timer >= self.spawn_interval:
                self.spawn_sprinkle(mouse_pos)
                self.spawn_timer = 0.0
        
        # Update existing sprinkles
        for sprinkle in self.sprinkles:
            sprinkle.update(dt, mouse_pos)
        
        # Remove sprinkles that are too far from mouse (cleanup)
        if mouse_in_window:
            self.sprinkles = [
                s for s in self.sprinkles 
                if s.position.distance_to(mouse_pos) < 400 or len(self.sprinkles) <= 20
            ]
        else:
            # Gradually remove sprinkles when mouse leaves
            if self.sprinkles and random.random() < dt * 2.0:
                self.sprinkles.pop()
    
    def spawn_sprinkle(self, mouse_pos: Vec2) -> None:
        # Spawn slightly behind the mouse for trailing effect
        spawn_offset = 20.0
        angle = random.uniform(0, 2 * math.pi)
        spawn_pos = Vec2(
            mouse_pos.x + math.cos(angle) * spawn_offset * random.uniform(0.5, 1.5),
            mouse_pos.y + math.sin(angle) * spawn_offset * random.uniform(0.5, 1.5)
        )
        
        sprinkle = Sprinkle(
            position=spawn_pos,
            target=mouse_pos,
            velocity=Vec2(0, 0),
            rotation=random.uniform(0, 2 * math.pi),
            rotation_speed=random.uniform(-8, 8),
            life_time=0.0,
            color=random.choice(self.SPRINKLE_COLORS),
            size=random.uniform(3.0, 8.0)
        )
        
        self.sprinkles.append(sprinkle)
    
    def get_sprinkles(self) -> List[Sprinkle]:
        return self.sprinkles

class SprinkleApp:
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    
    def __init__(self):
        rl.init_window(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, "Smooth Cursor Sprinkles")
        rl.set_target_fps(60)
        
        self.sprinkle_system = SprinkleSystem()
        self.last_mouse_pos = Vec2()
        
    def run(self) -> None:
        try:
            while not rl.window_should_close():
                self.update()
                self.render()
        finally:
            rl.close_window()
    
    def update(self) -> None:
        dt = rl.get_frame_time()
        
        # Get mouse state
        mouse_pos = rl.get_mouse_position()
        mouse_vec = Vec2(mouse_pos.x, mouse_pos.y)
        
        mouse_in_window = (
            0 <= mouse_pos.x < self.WINDOW_WIDTH and 
            0 <= mouse_pos.y < self.WINDOW_HEIGHT
        )
        
        # Update sprinkle system
        self.sprinkle_system.update(dt, mouse_vec, mouse_in_window)
        self.last_mouse_pos = mouse_vec
    
    def render(self) -> None:
        rl.begin_drawing()
        
        # Dark background for better sprinkle visibility
        rl.clear_background(rl.Color(20, 20, 30, 255))
        
        # Draw mouse trail
        trail_positions = list(self.sprinkle_system.mouse_trail)
        for i, pos in enumerate(trail_positions[:-1]):
            if i + 1 < len(trail_positions):
                next_pos = trail_positions[i + 1]
                alpha = int(50 * (i + 1) / len(trail_positions))
                rl.draw_line_ex(
                    rl.Vector2(pos.x, pos.y),
                    rl.Vector2(next_pos.x, next_pos.y),
                    2.0,
                    rl.Color(255, 255, 255, alpha)
                )
        
        # Draw sprinkles with glow effect
        for sprinkle in self.sprinkle_system.get_sprinkles():
            r, g, b = sprinkle.color
            alpha = int(255 * sprinkle.trail_alpha)
            color = rl.Color(r, g, b, alpha)
            
            # Draw glow (larger, more transparent)
            glow_size = sprinkle.size * 2.0
            glow_alpha = alpha // 4
            glow_color = rl.Color(r, g, b, glow_alpha)
            
            rl.draw_circle(
                int(sprinkle.position.x), 
                int(sprinkle.position.y), 
                glow_size, 
                glow_color
            )
            
            # Draw main sprinkle as rotated rectangle
            rect = rl.Rectangle(
                sprinkle.position.x - sprinkle.size * 0.3,
                sprinkle.position.y - sprinkle.size * 0.6,
                sprinkle.size * 0.6,
                sprinkle.size * 1.2
            )
            origin = rl.Vector2(sprinkle.size * 0.3, sprinkle.size * 0.6)
            rotation_degrees = math.degrees(sprinkle.rotation)
            
            rl.draw_rectangle_pro(rect, origin, rotation_degrees, color)
        
        # Draw UI
        rl.draw_text("Move mouse around to create sprinkles!", 10, 10, 20, rl.WHITE)
        sprinkle_count = len(self.sprinkle_system.get_sprinkles())
        rl.draw_text(f"Sprinkles: {sprinkle_count}", 10, 40, 16, rl.LIGHTGRAY)
        
        # Draw cursor indicator
        mouse_pos = rl.get_mouse_position()
        if (0 <= mouse_pos.x < self.WINDOW_WIDTH and 0 <= mouse_pos.y < self.WINDOW_HEIGHT):
            rl.draw_circle_lines(int(mouse_pos.x), int(mouse_pos.y), 15, rl.WHITE)
        
        rl.end_drawing()

def main():
    app = SprinkleApp()
    app.run()

if __name__ == "__main__":
    main()
