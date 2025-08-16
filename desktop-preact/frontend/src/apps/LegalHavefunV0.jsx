import { h } from 'preact';
import { signal } from '@preact/signals';
import { setup, css } from 'goober';
import { useRef, useEffect, useState } from 'preact/hooks';

setup(h);

// Lyrics data with timings (in seconds)
const lyricsData = [
  { text: "I see the future", time: 0, duration: 3 },
  { text: "But I don't see you there", time: 3, duration: 4 },
  { text: "All of my memories", time: 7, duration: 3 },
  { text: "Are painted in the air", time: 10, duration: 4 },
  { text: "I hear the echoes", time: 14, duration: 3 },
  { text: "Of voices I once knew", time: 17, duration: 4 },
  { text: "But they're just shadows now", time: 21, duration: 4 },
  { text: "Fading from view", time: 25, duration: 3 }
];

export function LyricsPlayer() {
  const canvasRef = useRef(null);
  const animationRef = useRef(null);
  const [currentTime, setCurrentTime] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [scrollPosition, setScrollPosition] = useState(0);
  const [canvasSize, setCanvasSize] = useState({ width: 800, height: 400 });
  const scrollSpeed = 0.2;
  const lineHeight = 80;

  // Get current line index
  const getCurrentLineIndex = () => {
    for (let i = 0; i < lyricsData.length; i++) {
      if (currentTime >= lyricsData[i].time &&
        currentTime < lyricsData[i].time + lyricsData[i].duration) {
        return i;
      }
    }
    return -1;
  };

  // Initialize canvas and resize handler
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const handleResize = () => {
      const width = Math.min(800, window.innerWidth - 40);
      setCanvasSize({ width, height: 400 });
      canvas.width = width;
      canvas.height = 400;
      renderLyrics();
    };

    handleResize();
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationRef.current);
    };
  }, []);

  // Animation loop
  useEffect(() => {
    if (!isPlaying) {
      cancelAnimationFrame(animationRef.current);
      return;
    }

    let lastTimestamp = performance.now();

    const animate = (timestamp) => {
      const deltaTime = (timestamp - lastTimestamp) / 1000;
      lastTimestamp = timestamp;

      setCurrentTime(prev => {
        const newTime = prev + deltaTime;

        // Auto-scroll logic
        const currentIndex = lyricsData.findIndex(line =>
          newTime >= line.time && newTime < line.time + line.duration
        );

        if (currentIndex >= 0) {
          const targetScroll = currentIndex * lineHeight - canvasSize.height / 3;
          setScrollPosition(prevScroll =>
            prevScroll + (targetScroll - prevScroll) * scrollSpeed
          );
        }

        return newTime;
      });

      renderLyrics();
      animationRef.current = requestAnimationFrame(animate);
    };

    animationRef.current = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(animationRef.current);
  }, [isPlaying, canvasSize.height]);

  // Render lyrics to canvas
  const renderLyrics = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const { width, height } = canvasSize;
    const currentIndex = getCurrentLineIndex();

    // Clear canvas
    ctx.fillStyle = '#121212';
    ctx.fillRect(0, 0, width, height);

    // Draw each line
    lyricsData.forEach((line, i) => {
      const yPos = i * lineHeight - scrollPosition;

      // Skip if not visible
      if (yPos < -lineHeight || yPos > height + lineHeight) return;

      const isCurrent = i === currentIndex;
      const isPast = i < currentIndex;
      const lineProgress = isCurrent
        ? Math.min(1, (currentTime - line.time) / line.duration)
        : 0;

      // Calculate visual properties
      let opacity = 1;
      let scale = 1;

      if (isCurrent) {
        opacity = lineProgress; // Fade in
        scale = 0.9 + (0.1 * lineProgress);
      } else if (isPast) {
        opacity = 0.6;
        scale = 0.9;
      } else {
        opacity = 0.8;
        scale = 0.95;
      }

      ctx.save();
      ctx.translate(width / 2, yPos);
      ctx.scale(scale, scale);

      // Text styling
      ctx.font = `bold ${isCurrent ? 32 : 26}px 'Arial', sans-serif`;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillStyle = isCurrent
        ? `rgba(255, 215, 0, ${opacity})`
        : `rgba(240, 240, 255, ${opacity * 0.8})`;

      // Text shadow
      ctx.shadowColor = 'rgba(0, 0, 0, 0.5)';
      ctx.shadowBlur = 5;
      ctx.shadowOffsetX = 0;
      ctx.shadowOffsetY = 2;

      ctx.fillText(line.text, 0, 0);
      ctx.restore();
    });
  };

  const handleSeek = (time) => {
    setCurrentTime(time);
    if (!isPlaying) {
      renderLyrics();
    }
  };

  return (
    <div class={styles.container}>
      <h2 class={styles.title}>Smooth Lyrics Player</h2>

      <div class={styles.canvasContainer}>
        <canvas
          ref={canvasRef}
          class={styles.canvas}
          width={canvasSize.width}
          height={canvasSize.height}
        />
      </div>

      <div class={styles.controls}>
        <button
          class={styles.controlButton}
          onClick={() => setIsPlaying(!isPlaying)}
        >
          {isPlaying ? '⏸ Pause' : '▶ Play'}
        </button>

        <input
          type="range"
          class={styles.timeSlider}
          min="0"
          max={lyricsData[lyricsData.length - 1].time + lyricsData[lyricsData.length - 1].duration}
          step="0.1"
          value={currentTime}
          onInput={(e) => handleSeek(parseFloat(e.target.value))}
        />

        <span class={styles.timeDisplay}>
          {Math.floor(currentTime)}.{Math.floor((currentTime % 1) * 10)}s
        </span>
      </div>
    </div>
  );
}

const styles = {
  container: css`
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    background: #1a1a1a;
    color: white;
    min-height: 100vh;
    font-family: 'Arial', sans-serif;
  `,
  title: css`
    color: #ffdd60;
    margin-bottom: 20px;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
  `,
  canvasContainer: css`
    margin: 20px 0;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
  `,
  canvas: css`
    display: block;
    background: #121212;
  `,
  controls: css`
    display: flex;
    align-items: center;
    gap: 15px;
    margin-top: 20px;
    width: 100%;
    max-width: 800px;
  `,
  controlButton: css`
    background: #ff5500;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: bold;
    transition: all 0.2s;
    
    &:hover {
      background: #ff7700;
    }
  `,
  timeSlider: css`
    flex: 1;
    height: 6px;
    border-radius: 3px;
    background: #444;
    outline: none;
    -webkit-appearance: none;
    
    &::-webkit-slider-thumb {
      -webkit-appearance: none;
      width: 18px;
      height: 18px;
      border-radius: 50%;
      background: #ffdd60;
      cursor: pointer;
    }
  `,
  timeDisplay: css`
    min-width: 60px;
    text-align: center;
    font-family: monospace;
  `
};

export default LyricsPlayer;
