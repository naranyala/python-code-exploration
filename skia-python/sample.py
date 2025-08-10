import skia
import glfw
from OpenGL.GL import *

# Window dimensions
width, height = 400, 400

# Initialize GLFW
if not glfw.init():
    exit(1)

# Create a window
window = glfw.create_window(width, height, "Centered Circle", None, None)
if not window:
    glfw.terminate()
    exit(1)

# Set up OpenGL context
glfw.make_context_current(window)

# Create Skia surface for OpenGL
def create_skia_surface(width, height):
    context = skia.GrContext.MakeGL()
    info = skia.ImageInfo.MakeN32Premul(width, height)
    surface = skia.Surface.MakeRenderTarget(context, skia.Budgeted.kNo, info)
    return surface, context

# Main render loop
surface, context = create_skia_surface(width, height)
while not glfw.window_should_close(window):
    # Get current window size
    w, h = glfw.get_framebuffer_size(window)
    glViewport(0, 0, w, h)
    
    # Clear OpenGL buffer
    glClearColor(1.0, 1.0, 1.0, 1.0)  # White background
    glClear(GL_COLOR_BUFFER_BIT)
    
    # Draw with Skia
    with surface as canvas:
        canvas.clear(skia.ColorWHITE)
        paint = skia.Paint(
            Color=skia.ColorGREEN,
            AntiAlias=True,
            Style=skia.Paint.kFill_Style
        )
        canvas.drawCircle(w / 2, h / 2, 100, paint)
    
    # Flush Skia and swap buffers
    surface.flushAndSubmit()
    glfw.swap_buffers(window)
    glfw.poll_events()

# Cleanup
glfw.terminate()
