/**
 * Site-wide navigation header
 * Displays app branding, navigation links, and disclaimer
 */
import { NavLink } from 'react-router-dom';

export default function Header() {
  return (
    <header className="bg-blue-600 text-white shadow-md">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold">Paper Trail</h1>
          <nav className="flex gap-6">
            <NavLink
              to="/"
              className={({ isActive }) =>
                isActive
                  ? 'font-bold underline underline-offset-4'
                  : 'hover:underline underline-offset-4'
              }
            >
              Politician Search
            </NavLink>
            <NavLink
              to="/donor_search"
              className={({ isActive }) =>
                isActive
                  ? 'font-bold underline underline-offset-4'
                  : 'hover:underline underline-offset-4'
              }
            >
              Donor Search
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
        </div>
      </div>
      <div className="bg-blue-500 px-4 py-2">
        <p className="text-sm text-center">
          Disclaimer: This data is for informational purposes only.
          Data accuracy is not guaranteed. Please verify all information
          with official sources.
        </p>
      </div>
    </header>
  );
}
