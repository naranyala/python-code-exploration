
import { h, Fragment } from 'preact';

import { css } from "goober"

const Button = (props) => {
  return (
    <button className={styles.btn}>
      {props?.label ?? (
        <>
          <b>ctrl+shift+i</b> {"to open devtools"}
        </>
      )}
    </button>
  )
}

export default Button

const styles = {
  btn: css`
        background: white;
        border-radius: 20px;
        padding: 20px;

        &:hover { background: lightgray; }
    `
}

