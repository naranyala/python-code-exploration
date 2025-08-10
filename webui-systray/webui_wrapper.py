# webui_wrapper.py
from .webui_bindings import ffi, lib
import os

class WebUIWindow:
    def __init__(self):
        self._window = lib.webui_new_window()
    
    def show(self, content, browser=0):
        """Show the window with the specified content.
        
        Args:
            content: HTML content or URL to show
            browser: 0 for default browser, or specific browser enum value
        """
        lib.webui_show(self._window, content.encode('utf-8'), browser)
    
    def bind(self, element, callback):
        """Bind a Python callback to a UI element.
        
        Args:
            element: ID of the HTML element to bind to
            callback: Python function to call when event occurs
        """
        @ffi.callback("void(webui_event_t)")
        def wrapped_callback(event):
            # Convert event to a more Pythonic object if needed
            callback(WebUIEvent(event))
        
        self._callbacks.append(wrapped_callback)  # Keep reference to prevent GC
        lib.webui_bind(self._window, element.encode('utf-8'), wrapped_callback)
    
    def set_root_folder(self, path):
        """Set the root folder for file operations."""
        lib.webui_set_root_folder(self._window, path.encode('utf-8'))
    
    def run_js(self, script, timeout=0):
        """Run JavaScript in the window."""
        buffer = ffi.new("char[]", 4096)  # Create a buffer for the response
        lib.webui_script(self._window, script.encode('utf-8'), timeout, buffer, 4096)
        return ffi.string(buffer).decode('utf-8')
    
    def loop(self):
        """Start the main event loop."""
        lib.webui_loop()
    
    def exit(self):
        """Exit the application."""
        lib.webui_exit()

class WebUIEvent:
    def __init__(self, event_ptr):
        self._event = event_ptr
    
    @property
    def window(self):
        return WebUIWindow._from_existing(lib.webui_event_get_window(self._event))
    
    @property
    def element(self):
        return ffi.string(lib.webui_event_get_element(self._event)).decode('utf-8')
    
    def get_string(self):
        return ffi.string(lib.webui_event_get_string(self._event)).decode('utf-8')
    
    def get_int(self):
        return lib.webui_event_get_int(self._event)
    
    def get_bool(self):
        return bool(lib.webui_event_get_bool(self._event))
    
    def return_string(self, value):
        lib.webui_event_return_string(self._event, value.encode('utf-8'))
    
    def return_int(self, value):
        lib.webui_event_return_int(self._event, value)
    
    def return_bool(self, value):
        lib.webui_event_return_bool(self._event, value)
