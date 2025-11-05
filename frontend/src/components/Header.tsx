/**
 * Site-wide navigation header
 * Displays app branding, navigation links, and disclaimer
 */
import { NavLink } from 'react-router-dom';
import { ThemeToggle } from './ThemeToggle';

export default function Header() {
  return (
    <header className="bg-gradient-to-r from-blue-900 to-blue-950 dark:from-gray-900 dark:to-gray-800 text-white shadow-lg transition-colors">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <img
              src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/The_Young_Turks_logo.svg/200px-The_Young_Turks_logo.svg.png"
              alt="TYT Logo"
              className="h-10 w-10"
              onError={(e) => {
                e.currentTarget.style.display = 'none';
              }}
            />
            <div>
              <h1 className="text-2xl font-bold">Paper Trail</h1>
              <p className="text-xs text-blue-100 dark:text-gray-400">by The People</p>
            </div>
          </div>
          <div className="flex items-center gap-6">
            <nav className="flex gap-6">
              <NavLink
                to="/politician"
                className={({ isActive }) =>
                  isActive
                    ? 'font-bold underline underline-offset-4'
                    : 'hover:underline underline-offset-4'
                }
              >
                Politicians
              </NavLink>
              <NavLink
                to="/donor"
                className={({ isActive }) =>
                  isActive
                    ? 'font-bold underline underline-offset-4'
                    : 'hover:underline underline-offset-4'
                }
              >
                Donors
              </NavLink>
              <NavLink
                to="/feedback"
                className={({ isActive }) =>
                  isActive
                    ? 'font-bold underline underline-offset-4'
                    : 'hover:underline underline-offset-4'
                }
              >
                Feedback
              </NavLink>
            </nav>
            <button
              onClick={() => {
                const event = new KeyboardEvent('keydown', {
                  key: 'k',
                  metaKey: true,
                  bubbles: true,
                });
                document.dispatchEvent(event);
              }}
              className="hidden sm:flex items-center gap-2 px-3 py-1.5 text-xs rounded-md border border-white/20 hover:bg-white/10 transition-colors"
              title="Search (Cmd+K or Ctrl+K)"
            >
              <span>Search</span>
              <kbd className="px-1.5 py-0.5 text-[10px] font-mono bg-white/20 rounded">⌘K</kbd>
            </button>
            <ThemeToggle />
          </div>
        </div>
      </div>
      <div className="bg-yellow-900/50 dark:bg-yellow-900/50 border-t border-yellow-700 dark:border-yellow-700 px-4 py-2 transition-colors">
        <p className="text-sm text-center text-yellow-300 dark:text-yellow-300">
          Disclaimer: This data is for informational purposes only.
          Data accuracy is not guaranteed. Please verify all information
          with official sources.
        </p>
      </div>
    </header>
  );
}
