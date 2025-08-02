#!/usr/bin/env python3
"""
Linux Power Menu - Python Raylib Version
Reactive state management system with 2x2 grid navigation
"""

import raylib as rl
from raylib import colors
import subprocess
from typing import Dict, List, Callable, Any, Optional


class ReactiveMap:
    """Generic reactive map that triggers callbacks on value changes"""

    def __init__(self):
        self.data: Dict[str, Any] = {}
        self.callbacks: Dict[str, List[Callable[[Any, Any], None]]] = {}
        self.contexts: Dict[str, List[Any]] = {}

    def set_key(self, key: str, value: Any) -> None:
        """Set key value and trigger callbacks if value changed"""
        if key in self.data and self.data[key] == value:
            return

        self.data[key] = value

        if key in self.callbacks:
            for i, callback in enumerate(self.callbacks[key]):
                ctx = self.contexts[key][i] if i < len(self.contexts[key]) else None
                callback(value, ctx)

    def get_key(self, key: str, default: Any = None) -> Any:
        """Get key value or return default"""
        return self.data.get(key, default)

    def subscribe_key(self, key: str, callback: Callable[[Any, Any], None], ctx: Any = None) -> None:
        """Subscribe callback to key changes"""
        if key not in self.callbacks:
            self.callbacks[key] = []
            self.contexts[key] = []

        self.callbacks[key].append(callback)
        self.contexts[key].append(ctx)


class Effect:
    """Effect that can be triggered by reactive changes"""

    def __init__(self, name: str, run_fn: Callable[[Any], None], ctx: Any = None):
        self.name = name
        self.run_fn = run_fn
        self.ctx = ctx
        self.triggers = 0

        # Execute immediately
        self.run_fn(self.ctx)

    def execute(self) -> None:
        """Execute the effect"""
        self.triggers += 1
        self.run_fn(self.ctx)


class GridMenuContext:
    """Context for grid menu state"""

    def __init__(self):
        self.store = ReactiveMap()
        self.selected_index = ReactiveMap()


# Power actions configuration
ACTIONS = ["logout", "reboot", "suspend", "shutdown"]

ACTION_LABELS = {
    "logout": "Logout",
    "reboot": "Reboot",
    "suspend": "Suspend",
    "shutdown": "Shutdown"
}


def run_action(action: str) -> None:
    """Execute system power action"""
    commands = {
        "logout": "pkill -KILL -u $(whoami)",
        "reboot": "systemctl reboot",
        "suspend": "systemctl suspend",
        "shutdown": "systemctl poweroff"
    }

    if action in commands:
        subprocess.run(commands[action], shell=True)


def confirm_effect_fn(ctx: GridMenuContext) -> None:
    """Effect function that handles confirmation logic"""
    requested_action = ctx.store.get_key("requested_action", "")
    confirmation = ctx.store.get_key("confirmation", "")

    if requested_action != "" and confirmation == "yes":
        run_action(requested_action)
        ctx.store.set_key("requested_action", "")
        ctx.store.set_key("confirmation", "")
    elif confirmation == "no":
        ctx.store.set_key("requested_action", "")
        ctx.store.set_key("confirmation", "")


def subscribe_effect_to_key(store: ReactiveMap, key: str, effect: Effect) -> None:
    """Subscribe effect to reactive key changes"""
    def callback(value: Any, ctx: Effect) -> None:
        ctx.execute()

    store.subscribe_key(key, callback, effect)


def main():
    # Initialize window
    screen_width = 600
    screen_height = 400
    window_title = "Linux Power Menu"

    rl.InitWindow(screen_width, screen_height, window_title.encode('utf-8'))
    rl.SetTargetFPS(60)

    # Initialize reactive state
    ctx = GridMenuContext()
    ctx.store.set_key("requested_action", "")
    ctx.store.set_key("confirmation", "")
    ctx.selected_index.set_key("index", 0)

    # Create confirmation effect
    confirm_effect = Effect("confirm_effect", confirm_effect_fn, ctx)
    subscribe_effect_to_key(ctx.store, "confirmation", confirm_effect)

    # Main loop
    while not rl.WindowShouldClose():
        requested_action = ctx.store.get_key("requested_action", "")

        if requested_action == "":
            # Handle grid navigation
            current_index = ctx.selected_index.get_key("index", 0)
            new_index = current_index

            # Fixed 2x2 grid navigation
            if rl.IsKeyPressed(rl.KEY_RIGHT):
                new_index = current_index + 1 if current_index % 2 == 0 else current_index - 1
            elif rl.IsKeyPressed(rl.KEY_LEFT):
                new_index = current_index - 1 if current_index % 2 == 1 else current_index + 1
            elif rl.IsKeyPressed(rl.KEY_DOWN):
                new_index = (current_index + 2) % 4
            elif rl.IsKeyPressed(rl.KEY_UP):
                new_index = (current_index + 2) % 4

            ctx.selected_index.set_key("index", new_index)

            # Handle selection
            if rl.IsKeyPressed(rl.KEY_ENTER):
                action = ACTIONS[new_index]
                ctx.store.set_key("requested_action", action)

        else:
            # Handle confirmation
            if rl.IsKeyPressed(rl.KEY_Y):
                ctx.store.set_key("confirmation", "yes")
            elif rl.IsKeyPressed(rl.KEY_N):
                ctx.store.set_key("confirmation", "no")

        # Drawing
        rl.BeginDrawing()
        rl.ClearBackground(colors.RAYWHITE)

        # Draw title
        title_text = "Power Menu (arrows + Enter)"
        rl.DrawText(title_text.encode('utf-8'), 20, 20, 20, colors.DARKGRAY)

        # Draw 2x2 grid of action buttons
        box_width = 250
        box_height = 80
        selected_index = ctx.selected_index.get_key("index", 0)

        for i in range(4):
            x = 50 + (i % 2) * (box_width + 20)
            y = 80 + (i // 2) * (box_height + 20)

            # Determine button color
            button_color = colors.DARKBLUE if i == selected_index else colors.GRAY

            # Draw button rectangle
            rl.DrawRectangle(x, y, box_width, box_height, button_color)

            # Draw button label
            action = ACTIONS[i]
            if action in ACTION_LABELS:
                label = ACTION_LABELS[action]
                label_bytes = label.encode('utf-8')
                rl.DrawText(label_bytes, x + 20, y + 25, 28, colors.RAYWHITE)

        # Draw confirmation overlay
        if requested_action != "":
            if requested_action in ACTION_LABELS:
                action_label = ACTION_LABELS[requested_action].upper()
                confirm_text = f"Confirm {action_label}? [Y/N]"

                # Draw semi-transparent overlay background
                rl.DrawRectangle(0, 0, screen_width, screen_height, colors.BLACK)

                # Draw confirmation text
                confirm_bytes = confirm_text.encode('utf-8')
                rl.DrawText(confirm_bytes, 100, 180, 28, colors.RAYWHITE)

        rl.EndDrawing()

    # Cleanup
    rl.CloseWindow()


if __name__ == "__main__":
    main()
