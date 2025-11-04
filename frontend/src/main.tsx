import { StrictMode, useEffect } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { ThemeProvider } from './components/providers/theme-provider'
import { applyChartJSTheme } from './lib/charting/chartjs-theme'

function Root() {
  useEffect(() => {
    applyChartJSTheme()
  }, [])

  return (
    <ThemeProvider defaultTheme="dark">
      <App />
    </ThemeProvider>
  )
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Root />
  </StrictMode>,
)
