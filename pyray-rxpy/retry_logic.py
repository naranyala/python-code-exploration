import pyray as rl
from rx.subject import Subject
from rx import operators as ops
from rx import of, throw
import random

rl.init_window(800, 600, "Error Handling")
rl.set_target_fps(60)

# Simulated unreliable service
unreliable_service = Subject()

# Process with error handling and retry
unreliable_service.pipe(
    ops.map(lambda req: {
        "data": req,
        "timestamp": rl.get_time()
    }),
    ops.merge_map(lambda item: 
        of(item) if random.random() > 0.3 else throw(Exception("Service failed"))
    ),
    ops.retry(2),  # Retry up to 2 times
    ops.catch(lambda e, source: of({"error": str(e)}))
).subscribe(
    on_next=lambda result: print(f"Result: {result}"),
    on_error=lambda e: print(f"Final error: {e}"),
    on_completed=lambda: print("Processing completed")
)

# Game loop
while not rl.window_should_close():
    if rl.is_key_pressed(rl.KEY_SPACE):
        unreliable_service.on_next("Request")
    
    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)
    rl.draw_text("Press SPACE to send request", 190, 200, 20, rl.MAROON)
    rl.draw_text("Check console for results", 190, 230, 20, rl.MAROON)
    rl.end_drawing()

rl.close_window()
