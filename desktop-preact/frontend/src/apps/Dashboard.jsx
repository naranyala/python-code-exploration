import { h } from 'preact';
import { signal } from '@preact/signals';
import { setup, css } from 'goober';

setup(h);

const leftOpen = signal(true);
const rightOpen = signal(true);
const leftAccordionOpen = signal(null);
const rightAccordionOpen = signal(null);

function Accordion({ openSignal, items }) {
  return (
    <div>
      {items.map((item, i) => (
        <div class={styles.accordionItem} key={i}>
          <div
            class={styles.accordionHeader}
            onClick={() =>
              openSignal.value = openSignal.value === i ? null : i
            }
          >
            {item.title}
          </div>
          <div
            class={`${styles.accordionContent} ${openSignal.value === i ? styles.open : ''}`}
          >
            {openSignal.value === i && <div>{item.content}</div>}
          </div>
        </div>
      ))}
    </div>
  );
}

export function Dashboard() {
  return (
    <div class={styles.container}>
      <div class={`${styles.sidebar} ${leftOpen.value ? styles.sidebarOpen : ''}`}>
        <button
          class={styles.toggleButton}
          onClick={() => leftOpen.value = !leftOpen.value}
        >
          {leftOpen.value ? 'Close' : 'Open'} Left
        </button>
        <Accordion
          openSignal={leftAccordionOpen}
          items={[
            { title: 'Left Item 1', content: 'Content for left 1' },
            { title: 'Left Item 2', content: 'Content for left 2' },
            { title: 'Left Item 3', content: 'Content for left 3' },
          ]}
        />
      </div>

      <div class={styles.mainContent}>
        <h1>Dashboard Content</h1>
      </div>

      <div class={`${styles.sidebar} ${rightOpen.value ? styles.sidebarOpen : ''}`}>
        <button
          class={styles.toggleButton}
          onClick={() => rightOpen.value = !rightOpen.value}
        >
          {rightOpen.value ? 'Close' : 'Open'} Right
        </button>
        <Accordion
          openSignal={rightAccordionOpen}
          items={[
            { title: 'Right Item 1', content: 'Content for right 1' },
            { title: 'Right Item 2', content: 'Content for right 2' },
            { title: 'Right Item 3', content: 'Content for right 3' },
          ]}
        />
      </div>
    </div>
  );
}

const styles = {
  container: css`
    display: flex;
    height: 100vh;
    background: #f0f0f0;
    color: #333;
  `,
  sidebar: css`
    background: #2c3e50;
    color: white;
    width: 0;
    transition: width 0.3s ease;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  `,
  sidebarOpen: css`
    width: 250px;
  `,
  mainContent: css`
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
  `,
  toggleButton: css`
    background: #3498db;
    border: none;
    padding: 0.5rem 1rem;
    color: white;
    cursor: pointer;
    margin: 0.5rem;
    border-radius: 4px;
    &:hover {
      background: #2980b9;
    }
  `,
  accordionItem: css`
    border-top: 1px solid rgba(255, 255, 255, 0.2);
  `,
  accordionHeader: css`
    padding: 1rem;
    cursor: pointer;
    background: rgba(255, 255, 255, 0.1);
  `,
  accordionContent: css`
    padding: 0;
    height: 0;
    overflow: hidden;
    background: rgba(255, 255, 255, 0.05);
    transition: padding 0.3s ease, height 0.3s ease;
  `,
  open: css`
    padding: 1rem;
    height: auto;
  `
};

