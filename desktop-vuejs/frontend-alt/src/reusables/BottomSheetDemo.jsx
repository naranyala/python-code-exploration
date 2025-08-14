

import { h, render } from 'preact';

import { useState } from 'preact/hooks';
import { setup, css } from 'goober';



function BottomSheet({ children, onClose }) {
  return (
    <div className={styles.overlay} onClick={onClose}>
      <div className={styles.sheet} onClick={e => e.stopPropagation()}>
        {children}
      </div>
    </div>
  );
}

function BottomSheetDemo() {
  const [open, setOpen] = useState(false);

  return (
    <main>
      <button className={styles.button} onClick={() => setOpen(true)}>
        Open Bottom Sheet
      </button>

      {open && (
        <BottomSheet onClose={() => setOpen(false)}>
          <h2>Bottom Sheet</h2>
          <p>This is a sliding-up drawer. Tap outside to close.</p>
        </BottomSheet>
      )}
    </main>
  );
}

export default BottomSheetDemo


const styles = {
  overlay: css`
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.4);
    display: flex;
    justify-content: center;
    align-items: flex-end;
    z-index: 999;
  `,
  sheet: css`
    background: white;
    width: 100%;
    max-width: 600px;
    border-top-left-radius: 16px;
    border-top-right-radius: 16px;
    padding: 24px;
    box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.2);
    animation: slideUp 0.3s ease-out;

    @keyframes slideUp {
      from { transform: translateY(100%); }
      to { transform: translateY(0); }
    }
  `,
  button: css`
    padding: 12px 20px;
    background: #0077ff;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 16px;
    margin: 40px auto;
    display: block;
  `
};
