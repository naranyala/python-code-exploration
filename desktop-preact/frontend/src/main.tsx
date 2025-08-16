import { render } from 'preact'

import './index.css'
import './css-reset.css'

import { App } from './app.tsx'
render(<App />, document.getElementById('app')!)

// import { Dashboard } from './apps/Dashboard.jsx'
// render(<Dashboard />, document.getElementById('app')!)

// import { Dashboard2 } from './apps/Dashboard2.jsx'
// render(<Dashboard2 />, document.getElementById('app')!)

// import LegalHavefunV0 from './apps/LegalHavefunV0.jsx'
// render(<LegalHavefunV0 />, document.getElementById('app')!)

import LegalHavefunV1 from './apps/LegalHavefunV1.jsx'
render(<LegalHavefunV1 />, document.getElementById('app')!)

// import LegalHavefunV2 from './apps/LegalHavefunV2.jsx'
// render(<LegalHavefunV2 />, document.getElementById('app')!)


// import BudalMantepOpportunity from './apps/BudalMantepOpportunity.jsx'
// render(<BudalMantepOpportunity />, document.getElementById('app')!)

// import BudalMantepFiles from './apps/BudalMantepFiles.jsx'
// render(<BudalMantepFiles />, document.getElementById('app')!)
