import tkinter as tk
from tkinter import messagebox
import sys

# Structure to hold counter state
class CounterState:
    def __init__(self):
        self.count = 0
        self.label = None

# Global state
state = CounterState()

# Increment counter and update display
def increment_counter():
    state.count += 1
    if state.label:
        state.label.config(text=f"Count: {state.count}")

# Create and run the GUI
def create_window():
    try:
        root = tk.Tk()
        root.title("Python Counter")
        root.geometry("300x200")

        # Create and pack label
        state.label = tk.Label(root, text=f"Count: {state.count}", font=("Arial", 14))
        state.label.pack(pady=20)

        # Create and pack button
        button = tk.Button(root, text="Increment", command=increment_counter)
        button.pack(pady=10)

        # Handle window close
        root.protocol("WM_DELETE_WINDOW", lambda: root.quit())

        # Start main loop
        root.mainloop()

    except tk.TclError as e:
        print(f"Failed to create GUI: {e}")
        sys.exit(1)

# Main function
def main():
    create_window()

if __name__ == "__main__":
    main()
