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
      {items.map((item, i) => {
        const isOpen = openSignal.value === i;
        return (
          <div class={styles.accordionItem} key={i}>
            <div
              class={styles.accordionHeader}
              onClick={() =>
                openSignal.value = isOpen ? null : i
              }
            >
              {item.title}
            </div>
            <div
              class={`${styles.accordionContent} ${isOpen ? styles.open : ''}`}
            >
              {isOpen && (
                <div class={styles.accordionInner}>
                  {typeof item.content === 'function'
                    ? h(item.content)
                    : item.content}
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}

function SampleWidget() {
  return (
    <div>
      <p>This is a sample widget inside the accordion.</p>
      <button>Click Me</button>
    </div>
  );
}

export function Sample2() {
  return (
    <div class={styles.container}>
      {/* New fixed top navbar */}
      <div class={styles.navbar}>
        <button
          class={styles.toggleButton}
          onClick={() => leftOpen.value = !leftOpen.value}
        >
          {leftOpen.value ? 'Close Left' : 'Open Left'}
        </button>
        <h1 class={styles.title}>Dashboard</h1>
        <button
          class={styles.toggleButton}
          onClick={() => rightOpen.value = !rightOpen.value}
        >
          {rightOpen.value ? 'Close Right' : 'Open Right'}
        </button>
      </div>

      <div class={styles.contentWrapper}>
        <div class={`${styles.sidebar} ${leftOpen.value ? styles.sidebarOpen : ''}`}>
          <Accordion
            openSignal={leftAccordionOpen}
            items={[
              { title: 'Left Item 1', content: 'Simple text content' },
              { title: 'Left Item 2', content: <SampleWidget /> },
              { title: 'Left Item 3', content: () => <div>Dynamic from function</div> },
            ]}
          />
        </div>

        <div class={styles.mainContent}>
          <p>Main content goes here</p>
        </div>

        <div class={`${styles.sidebar} ${rightOpen.value ? styles.sidebarOpen : ''}`}>
          <Accordion
            openSignal={rightAccordionOpen}
            items={[
              { title: 'Right Item 1', content: 'Another text block' },
              { title: 'Right Item 2', content: <div><b>Bold Content</b> inside accordion</div> },
              { title: 'Right Item 3', content: SampleWidget },
            ]}
          />
        </div>
      </div>
    </div>
  );
}

export default Sample2;

const styles = {
  container: css`
    display: flex;
    flex-direction: column;
    height: 100vh;
    background: #f0f0f0;
    color: #333;
  `,
  navbar: css`
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background: #2c3e50;
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 1rem;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    z-index: 100;
  `,
  title: css`
    margin: 0;
    font-size: 1.2rem;
  `,
  contentWrapper: css`
    display: flex;
    flex: 1;
    margin-top: 50px; /* Account for fixed navbar */
    height: calc(100vh - 50px);
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
    padding: 1rem;
    overflow-y: auto;
  `,
  toggleButton: css`
    background: #3498db;
    border: none;
    padding: 0.5rem 1rem;
    color: white;
    cursor: pointer;
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
  accordionInner: css`
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  `,
  open: css`
    padding: 1rem;
    height: auto;
  `
};
