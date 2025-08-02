import pyray as rl
from rx.subject import Subject
from rx import operators as ops
from rx import merge

rl.init_window(800, 600, "Complex Event Handling")
rl.set_target_fps(60)

# Reactive state
player = {"x": 400, "y": 300, "color": rl.BLUE, "speed": 5}

# Event streams
keyboard_events = Subject()
mouse_events = Subject()

# Combine keyboard and mouse events
merge(
    keyboard_events.pipe(
        ops.filter(lambda key: key in [rl.KEY_W, rl.KEY_S, rl.KEY_A, rl.KEY_D]),
        ops.map(lambda key: {
            rl.KEY_W: (0, -1),
            rl.KEY_S: (0, 1),
            rl.KEY_A: (-1, 0),
            rl.KEY_D: (1, 0)
        }[key])
    ),
    mouse_events.pipe(
        ops.filter(lambda btn: btn == rl.MOUSE_LEFT_BUTTON),
        ops.with_latest_from(keyboard_events.pipe(
            ops.start_with(None),
            ops.map(lambda _: player["color"])
        )),
        ops.map(lambda pair: ("color_change", rl.RED if pair[1] == rl.BLUE else rl.BLUE))
    )
).subscribe(
    on_next=lambda event: (
        player.update(x=player["x"] + event[0] * player["speed"]) 
        if isinstance(event, tuple) and len(event) == 2 
        else player.update(color=event[1])
    ),
    on_error=lambda e: print(f"Event error: {e}")
)

# Game loop
while not rl.window_should_close():
    # Emit keyboard events
    if rl.is_key_down(rl.KEY_W): keyboard_events.on_next(rl.KEY_W)
    if rl.is_key_down(rl.KEY_S): keyboard_events.on_next(rl.KEY_S)
    if rl.is_key_down(rl.KEY_A): keyboard_events.on_next(rl.KEY_A)
    if rl.is_key_down(rl.KEY_D): keyboard_events.on_next(rl.KEY_D)
    
    # Emit mouse events
    if rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON):
        mouse_events.on_next(rl.MOUSE_LEFT_BUTTON)
    
    # Drawing
    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)
    rl.draw_rectangle(player["x"], player["y"], 50, 50, player["color"])
    rl.end_drawing()

rl.close_window()
