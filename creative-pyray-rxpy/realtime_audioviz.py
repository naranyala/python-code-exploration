
import pyray as pr
import numpy as np
import sounddevice as sd

# Audio settings
SAMPLE_RATE = 44100
BUFFER_SIZE = 1024

# Visualization settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
NUM_BANDS = 64

# Initialize pyray window
pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, b"Audio Visualizer")
pr.set_target_fps(60)

# Audio callback
audio_buffer = np.zeros(BUFFER_SIZE)

def audio_callback(indata, frames, time, status):
    global audio_buffer
    audio_buffer = indata[:, 0]  # Mono channel

# Start audio stream
stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=SAMPLE_RATE, blocksize=BUFFER_SIZE)
stream.start()

while not pr.window_should_close():
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)

    # FFT analysis
    fft = np.abs(np.fft.rfft(audio_buffer))[:NUM_BANDS]
    fft = np.clip(fft / np.max(fft), 0, 1)  # Normalize

    # Draw bars
    bar_width = SCREEN_WIDTH / NUM_BANDS
    for i in range(NUM_BANDS):
        bar_height = fft[i] * SCREEN_HEIGHT
        x = i * bar_width
        y = SCREEN_HEIGHT - bar_height
        pr.draw_rectangle(int(x), int(y), int(bar_width - 2), int(bar_height), pr.RAYWHITE)

    pr.end_drawing()

# Cleanup
stream.stop()
pr.close_window()
