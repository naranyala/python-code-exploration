import asyncio
import platform
import pyray as rl

# Package-level variables for animation state
scale = 0.0
text_scale = 0.0

def ui_modal(title, message, is_open, buttons, bounds=(0, 0, 400, 300), anim_speed=0.15, text_anim_speed=0.3):
    global scale, text_scale
    # Create modifiable copy of bounds
    modal_bounds = list(bounds)

    # Center if using default position
    if modal_bounds[0] == 0 and modal_bounds[1] == 0:
        modal_bounds[0] = (rl.get_screen_width() - modal_bounds[2]) / 2
        modal_bounds[1] = (rl.get_screen_height() - modal_bounds[3]) / 2

    # Animation state
    target_scale = 1.0 if is_open[0] else 0.0
    scale += (target_scale - scale) * anim_speed
    text_scale += (target_scale - text_scale) * text_anim_speed

    # Early exit if closed
    if scale <= 0.01 and not is_open[0]:
        return -1

    mouse = rl.get_mouse_position()
    result = -1

    # Constants for layout
    PADDING = 20
    TITLE_HEIGHT = 40
    BUTTON_HEIGHT = 40
    BUTTON_SPACING = 10

    # Draw overlay
    if scale > 0:
        rl.draw_rectangle(
            0,
            0,
            rl.get_screen_width(),
            rl.get_screen_height(),
            rl.Color(0, 0, 0, int(200 * scale))
        )

    # Draw modal content
    if scale > 0.01:
        # Calculate animated bounds
        scaled_bounds = modal_bounds.copy()
        scaled_bounds[2] *= scale
        scaled_bounds[3] *= scale
        scaled_bounds[0] = modal_bounds[0] + (modal_bounds[2] - scaled_bounds[2]) / 2
        scaled_bounds[1] = modal_bounds[1] + (modal_bounds[3] - scaled_bounds[3]) / 2

        # Main panel
        rl.draw_rectangle_rec(rl.Rectangle(*scaled_bounds), rl.WHITE)
        rl.draw_rectangle_lines_ex(rl.Rectangle(*scaled_bounds), 2, rl.BLACK)

        # Title area
        title_rect = (
            scaled_bounds[0] + PADDING,
            scaled_bounds[1] + PADDING,
            scaled_bounds[2] - 2 * PADDING,
            TITLE_HEIGHT
        )
        rl.draw_text_ex(
            rl.get_font_default(),
            title,
            rl.Vector2(title_rect[0], title_rect[1]),
            24,
            1,
            rl.Color(0, 0, 0, int(255 * text_scale))
        )

        # Message area
        msg_pos = rl.Vector2(scaled_bounds[0] + PADDING, scaled_bounds[1] + PADDING + TITLE_HEIGHT)
        msg_width = scaled_bounds[2] - 2 * PADDING
        rl.draw_text_ex(
            rl.get_font_default(),
            message,
            msg_pos,
            20,
            1,
            rl.Color(64, 64, 64, int(255 * text_scale))
        )

        # Buttons
        button_width = (scaled_bounds[2] - 2 * PADDING - (len(buttons) - 1) * BUTTON_SPACING) / len(buttons)
        button_y = scaled_bounds[1] + scaled_bounds[3] - BUTTON_HEIGHT - PADDING

        for i, button in enumerate(buttons):
            button_rect = rl.Rectangle(
                scaled_bounds[0] + PADDING + i * (button_width + BUTTON_SPACING),
                button_y,
                button_width,
                BUTTON_HEIGHT
            )

            # Button state
            hovered = rl.check_collision_point_rec(mouse, button_rect)
            color = rl.SKYBLUE if hovered else rl.LIGHTGRAY

            # Draw button
            rl.draw_rectangle_rec(button_rect, color)
            rl.draw_rectangle_lines_ex(button_rect, 1, rl.BLACK)

            # Center text
            text_width = rl.measure_text(button, 20)
            rl.draw_text(
                button,
                int(button_rect.x + (button_rect.width - text_width) / 2),
                int(button_rect.y + BUTTON_HEIGHT / 2 - 10),
                20,
                rl.Color(0, 0, 0, int(255 * text_scale))
            )

            # Handle click
            if hovered and rl.is_mouse_button_released(rl.MouseButton.MOUSE_BUTTON_LEFT):
                result = i
                is_open[0] = False

        # Close when clicking outside
        if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT):
            if not rl.check_collision_point_rec(mouse, rl.Rectangle(*scaled_bounds)):
                is_open[0] = False

    return result

def setup():
    rl.init_window(800, 600, "Modal Demo")
    return True

def update_loop():
    global show_modal, last_result
    if rl.window_should_close():
        return False

    if rl.is_key_pressed(rl.KeyboardKey.KEY_F):
        show_modal[0] = not show_modal[0]

    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)
    rl.draw_text("Press F to toggle modal", 20, 20, 20, rl.BLACK)

    # Show modal
    result = ui_modal(
        "Confirm Action",
        "Are you sure you want to proceed?\nThis action cannot be undone.\n\nPlease confirm your choice:",
        show_modal,
        ["Yes", "No", "Cancel"],
        anim_speed=0.2,
        text_anim_speed=0.3
    )

    if result >= 0:
        last_result = result

    if last_result >= 0:
        status = f"Last selection: {last_result}"
        rl.draw_text(status, 20, 50, 20, rl.BLACK)

    rl.end_drawing()
    return True

async def main():
    setup()
    global show_modal, last_result
    show_modal = [False]  # Mutable boolean
    last_result = -1
    FPS = 60

    while update_loop():
        await asyncio.sleep(1.0 / FPS)

    rl.close_window()

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())
