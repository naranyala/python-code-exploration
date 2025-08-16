import { h, render, createRef } from 'preact';
import { signal, computed } from '@preact/signals';
import { useEffect, useState } from 'preact/hooks';
import { setup, css } from 'goober';

// Set up Goober for Preact
setup(h);

// Styles
const styles = {
  container: css`
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    padding: 1rem;
    box-sizing: border-box;
  `,
  header: css`
    text-align: center;
    margin-bottom: 2rem;
    color: white;
    font-size: 2rem;
    font-weight: 300;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    
    @media (max-width: 768px) {
      font-size: 1.5rem;
      margin-bottom: 1.5rem;
    }
  `,
  canvasWrapper: css`
    position: relative;
    border-radius: 50%;
    padding: 20px;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    border: 1px solid rgba(255, 255, 255, 0.18);
  `,
  canvas: css`
    border-radius: 50%;
    background: radial-gradient(circle at center, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
    display: block;
    width: 400px;
    height: 400px;
    max-width: 80vw;
    max-height: 80vw;
    
    @media (max-width: 768px) {
      width: 300px;
      height: 300px;
    }
  `,
  controls: css`
    margin-top: 2rem;
    display: flex;
    gap: 1rem;
    
    @media (max-width: 768px) {
      flex-direction: column;
      width: 100%;
      max-width: 250px;
    }
  `,
  button: css`
    padding: 12px 24px;
    border: none;
    border-radius: 25px;
    cursor: pointer;
    font-weight: 500;
    font-size: 1rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    color: white;
    text-transform: uppercase;
    letter-spacing: 1px;
    position: relative;
    overflow: hidden;
    
    &:before {
      content: '';
      position: absolute;
      top: 0;
      left: -100%;
      width: 100%;
      height: 100%;
      background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
      transition: left 0.5s;
    }
    
    &:hover:before {
      left: 100%;
    }
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    }
    
    &:active {
      transform: translateY(0);
    }
    
    @media (max-width: 768px) {
      width: 100%;
    }
  `,
  startButton: css`
    background: linear-gradient(135deg, #4CAF50, #45a049);
    box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
    
    &:hover {
      background: linear-gradient(135deg, #45a049, #4CAF50);
    }
  `,
  stopButton: css`
    background: linear-gradient(135deg, #f44336, #da190b);
    box-shadow: 0 4px 15px rgba(244, 67, 54, 0.3);
    
    &:hover {
      background: linear-gradient(135deg, #da190b, #f44336);
    }
  `,
  presetControls: css`
    margin-top: 1rem;
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    justify-content: center;
    
    @media (max-width: 768px) {
      flex-direction: column;
    }
  `,
  presetButton: css`
    padding: 8px 16px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.1);
    color: white;
    cursor: pointer;
    font-size: 0.85rem;
    transition: all 0.2s ease;
    
    &:hover {
      background: rgba(255, 255, 255, 0.2);
      border-color: rgba(255, 255, 255, 0.5);
    }
    
    @media (max-width: 768px) {
      width: 100%;
    }
  `
};

// Animation state
const isAnimating = signal(false);
const animationSpeed = signal(1);
const circleCount = signal(6);
const currentPreset = signal('default');

// Animation presets
const presets = {
  default: { speed: 1, count: 6, colors: ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3'] },
  fast: { speed: 2.5, count: 8, colors: ['#ff3838', '#ff9500', '#ffdd00', '#00ff00', '#0099ff', '#9500ff'] },
  slow: { speed: 0.5, count: 4, colors: ['#667eea', '#764ba2', '#f093fb', '#f5576c'] },
  many: { speed: 1.2, count: 12, colors: ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3', '#6c5ce7', '#fd79a8', '#fdcb6e', '#55a3ff', '#00b894', '#e17055'] }
};

// Circle class for individual circle management
class AnimatedCircle {
  constructor(centerX, centerY, index, totalCircles) {
    this.centerX = centerX;
    this.centerY = centerY;
    this.index = index;
    this.totalCircles = totalCircles;
    this.baseRadius = 30 + (index * 25);
    this.angle = (index * Math.PI * 2) / totalCircles;
    this.speed = 0.02 + (index * 0.005);
    this.pulsePhase = index * 0.5;
    this.orbitRadius = 80 + (index * 15);
    this.color = presets[currentPreset.value].colors[index % presets[currentPreset.value].colors.length];
  }

  update(time) {
    const preset = presets[currentPreset.value];
    this.angle += this.speed * animationSpeed.value;
    this.pulsePhase += 0.03 * animationSpeed.value;
    
    // Update position (orbital motion)
    this.x = this.centerX + Math.cos(this.angle) * this.orbitRadius;
    this.y = this.centerY + Math.sin(this.angle) * this.orbitRadius;
    
    // Update size (pulsing)
    this.radius = this.baseRadius + Math.sin(this.pulsePhase) * 10;
    
    // Update opacity
    this.opacity = 0.6 + Math.sin(this.pulsePhase * 1.5) * 0.3;
    
    // Update color rotation
    this.colorIndex = (this.index + Math.floor(time * 0.5)) % preset.colors.length;
    this.color = preset.colors[this.colorIndex];
  }

  draw(ctx) {
    ctx.save();
    
    // Create gradient
    const gradient = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.radius);
    gradient.addColorStop(0, this.color + 'dd');
    gradient.addColorStop(0.7, this.color + '88');
    gradient.addColorStop(1, this.color + '00');
    
    // Draw circle
    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
    ctx.fill();
    
    // Add inner glow
    ctx.fillStyle = this.color + 'aa';
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.radius * 0.3, 0, Math.PI * 2);
    ctx.fill();
    
    ctx.restore();
  }
}

// Animation manager
class CircleAnimationManager {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.circles = [];
    this.animationId = null;
    this.startTime = 0;
    this.setupCanvas();
    this.createCircles();
  }

  setupCanvas() {
    const rect = this.canvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    
    this.canvas.width = rect.width * dpr;
    this.canvas.height = rect.height * dpr;
    
    this.ctx.scale(dpr, dpr);
    this.canvas.style.width = rect.width + 'px';
    this.canvas.style.height = rect.height + 'px';
    
    this.centerX = rect.width / 2;
    this.centerY = rect.height / 2;
  }

  createCircles() {
    this.circles = [];
    const count = circleCount.value;
    
    for (let i = 0; i < count; i++) {
      this.circles.push(new AnimatedCircle(this.centerX, this.centerY, i, count));
    }
  }

  animate = (currentTime) => {
    if (!this.startTime) this.startTime = currentTime;
    const elapsed = (currentTime - this.startTime) / 1000;

    // Clear canvas with fade effect
    this.ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // Update and draw circles
    this.circles.forEach(circle => {
      circle.update(elapsed);
      circle.draw(this.ctx);
    });

    // Draw central pulse
    this.drawCenterPulse(elapsed);

    if (isAnimating.value) {
      this.animationId = requestAnimationFrame(this.animate);
    }
  }

  drawCenterPulse(time) {
    const pulseRadius = 20 + Math.sin(time * 3) * 15;
    const pulseOpacity = 0.3 + Math.sin(time * 2) * 0.2;
    
    const gradient = this.ctx.createRadialGradient(
      this.centerX, this.centerY, 0,
      this.centerX, this.centerY, pulseRadius
    );
    
    gradient.addColorStop(0, `rgba(255, 255, 255, ${pulseOpacity})`);
    gradient.addColorStop(1, 'rgba(255, 255, 255, 0)');
    
    this.ctx.fillStyle = gradient;
    this.ctx.beginPath();
    this.ctx.arc(this.centerX, this.centerY, pulseRadius, 0, Math.PI * 2);
    this.ctx.fill();
  }

  start() {
    if (!isAnimating.value) {
      isAnimating.value = true;
      this.startTime = 0;
      this.animationId = requestAnimationFrame(this.animate);
    }
  }

  stop() {
    isAnimating.value = false;
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
      this.animationId = null;
    }
  }

  updatePreset(presetName) {
    currentPreset.value = presetName;
    const preset = presets[presetName];
    animationSpeed.value = preset.speed;
    circleCount.value = preset.count;
    this.createCircles();
  }

  cleanup() {
    this.stop();
  }
}

// Main App Component
const App = () => {
  const canvasRef = createRef();
  const [manager, setManager] = useState(null);

  useEffect(() => {
    if (!canvasRef.current) return;

    const animationManager = new CircleAnimationManager(canvasRef.current);
    setManager(animationManager);

    return () => {
      animationManager.cleanup();
    };
  }, []);

  const handleStart = () => {
    if (manager) manager.start();
  };

  const handleStop = () => {
    if (manager) manager.stop();
  };

  const handlePresetChange = (presetName) => {
    if (manager) {
      manager.updatePreset(presetName);
    }
  };

  return (
    <div class={styles.container}>
      <h1 class={styles.header}>Orbital Circle Symphony</h1>
      
      <div class={styles.canvasWrapper}>
        <canvas 
          ref={canvasRef} 
          class={styles.canvas}
        />
      </div>

      <div class={styles.controls}>
        <button
          class={`${styles.button} ${styles.startButton}`}
          onClick={handleStart}
        >
          Start
        </button>
        <button
          class={`${styles.button} ${styles.stopButton}`}
          onClick={handleStop}
        >
          Stop
        </button>
      </div>

      <div class={styles.presetControls}>
        {Object.keys(presets).map(presetName => (
          <button
            key={presetName}
            class={styles.presetButton}
            onClick={() => handlePresetChange(presetName)}
            style={{
              background: currentPreset.value === presetName 
                ? 'rgba(255, 255, 255, 0.3)' 
                : 'rgba(255, 255, 255, 0.1)'
            }}
          >
            {presetName.charAt(0).toUpperCase() + presetName.slice(1)}
          </button>
        ))}
      </div>
    </div>
  );
};

export default App;
