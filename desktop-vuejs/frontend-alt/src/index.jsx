
import { h, render } from 'preact';

import { setup } from "goober"

import App from "./App"

setup(h);

render(<App />, document.getElementById('app'));
