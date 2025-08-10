import pyray as rl
from rx.subject import Subject
from rx import operators as ops
from rx.scheduler import ThreadPoolScheduler
import time

rl.init_window(640, 480, b"Reactive Button")
rl.set_target_fps(60)

# --- Reactive streams
mouse_pos_subject = Subject()
mouse_click_subject = Subject()

# --- Button bounds
button_rect = rl.Rectangle(200, 200, 240, 60)

# --- Hover stream
hover_stream = mouse_pos_subject.pipe(
    ops.map(lambda pos: rl.check_collision_point_rec(pos, button_rect)),
    ops.distinct_until_changed()
)

# --- Click stream only if hovering
click_stream = mouse_click_subject.pipe(
    ops.with_latest_from(hover_stream),
    ops.filter(lambda pair: pair[1]),
    ops.map(lambda _: "clicked"),
    ops.throttle_first(0.5),  # prevent spam
)

hovering = False
button_clicked = False

hover_stream.subscribe(lambda state: globals().__setitem__('hovering', state))
click_stream.subscribe(lambda _: globals().__setitem__('button_clicked', True))

# --- Main loop
while not rl.window_should_close():
    mouse_pos = rl.get_mouse_position()
    mouse_pos_subject.on_next(mouse_pos)

    if rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON):
        mouse_click_subject.on_next("click")

    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)

    color = rl.DARKGRAY if hovering else rl.GRAY
    rl.draw_rectangle_rec(button_rect, color)
    rl.draw_text("Click Me", 250, 220, 20, rl.WHITE)

    if button_clicked:
        rl.draw_text("Button Clicked!", 220, 300, 20, rl.RED)
        button_clicked = False  # reset for next frame

    rl.end_drawing()

rl.close_window()

