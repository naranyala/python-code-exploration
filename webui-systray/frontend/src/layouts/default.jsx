
export default function Layout(props) {
  return (
    <div>
      <nav>sidebar</nav>
      {props?.children}
    </div>
  )
}
