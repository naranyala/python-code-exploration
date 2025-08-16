import { h, render, createRef } from 'preact';
import { signal, effect } from '@preact/signals';
import { setup, css } from 'goober';
import { useState, useEffect } from 'preact/hooks';

// Set up Goober for Preact
setup(h);

// Grouped styles with mobile responsiveness
const styles = {
  container: css`
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    background: #f0f4f8;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    padding: 1rem;
    box-sizing: border-box;

    @media (max-width: 768px) {
      padding: 0.5rem;
    }
  `,
  header: css`
    text-align: center;
    margin-bottom: 1.5rem;
    color: #333;
    font-size: 1.5rem;

    @media (max-width: 768px) {
      font-size: 1.2rem;
      margin-bottom: 1rem;
    }
  `,
  canvasContainer: css`
    position: relative;
    width: 400px;
    height: 400px;
    max-width: 80vw;
    max-height: 80vh;
    aspect-ratio: 1 / 1;
  `,
  canvas: css`
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background: white;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);

    @media (max-width: 768px) {
      max-width: 90vw;
      max-height: 90vh;
    }
  `,
  controls: css`
    margin-top: 1.5rem;
    display: flex;
    gap: 1rem;

    @media (max-width: 768px) {
      flex-direction: column;
      gap: 0.75rem;
      width: 100%;
      max-width: 300px;
    }
  `,
  button: css`
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 500;
    transition: all 0.2s ease;
    color: white;
    touch-action: manipulation;

    &:hover {
      opacity: 0.9;
      transform: scale(1.02);
    }

    @media (max-width: 768px) {
      padding: 0.6rem 1rem;
      font-size: 0.9rem;
      width: 100%;
    }
  `,
  startButton: css`
    background: #28a745;
  `,
  stopButton: css`
    background: #dc3545;
  `,
  error: css`
    color: #dc3545;
    text-align: center;
    margin-top: 1rem;
    font-size: 0.9rem;
  `
};

// Signals for reactive state
const isAnimating = signal(false);
const animationFrameId = signal(null);
const webglError = signal('');

// Helper function to compile shader
const compileShader = (gl, source, type) => {
  const shader = gl.createShader(type);
  gl.shaderSource(shader, source);
  gl.compileShader(shader);
  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    console.error('Shader compile error:', gl.getShaderInfoLog(shader));
    return null;
  }
  return shader;
};

// WebGL setup class to manage context and resources
class WebGLManager {
  constructor(canvas) {
    this.canvas = canvas;
    this.gl = null;
    this.program = null;
    this.uniforms = {};
    this.buffers = {};
    this.startTime = Date.now();
  }

  init() {
    // Set canvas size to match display size
    const rect = this.canvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    this.canvas.width = rect.width * dpr;
    this.canvas.height = rect.height * dpr;

    this.gl = this.canvas.getContext('webgl', { 
      alpha: true, 
      premultipliedAlpha: false 
    });

    if (!this.gl) {
      webglError.value = 'WebGL is not supported in this browser.';
      return false;
    }

    return this.setupShaders() && this.setupGeometry();
  }

  setupShaders() {
    const vsSource = `
      attribute vec2 aPosition;
      void main() {
        gl_Position = vec4(aPosition, 0.0, 1.0);
      }
    `;

    // Enhanced fragment shader with better visual effects
    const fsSource = `
      precision mediump float;
      uniform vec2 uResolution;
      uniform float uTime;
      
      void main() {
        vec2 uv = (gl_FragCoord.xy - uResolution.xy * 0.5) / min(uResolution.x, uResolution.y);
        float dist = length(uv);
        vec3 color = vec3(0.0);
        float totalIntensity = 0.0;

        // Create multiple pulsing rings with different characteristics
        for (float i = 0.0; i < 5.0; i += 1.0) {
          float phase = uTime * (0.6 + i * 0.15) + i * 1.2566;
          float radius = 0.12 + (i * 0.07) + sin(phase) * 0.04;
          float thickness = 0.015 + abs(sin(phase * 1.3)) * 0.02;
          
          // Create smooth ring with better falloff
          float ring = 1.0 - smoothstep(0.0, thickness, abs(dist - radius));
          ring *= smoothstep(radius + thickness + 0.03, radius + thickness, dist);
          ring *= smoothstep(radius - thickness - 0.03, radius - thickness, dist);
          
          // Enhanced color cycling
          float hue = mod(uTime * 0.4 + i * 0.8, 6.28318);
          vec3 ringColor = 0.6 + 0.4 * cos(hue + vec3(0.0, 2.094, 4.188));
          
          float intensity = ring * (1.0 - i * 0.12) * (0.8 + 0.2 * sin(phase * 2.5));
          color += ringColor * intensity;
          totalIntensity += intensity;
        }

        // Add subtle center glow
        float centerGlow = 1.0 - smoothstep(0.0, 0.15 + 0.05 * sin(uTime * 1.8), dist);
        centerGlow *= 0.2 + 0.1 * sin(uTime * 2.5);
        color += vec3(0.9, 0.95, 1.0) * centerGlow;
        totalIntensity += centerGlow;

        if (totalIntensity > 0.01) {
          gl_FragColor = vec4(color, min(totalIntensity, 0.9));
        } else {
          discard;
        }
      }
    `;

    const vertexShader = compileShader(this.gl, vsSource, this.gl.VERTEX_SHADER);
    const fragmentShader = compileShader(this.gl, fsSource, this.gl.FRAGMENT_SHADER);

    if (!vertexShader || !fragmentShader) {
      webglError.value = 'Failed to compile shaders.';
      return false;
    }

    this.program = this.gl.createProgram();
    this.gl.attachShader(this.program, vertexShader);
    this.gl.attachShader(this.program, fragmentShader);
    this.gl.linkProgram(this.program);

    if (!this.gl.getProgramParameter(this.program, this.gl.LINK_STATUS)) {
      webglError.value = 'Failed to link shader program.';
      return false;
    }

    this.gl.useProgram(this.program);

    // Get uniform locations
    this.uniforms = {
      uResolution: this.gl.getUniformLocation(this.program, 'uResolution'),
      uTime: this.gl.getUniformLocation(this.program, 'uTime')
    };

    this.gl.uniform2f(this.uniforms.uResolution, this.canvas.width, this.canvas.height);

    // Enable blending for transparency
    this.gl.enable(this.gl.BLEND);
    this.gl.blendFunc(this.gl.SRC_ALPHA, this.gl.ONE_MINUS_SRC_ALPHA);

    // Clean up shaders
    this.gl.deleteShader(vertexShader);
    this.gl.deleteShader(fragmentShader);

    webglError.value = '';
    return true;
  }

  setupGeometry() {
    // Full-screen quad vertices
    const vertices = new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]);
    this.buffers.vertex = this.gl.createBuffer();
    this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.buffers.vertex);
    this.gl.bufferData(this.gl.ARRAY_BUFFER, vertices, this.gl.STATIC_DRAW);

    const aPosition = this.gl.getAttribLocation(this.program, 'aPosition');
    this.gl.vertexAttribPointer(aPosition, 2, this.gl.FLOAT, false, 0, 0);
    this.gl.enableVertexAttribArray(aPosition);

    return true;
  }

  render() {
    if (!this.gl || !this.program) return;

    const currentTime = (Date.now() - this.startTime) * 0.001;
    this.gl.uniform1f(this.uniforms.uTime, currentTime);

    // Clear with transparent background
    this.gl.clearColor(0.0, 0.0, 0.0, 0.0);
    this.gl.clear(this.gl.COLOR_BUFFER_BIT);

    // Draw the quad
    this.gl.drawArrays(this.gl.TRIANGLE_STRIP, 0, 4);
  }

  cleanup() {
    if (this.gl) {
      if (this.program) this.gl.deleteProgram(this.program);
      if (this.buffers.vertex) this.gl.deleteBuffer(this.buffers.vertex);
    }
  }
}

// Main App component using JSX
const App = () => {
  const canvasRef = createRef();
  const [webglManager, setWebglManager] = useState(null);

  // Initialize WebGL when component mounts
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const manager = new WebGLManager(canvas);
    if (manager.init()) {
      setWebglManager(manager);
    }

    return () => {
      if (manager) {
        manager.cleanup();
      }
    };
  }, []);

  // Animation loop effect
  effect(() => {
    if (!isAnimating.value || !webglManager) {
      if (animationFrameId.value) {
        cancelAnimationFrame(animationFrameId.value);
        animationFrameId.value = null;
      }
      return;
    }

    const animate = () => {
      if (!isAnimating.value) return;

      webglManager.render();
      animationFrameId.value = requestAnimationFrame(animate);
    };

    animate();

    // Cleanup function
    return () => {
      if (animationFrameId.value) {
        cancelAnimationFrame(animationFrameId.value);
        animationFrameId.value = null;
      }
    };
  });

  const startAnimation = () => {
    if (webglManager) {
      webglManager.startTime = Date.now(); // Reset start time
      isAnimating.value = true;
    }
  };

  const stopAnimation = () => {
    isAnimating.value = false;
  };

  return (
    <div class={styles.container}>
      <h1 class={styles.header}>WebGL Audio-Like Circle Animation</h1>
      <div class={styles.canvasContainer}>
        <canvas
          ref={canvasRef}
          class={styles.canvas}
        />
      </div>
      {webglError.value && <div class={styles.error}>{webglError.value}</div>}
      <div class={styles.controls}>
        <button
          class={`${styles.button} ${styles.startButton}`}
          onClick={startAnimation}
          disabled={!webglManager}
        >
          Start
        </button>
        <button
          class={`${styles.button} ${styles.stopButton}`}
          onClick={stopAnimation}
        >
          Stop
        </button>
      </div>
    </div>
  );
};

export default App;
