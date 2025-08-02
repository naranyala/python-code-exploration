import pyray as rl
from rx.subject import BehaviorSubject
from rx import operators as ops

rl.init_window(800, 600, "State Management")
rl.set_target_fps(60)

# Reactive state management
game_state = BehaviorSubject({
    "score": 0,
    "level": 1,
    "player_health": 100
})

# Process state changes reactively
game_state.pipe(
    ops.map(lambda state: {
        **state,
        "level": state["score"] // 100 + 1
    }),
    ops.distinct_until_changed()
).subscribe(
    on_next=lambda state: game_state.on_next(state),
    on_error=lambda e: print(f"State error: {e}")
)

# Input handling
input_stream = BehaviorSubject(None)

input_stream.pipe(
    ops.filter(lambda key: key == rl.KEY_SPACE),
    ops.with_latest_from(game_state),
    ops.map(lambda pair: {
        **pair[1],
        "score": pair[1]["score"] + 10
    })
).subscribe(
    on_next=game_state.on_next,
    on_error=lambda e: print(f"Input error: {e}")
)

# Game loop
while not rl.window_should_close():
    # Emit input events
    if rl.is_key_pressed(rl.KEY_SPACE):
        input_stream.on_next(rl.KEY_SPACE)
    
    # Get current state
    current_state = game_state.value
    
    # Drawing
    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)
    rl.draw_text(f"Score: {current_state['score']}", 10, 10, 20, rl.BLACK)
    rl.draw_text(f"Level: {current_state['level']}", 10, 40, 20, rl.BLACK)
    rl.draw_text(f"Health: {current_state['player_health']}", 10, 70, 20, rl.BLACK)
    rl.end_drawing()

rl.close_window()
