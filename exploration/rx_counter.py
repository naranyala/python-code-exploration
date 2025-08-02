from typing import List, Callable
import pyray as rl

# === Reactive System with Explicit Type Safety ===
class Observable:
    """Observable container for integer values with explicit type safety"""

    def __init__(self, initial_value: int) -> None:
        self.value: int = initial_value
        self.watchers: List[Callable[[], None]] = []

def new_observable(initial_value: int) -> Observable:
    """Creates a new Observable with explicit initial value"""
    return Observable(initial_value)

def set_value(observable: Observable, new_value: int) -> None:
    """Sets observable value with change detection and notification"""
    if observable.value != new_value:
        observable.value = new_value
        for watcher in observable.watchers:
            watcher()

def get_value(observable: Observable) -> int:
    """Gets current observable value"""
    return observable.value

def add_watcher(observable: Observable, callback: Callable[[], None]) -> None:
    """Adds a watcher callback to observable"""
    observable.watchers.append(callback)

# === UI Constants with Explicit Types ===
SCREEN_WIDTH: int = 400
SCREEN_HEIGHT: int = 200
FONT_SIZE: int = 32
BUTTON_FONT_SIZE: int = 20
BUTTON_WIDTH: float = 80.0
BUTTON_HEIGHT: float = 40.0
PADDING: float = 20.0
BUTTON_TEXT_OFFSET_X: int = 20
BUTTON_TEXT_OFFSET_Y: int = 8
COUNTER_DISPLAY_Y: int = 40
BUTTON_ROW_Y: float = 100.0

# === UI Button with Explicit State Management ===
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

# === Text Measurement with Explicit Type Handling ===
def measure_text_width(text: str, font_size: int) -> int:
    """Measures text width with explicit type conversion"""
    return rl.measure_text(text, font_size)

# === Main Application Loop ===
def main() -> None:
    """Main application entry point with explicit control flow"""
    # Initialize window with explicit dimensions
    rl.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Observable Counter")
    rl.set_target_fps(60)

    # Create observable counter with explicit initial state
    counter: Observable = new_observable(0)

    # Add watcher with explicit closure
    add_watcher(counter, lambda: print(f"Counter changed to {get_value(counter)}"))

    # Main rendering loop
    while not rl.window_should_close():
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        # Calculate center position explicitly
        center_x: int = SCREEN_WIDTH // 2
        current_value: int = get_value(counter)
        value_string: str = str(current_value)
        text_width: int = measure_text_width(value_string, FONT_SIZE)
        text_x: int = center_x - (text_width // 2)

        # Draw counter value with explicit string type
        rl.draw_text(value_string, text_x, COUNTER_DISPLAY_Y, FONT_SIZE, rl.BLACK)

        # Define button bounds with explicit positioning
        decrement_button_bounds = rl.Rectangle(
            float(center_x) - BUTTON_WIDTH - PADDING,
            BUTTON_ROW_Y,
            BUTTON_WIDTH,
            BUTTON_HEIGHT
        )

        increment_button_bounds = rl.Rectangle(
            float(center_x) + PADDING,
            BUTTON_ROW_Y,
            BUTTON_WIDTH,
            BUTTON_HEIGHT
        )

        # Handle button interactions with explicit state changes
        if render_button(decrement_button_bounds, "-"):
            set_value(counter, current_value - 1)

        if render_button(increment_button_bounds, "+"):
            set_value(counter, current_value + 1)

        rl.end_drawing()

    # Cleanup resources
    rl.close_window()

# Entry point with explicit module guard
if __name__ == "__main__":
    main()
