import pyray as pr
import numpy as np
import sounddevice as sd
import math

# Audio settings
SAMPLE_RATE = 44100
BUFFER_SIZE = 1024

# Visualization settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
NUM_BANDS = 64
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2
MIN_RADIUS = 100
MAX_RADIUS = 250

# Smoothing settings
SMOOTHING_FACTOR = 0.85
NOISE_FLOOR = 0.002      # Slightly higher to filter low freq noise
MIN_AMPLITUDE = 0.01     # Minimum visible amplitude

# Initialize pyray window
pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, b"Circular Audio Visualizer")
pr.set_target_fps(60)

# Audio callback
audio_buffer = np.zeros(BUFFER_SIZE)
smoothed_fft = np.zeros(NUM_BANDS)

def audio_callback(indata, frames, time, status):
    global audio_buffer
    audio_buffer = indata[:, 0]  # Mono channel

# Start audio stream
stream = sd.InputStream(callback=audio_callback, channels=1, 
                       samplerate=SAMPLE_RATE, blocksize=BUFFER_SIZE)
stream.start()

while not pr.window_should_close():
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    
    # Apply window function and high-pass filter
    windowed = audio_buffer * np.hanning(len(audio_buffer))
    
    # FFT analysis - skip more low frequency bins to avoid DC and low freq noise
    fft_raw = np.abs(np.fft.rfft(windowed))[3:NUM_BANDS+3]  # Skip first 3 bins
    
    # Apply logarithmic scaling for better frequency distribution
    fft_raw = np.log1p(fft_raw * 1000) / np.log1p(1000)
    
    # Normalize with safe division
    max_val = np.max(fft_raw)
    if max_val > NOISE_FLOOR:
        fft_normalized = np.clip(fft_raw / max_val, 0, 1)
    else:
        fft_normalized = np.zeros(NUM_BANDS)
    
    # Apply noise floor and minimum amplitude
    fft_normalized = np.where(fft_normalized < NOISE_FLOOR, 0, fft_normalized)
    fft_normalized = np.maximum(fft_normalized, MIN_AMPLITUDE * np.random.random(NUM_BANDS) * 0.1)
    
    # Smooth the FFT values with different rates for different frequencies
    for i in range(NUM_BANDS):
        # Lower frequencies get more smoothing
        freq_smoothing = SMOOTHING_FACTOR + (1 - SMOOTHING_FACTOR) * (i / NUM_BANDS) * 0.3
        smoothed_fft[i] = freq_smoothing * smoothed_fft[i] + (1 - freq_smoothing) * fft_normalized[i]
    
    # Additional processing to ensure all bars animate
    # Add subtle random variation to prevent static bars
    variation = np.random.random(NUM_BANDS) * 0.02
    smoothed_fft = np.maximum(smoothed_fft + variation, MIN_AMPLITUDE)
    
    # Draw circular visualization
    angle_step = 2 * math.pi / NUM_BANDS
    
    for i in range(NUM_BANDS):
        # Calculate angle for this band
        angle = i * angle_step
        
        # Calculate radius based on smoothed FFT magnitude
        radius = MIN_RADIUS + (smoothed_fft[i] * (MAX_RADIUS - MIN_RADIUS))
        
        # Calculate line endpoints
        inner_x = CENTER_X + MIN_RADIUS * math.cos(angle)
        inner_y = CENTER_Y + MIN_RADIUS * math.sin(angle)
        outer_x = CENTER_X + radius * math.cos(angle)
        outer_y = CENTER_Y + radius * math.sin(angle)
        
        # Color based on frequency band with better distribution
        # Avoid pure red at the start by offsetting the hue
        hue = ((i / NUM_BANDS) * 300 + 60) % 360  # Start from yellow, avoid red
        intensity = 0.4 + 0.6 * smoothed_fft[i]
        saturation = 0.8 + 0.2 * smoothed_fft[i]
        color = pr.color_from_hsv(hue, saturation, intensity)
        
        # Line thickness based on amplitude
        thickness = 2.0 + smoothed_fft[i] * 3.0
        
        # Draw line from inner circle to outer position
        pr.draw_line_ex(pr.Vector2(inner_x, inner_y), 
                        pr.Vector2(outer_x, outer_y), 
                        thickness, color)
    
    # Draw center circle with pulsing
    avg_amplitude = np.mean(smoothed_fft)
    pulse_radius = MIN_RADIUS * (0.95 + 0.05 * avg_amplitude)
    center_brightness = int(40 + 60 * avg_amplitude)
    
    pr.draw_circle(CENTER_X, CENTER_Y, pulse_radius, 
                   pr.Color(center_brightness, center_brightness, center_brightness, 255))
    pr.draw_circle_lines(CENTER_X, CENTER_Y, MIN_RADIUS, pr.GRAY)
    
    pr.end_drawing()

# Cleanup
stream.stop()
pr.close_window()
