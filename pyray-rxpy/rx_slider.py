from typing import TypeVar, Generic, List, Callable
import pyray as rl

# === Reactive Global Store with Explicit Type Safety ===
T = TypeVar('T')

class Observable(Generic[T]):
    """Observable container with explicit type safety and change notification"""

    def __init__(self, initial_value: T) -> None:
        self.value: T = initial_value
        self.watchers: List[Callable[[], None]] = []

def new_observable(initial_value: T) -> Observable[T]:
    """Creates a new Observable with explicit initial value and empty watchers"""
    return Observable(initial_value)

def set_value(observable: Observable[T], new_value: T) -> None:
    """Sets observable value with change detection and notification"""
    if observable.value != new_value:
        observable.value = new_value
        for watcher in observable.watchers:
            watcher()

def get_value(observable: Observable[T]) -> T:
    """Gets current observable value"""
    return observable.value

def add_watcher(observable: Observable[T], callback: Callable[[], None]) -> None:
    """Adds a watcher callback to observable"""
    observable.watchers.append(callback)

# === Global Store with Explicit Initialization ===
class ApplicationStore:
    """Application store with explicit observable fields"""

    def __init__(self) -> None:
        self.slider_a: Observable[float] = new_observable(0.5)
        self.slider_b: Observable[float] = new_observable(0.25)

def new_application_store() -> ApplicationStore:
    """Creates new application store with explicit default values"""
    return ApplicationStore()

# Global store instance with explicit initialization
global_store: ApplicationStore = new_application_store()

# === UI Constants with Explicit Types ===
SCREEN_WIDTH: int = 500
SCREEN_HEIGHT: int = 300
SLIDER_TRACK_WIDTH: float = 300.0
SLIDER_TRACK_HEIGHT: float = 20.0
SLIDER_START_X: float = 100.0
SLIDER_Y_SPACING: float = 70.0
LABEL_OFFSET_X: int = 50
LABEL_OFFSET_Y: int = 5
LABEL_FONT_SIZE: int = 20
VALUE_DISPLAY_Y: int = 200
VALUE_DISPLAY_SPACING: int = 30
SLIDER_KNOB_WIDTH: float = 10.0
SLIDER_KNOB_HEIGHT: float = 30.0
SLIDER_KNOB_OFFSET: float = 5.0

# === Utility Functions ===
def clamp_float(value: float, min_val: float, max_val: float) -> float:
    """Clamps float value between min and max bounds"""
    if value < min_val:
        return min_val
    elif value > max_val:
        return max_val
    else:
        return value

# === Slider Component with Explicit State Management ===
def render_slider(label_text: str, position_y: float, observable: Observable[float]) -> bool:
    """Renders interactive slider and returns true if value was modified"""
    label_x: int = LABEL_OFFSET_X
    label_y: int = int(position_y) - LABEL_OFFSET_Y - 30
    rl.draw_text(label_text, label_x, label_y, LABEL_FONT_SIZE, rl.DARKGRAY)

    # Define slider track bounds
    track_bounds = rl.Rectangle(
        SLIDER_START_X,
        position_y,
        SLIDER_TRACK_WIDTH,
        SLIDER_TRACK_HEIGHT
    )

    # Draw slider track
    rl.draw_rectangle_rounded(track_bounds, 0.2, 5, rl.LIGHTGRAY)

    # Calculate knob position based on current value
    current_value: float = get_value(observable)
    knob_center_x: float = track_bounds.x + (current_value * track_bounds.width)

    # Draw slider knob using individual rectangle parameters
    knob_x: float = knob_center_x - (SLIDER_KNOB_WIDTH / 2.0)
    knob_y: float = position_y - SLIDER_KNOB_OFFSET
    rl.draw_rectangle(
        int(knob_x),
        int(knob_y),
        int(SLIDER_KNOB_WIDTH),
        int(SLIDER_KNOB_HEIGHT),
        rl.MAROON
    )

    # Create knob bounds for collision detection
    knob_bounds = rl.Rectangle(
        knob_x,
        knob_y,
        SLIDER_KNOB_WIDTH,
        SLIDER_KNOB_HEIGHT
    )

    # Handle mouse interaction
    mouse_position: rl.Vector2 = rl.get_mouse_position()
    is_track_hovered: bool = rl.check_collision_point_rec(mouse_position, track_bounds)
    is_mouse_pressed: bool = rl.is_mouse_button_down(rl.MouseButton.MOUSE_BUTTON_LEFT)

    if is_track_hovered and is_mouse_pressed:
        relative_position: float = (mouse_position.x - track_bounds.x) / track_bounds.width
        clamped_value: float = clamp_float(relative_position, 0.0, 1.0)
        set_value(observable, clamped_value)
        return True

    return False

# === Value Display Functions ===
def render_value_display(label_text: str, value: float, position_y: int) -> None:
    """Renders formatted value display"""
    formatted_text: str = f"{label_text} = {value:.2f}"
    rl.draw_text(formatted_text, LABEL_OFFSET_X, position_y, LABEL_FONT_SIZE, rl.BLACK)

# === Main Application Loop ===
def main() -> None:
    """Main application entry point with explicit control flow"""
    # Initialize window with explicit dimensions
    rl.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Dependent Sliders with Global Store")
    rl.set_target_fps(60)

    # Establish dependency: Slider B follows Slider A at half value
    def slider_a_dependency() -> None:
        slider_a_value: float = get_value(global_store.slider_a)
        dependent_value: float = slider_a_value / 2.0
        set_value(global_store.slider_b, dependent_value)

    add_watcher(global_store.slider_a, slider_a_dependency)

    # Main rendering and interaction loop
    while not rl.window_should_close():
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        # Render interactive sliders
        slider_a_y: float = 80.0
        slider_b_y: float = slider_a_y + SLIDER_Y_SPACING

        render_slider("Slider A", slider_a_y, global_store.slider_a)
        render_slider("Slider B", slider_b_y, global_store.slider_b)

        # Display current values
        slider_a_value: float = get_value(global_store.slider_a)
        slider_b_value: float = get_value(global_store.slider_b)

        render_value_display("A", slider_a_value, VALUE_DISPLAY_Y)
        render_value_display("B", slider_b_value, VALUE_DISPLAY_Y + VALUE_DISPLAY_SPACING)

        rl.end_drawing()

    # Cleanup resources
    rl.close_window()

# Entry point with explicit module guard
if __name__ == "__main__":
    main()
