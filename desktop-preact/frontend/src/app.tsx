import './app.css'

import Navbar from "./shared/Navbar.jsx"
import Button from "./shared/Button.jsx"
import BottomSheet from "./shared/BottomSheet.jsx"

import { css } from 'goober'
import { signal, effect, computed } from '@preact/signals'

export function App() {

  const count = signal(0)
  const doubled = computed(() => count.value * 2)

  effect(() => {
    console.log("count: ", count.value)
    console.log("doubled: ", doubled.value)
  })

  return (
    <div className={styles.container}>
      <Navbar />

      <button onClick={() => count.value++}>{count} - {doubled}</button>

      <Button />

      <BottomSheet />
    </div>
  )
}

const styles = {
  container: css`
    display: grid;
    align-item: center;
    padding: 20px;
    border: 1px solid gray;
    margin: 0 auto;
  `
}
