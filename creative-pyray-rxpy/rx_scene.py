
import pyray as rl 
from rx.subject import BehaviorSubject

rl.init_window(640, 480, b"Reactive Scene Switch")
rl.set_target_fps(60)

scene_subject = BehaviorSubject("menu")

# Switch to "game" on Enter key
def check_scene_switch():
    if rl.is_key_pressed(rl.KEY_ENTER):
        current = scene_subject.value
        next_scene = "game" if current == "menu" else "menu"
        scene_subject.on_next(next_scene)

def draw_menu():
    rl.draw_text("MENU: Press Enter to Start Game", 100, 200, 20, rl.DARKGREEN)

def draw_game():
    rl.draw_text("GAME: Press Enter to return to Menu", 100, 200, 20, rl.MAROON)

# Reactively redraw based on scene
current_scene = "menu"
scene_subject.subscribe(lambda s: globals().__setitem__('current_scene', s))

while not rl.window_should_close():
    check_scene_switch()

    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)
    draw_func = draw_menu if current_scene == "menu" else draw_game
    draw_func()
    rl.end_drawing()

rl.close_window()
