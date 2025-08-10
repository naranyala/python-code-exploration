
import pyray as rl
from rx import interval
from rx import operators as ops

rl.init_window(640, 480, b"Reactive Ticker")
rl.set_target_fps(60)

tick_stream = interval(0.016).pipe(  # ~60 FPS
    ops.scan(lambda acc, _: acc + 1, 0),         # frame counter
    ops.map(lambda count: count * 0.016),        # elapsed seconds
)

elapsed_time = 0.0
tick_stream.subscribe(lambda t: globals().__setitem__('elapsed_time', t))

while not rl.window_should_close():
    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)
    rl.draw_text(f"Elapsed: {elapsed_time:.2f}s", 10, 10, 20, rl.BLACK)
    rl.end_drawing()

rl.close_window()
