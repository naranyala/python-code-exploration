
import { h } from "preact";
import { signal } from "@preact/signals";
import { css } from "goober";

const isOpen = signal(false); // toggle signal

const Navbar = () => {
  return (
    <nav className={styles.navbar}>
      <div className={styles.brand}>MyApp</div>
      <button
        className={styles.toggleBtn}
        onClick={() => (isOpen.value = !isOpen.value)}
        aria-label="Toggle menu"
      >
        ☰
      </button>
      <div className={`${styles.menu} ${!isOpen.value ? styles.hidden : ""}`}>
        <button>Home</button>
        <button>About</button>
        <button>Contact</button>
      </div>
    </nav>
  );
};

export default Navbar

const styles = {
  navbar: css`
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    background: #fafafa;
    flex-wrap: wrap;
  `,
  brand: css`
    font-weight: bold;
    font-size: 1.2rem;
  `,
  toggleBtn: css`
    display: none;
    font-size: 1.5rem;
    cursor: pointer;
    background: none;
    border: none;

    @media (max-width: 600px) {
      display: block;
    }
  `,
  menu: css`
    display: flex;
    gap: 15px;

    @media (max-width: 600px) {
      flex-direction: column;
      width: 100%;
    }

    button {
      padding: 10px 15px;
      border-radius: 12px;
      border: none;
      background: white;
      cursor: pointer;

      &:hover {
        background: lightgray;
      }
    }
  `,
  hidden: css`
    display: none;
  `
};

