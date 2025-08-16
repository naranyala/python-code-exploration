import { h, render } from 'preact';
import { signal } from '@preact/signals';
import { setup, css } from 'goober';

setup(h);

// State
const isNavOpen = signal(false);

// Styles
const styles = {
  body: css`
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        margin: 0;
        padding: 0;
        background: #f4f4f9;
        color: #333;
      `,
  navbar: css`
        background: #2c3e50;
        color: white;
        padding: 1rem;
        position: fixed;
        width: 100%;
        top: 0;
        z-index: 1000;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      `,
  navContainer: css`
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
      `,
  navBrand: css`
        font-size: 1.5rem;
        font-weight: bold;
      `,
  navLinks: css`
        display: flex;
        gap: 1.5rem;
        @media (max-width: 600px) {
          display: ${isNavOpen.value ? 'flex' : 'none'};
          flex-direction: column;
          position: absolute;
          top: 60px;
          left: 0;
          right: 0;
          background: #2c3e50;
          padding: 1rem;
        }
      `,
  navLink: css`
        color: white;
        text-decoration: none;
        font-size: 1rem;
        &:hover { color: #3498db; }
      `,
  navToggle: css`
        display: none;
        background: none;
        border: none;
        color: white;
        font-size: 1.5rem;
        cursor: pointer;
        @media (max-width: 600px) {
          display: block;
        }
      `,
  main: css`
        margin-top: 80px;
        padding: 1rem;
      `,
  container: css`
        max-width: 1200px;
        margin: 0 auto;
      `,
  grid: css`
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        padding: 1rem;
      `,
  card: css`
        background: white;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
        cursor: pointer;
        transition: transform 0.2s, box-shadow 0.2s;
        &:hover {
          transform: translateY(-5px);
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
      `,
  cardTitle: css`
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
      `,
  cardDescription: css`
        font-size: 0.9rem;
        color: #666;
      `
};

// Sample menu items
const menuItems = [
  { id: 1, title: 'Dashboard', description: 'View key metrics and insights' },
  { id: 2, title: 'Tasks', description: 'Manage your tasks and projects' },
  { id: 3, title: 'Reports', description: 'Generate and view reports' },
  { id: 4, title: 'Settings', description: 'Customize your preferences' },
  { id: 5, title: 'Users', description: 'Manage user accounts' },
  { id: 6, title: 'Analytics', description: 'Track performance data' }
];

// Navbar Component
function Navbar() {
  return (
    <nav class={styles.navbar}>
      <div class={styles.navContainer}>
        <div class={styles.navBrand}>MyApp</div>
        <button
          class={styles.navToggle}
          onClick={() => (isNavOpen.value = !isNavOpen.value)}
        >
          ☰
        </button>
        <div class={styles.navLinks}>
          <a href="#home" class={styles.navLink}>Home</a>
          <a href="#about" class={styles.navLink}>About</a>
          <a href="#services" class={styles.navLink}>Services</a>
          <a href="#contact" class={styles.navLink}>Contact</a>
        </div>
      </div>
    </nav>
  );
}

// Grid Menu Component
function GridMenu() {
  return (
    <div class={styles.grid}>
      {menuItems.map(item => (
        <div
          key={item.id}
          class={styles.card}
          onClick={() => alert(`Clicked ${item.title}`)}
        >
          <h3 class={styles.cardTitle}>{item.title}</h3>
          <p class={styles.cardDescription}>{item.description}</p>
        </div>
      ))}
    </div>
  );
}

// Main App Component
export function App() {
  return (
    <div class={styles.body}>
      <Navbar />
      <main class={styles.main}>
        <div class={styles.container}>
          <h1>Dashboard Menu</h1>
          <GridMenu />
        </div>
      </main>
    </div>
  );
}

