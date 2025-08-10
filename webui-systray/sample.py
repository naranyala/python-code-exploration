from webui_wrapper import WebUIWindow

def button_click(event):
    print(f"Button clicked! Element: {event.element}")
    event.return_string("Hello from Python!")

def main():
    # Create a new window
    window = WebUIWindow()
    
    # Bind a Python function to a button click
    window.bind("myButton", button_click)
    
    # HTML content
    html = """
    <html>
    <body>
        <button id="myButton">Click Me</button>
    </body>
    </html>
    """
    
    # Show the window
    window.show(html)
    
    # Start the event loop
    window.loop()

if __name__ == "__main__":
    main()
