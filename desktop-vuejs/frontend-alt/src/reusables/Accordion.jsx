
import { h } from 'preact';
import { useState } from 'preact/hooks';
import { setup, css } from 'goober';



function AccordionItem({ title, children }) {
  const [open, setOpen] = useState(false);
  return (
    <div className={styles.item}>
      <div className={styles.header} onClick={() => setOpen(!open)}>
        {title}
      </div>
      {open && <div className={styles.content}>{children}</div>}
    </div>
  );
}

function Accordion() {
  return (
    <main className={styles.container}>
      <AccordionItem title="Section 1">
        This is the content of section 1. You can put anything here.
      </AccordionItem>
      <AccordionItem title="Section 2">
        Section 2 content. Maybe even nested components or forms.
      </AccordionItem>
      <AccordionItem title="Section 3">
        Section 3 is here. You can style it however you like.
      </AccordionItem>
    </main>
  );
}

export default Accordion


const styles = {
  container: css`
    max-width: 600px;
    margin: 40px auto;
    font-family: sans-serif;
  `,
  item: css`
    border: 1px solid #ccc;
    margin-bottom: 10px;
    border-radius: 4px;
    overflow: hidden;
  `,
  header: css`
    background: #f0f0f0;
    padding: 12px 16px;
    cursor: pointer;
    font-weight: bold;
    transition: background 0.3s;
    &:hover {
      background: #ddd;
    }
  `,
  content: css`
    padding: 16px;
    background: #fff;
    animation: fadeIn 0.3s ease-in-out;
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(-5px); }
      to { opacity: 1; transform: translateY(0); }
    }
  `
};
