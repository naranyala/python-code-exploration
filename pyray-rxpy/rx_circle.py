from typing import TypeVar, Generic, List, Callable, Sequence
from dataclasses import dataclass
import pyray as rl

# === Reactive System with Explicit Type Safety ===
T = TypeVar('T')

class Observable(Generic[T]):
    """Observable container with explicit type safety and change notification"""

    def __init__(self, initial_value: T) -> None:
        self._value: T = initial_value
        self._watchers: List[Callable[[], None]] = []

    def set_value(self, new_value: T) -> None:
        """Sets observable value with change detection and notification"""
        if self._value != new_value:
            self._value = new_value
            for watcher in self._watchers:
                watcher()

    def get_value(self) -> T:
        """Gets current observable value"""
        return self._value

    def add_watcher(self, callback: Callable[[], None]) -> None:
        """Adds a watcher callback to observable"""
        self._watchers.append(callback)

# === UI Constants with Explicit Types ===
SCREEN_WIDTH: int = 500
SCREEN_HEIGHT: int = 400
SIDEBAR_WIDTH: float = 100.0
SIDEBAR_PADDING: float = 10.0
BUTTON_FONT_SIZE: int = 16
BUTTON_WIDTH: float = 80.0
BUTTON_HEIGHT: float = 30.0
BUTTON_TEXT_OFFSET_X: int = 15
BUTTON_TEXT_OFFSET_Y: int = 7
SLIDER_WIDTH: float = 20.0
SLIDER_HEIGHT: float = 100.0
SLIDER_TRACK_WIDTH: float = 10.0
SLIDER_HANDLE_SIZE: float = 20.0
CIRCLE_CENTER_X: float = (SCREEN_WIDTH - SIDEBAR_WIDTH) / 2.0 + SIDEBAR_WIDTH
CIRCLE_CENTER_Y: float = SCREEN_HEIGHT / 2.0
MIN_RADIUS: float = 10.0
MAX_RADIUS: float = 150.0

# Predefined colors using raylib Color constants
PREDEFINED_COLORS: Sequence[rl.Color] = [
    rl.RED,
    rl.BLUE,
    rl.GREEN
]

def render_button(bounds: rl.Rectangle, label: str) -> bool:
    """Renders button and returns true if clicked"""
    rl.draw_rectangle_rounded(bounds, 0.3, 5, rl.DARKGRAY)

    text_x: int = int(bounds.x) + BUTTON_TEXT_OFFSET_X
    text_y: int = int(bounds.y) + BUTTON_TEXT_OFFSET_Y
    rl.draw_text(label, text_x, text_y, BUTTON_FONT_SIZE, rl.WHITE)

    mouse_position: rl.Vector2 = rl.get_mouse_position()
    is_hovered: bool = rl.check_collision_point_rec(mouse_position, bounds)
    is_clicked: bool = rl.is_mouse_button_released(rl.MouseButton.MOUSE_BUTTON_LEFT)

    return is_hovered and is_clicked

def render_slider(bounds: rl.Rectangle, value: float, min_value: float, max_value: float) -> float:
    """Renders a vertical slider and returns the updated value"""
    track_x: float = bounds.x + (bounds.width - SLIDER_TRACK_WIDTH) / 2.0
    track_bounds = rl.Rectangle(
        track_x,
        bounds.y,
        SLIDER_TRACK_WIDTH,
        bounds.height
    )

    # Draw track
    rl.draw_rectangle(int(track_bounds.x), int(track_bounds.y),
                     int(track_bounds.width), int(track_bounds.height), rl.GRAY)

    # Calculate handle position (inverted for vertical slider: smaller y = larger value)
    normalized_value: float = (value - min_value) / (max_value - min_value)
    handle_y: float = bounds.y + bounds.height - (normalized_value * bounds.height)
    handle_bounds = rl.Rectangle(
        bounds.x,
        handle_y - SLIDER_HANDLE_SIZE / 2.0,
        bounds.width,
        SLIDER_HANDLE_SIZE
    )

    # Draw handle
    rl.draw_rectangle_rounded(handle_bounds, 0.3, 5, rl.DARKBLUE)

    # Handle mouse interaction
    mouse_position: rl.Vector2 = rl.get_mouse_position()
    new_value: float = value
    if (rl.is_mouse_button_down(rl.MouseButton.MOUSE_BUTTON_LEFT) and
        rl.check_collision_point_rec(mouse_position, bounds)):
        relative_y: float = mouse_position.y - bounds.y
        normalized: float = 1.0 - max(0.0, min(1.0, relative_y / bounds.height))  # Invert for vertical
        new_value = min_value + normalized * (max_value - min_value)

    return max(min_value, min(max_value, new_value))

def main() -> None:
    """Main application loop with explicit control flow"""
    # Initialize window with explicit dimensions
    rl.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Resizable Colored Circle")
    rl.set_target_fps(60)

    # Create observables for radius and color
    radius: Observable[float] = Observable(50.0)
    color: Observable[rl.Color] = Observable(rl.BLUE)

    # Add watchers for debugging
    radius.add_watcher(lambda: print(f"Radius changed to {radius.get_value()}"))
    color.add_watcher(lambda: print(f"Color changed to {color.get_value()}"))

    # Main rendering loop
    while not rl.window_should_close():
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        # Draw sidebar background
        rl.draw_rectangle(0, 0, int(SIDEBAR_WIDTH), SCREEN_HEIGHT, rl.LIGHTGRAY)

        # Draw circle with current radius and color
        current_radius: float = radius.get_value()
        current_color: rl.Color = color.get_value()
        rl.draw_circle(int(CIRCLE_CENTER_X), int(CIRCLE_CENTER_Y),
                      current_radius, current_color)

        # Draw radius value below circle
        radius_text: str = f"Radius: {current_radius:.1f}"
        text_width: int = rl.measure_text(radius_text, BUTTON_FONT_SIZE)
        text_x: int = int(CIRCLE_CENTER_X) - (text_width // 2)
        rl.draw_text(radius_text, text_x, int(CIRCLE_CENTER_Y + current_radius + 20.0),
                    BUTTON_FONT_SIZE, rl.BLACK)

        # Draw slider for radius
        slider_bounds = rl.Rectangle(
            SIDEBAR_PADDING,
            SIDEBAR_PADDING,
            SLIDER_WIDTH,
            SLIDER_HEIGHT
        )
        new_radius: float = render_slider(slider_bounds, radius.get_value(), MIN_RADIUS, MAX_RADIUS)
        radius.set_value(new_radius)

        # Draw color selection buttons
        color_names: List[str] = ["Red", "Blue", "Green"]
        for i in range(len(PREDEFINED_COLORS)):
            button_bounds = rl.Rectangle(
                SIDEBAR_PADDING,
                SIDEBAR_PADDING + SLIDER_HEIGHT + SIDEBAR_PADDING + i * (BUTTON_HEIGHT + SIDEBAR_PADDING),
                BUTTON_WIDTH,
                BUTTON_HEIGHT
            )
            if render_button(button_bounds, color_names[i]):
                color.set_value(PREDEFINED_COLORS[i])

        rl.end_drawing()

    # Cleanup resources
    rl.close_window()

# Entry point with explicit module guard
if __name__ == "__main__":
    main()
