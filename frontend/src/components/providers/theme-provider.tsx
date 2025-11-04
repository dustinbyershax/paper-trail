import * as React from "react"

type Theme = "light" | "dark"
type Ctx = { theme: Theme; setTheme: (t: Theme) => void }
const ThemeCtx = React.createContext<Ctx | null>(null)

export function ThemeProvider({ defaultTheme = "dark", children }:{
  defaultTheme?: Theme; children: React.ReactNode
}) {
  const [theme, setTheme] = React.useState<Theme>(() => {
    const saved = localStorage.getItem("theme") as Theme | null
    return saved ?? defaultTheme
  })
  React.useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme)
    localStorage.setItem("theme", theme)
  }, [theme])
  return <ThemeCtx.Provider value={{ theme, setTheme }}>{children}</ThemeCtx.Provider>
}

export function useTheme() {
  const ctx = React.useContext(ThemeCtx)
  if (!ctx) throw new Error("useTheme must be used within ThemeProvider")
  return ctx
}
