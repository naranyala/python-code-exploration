
import pyray as rl

from rx import operators as ops
from rx import interval
from rx import zip as rx_zip

from rx.subject import Subject

click_subject = Subject()

# Emit mouse click
def check_mouse_click():
    if rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON):
        click_subject.on_next("click")

# Simulate time interval
timer = interval(1.0).pipe(ops.map(lambda i: f"time:{i}"))

# Combine user click and time tick
zipped = rx_zip(click_subject, timer)

zipped.subscribe(lambda pair: print(f"CLICKED @ {pair[1]}"))

rl.init_window(640, 480, b"Click + Time Combo")

while not rl.window_should_close():
    check_mouse_click()
    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)
    rl.draw_text("Click to combine with timer", 20, 20, 20, rl.DARKGRAY)
    rl.end_drawing()

rl.close_window()
