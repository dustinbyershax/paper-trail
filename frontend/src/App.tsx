/**
 * Main application component with React Router setup
 * Defines routes for Politician Search, Donor Search, and Feedback pages
 */
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import PoliticianSearch from './pages/PoliticianSearch';
import DonorSearch from './pages/DonorSearch';
import Feedback from './pages/Feedback';
import { CommandPalette } from './components/CommandPalette';
import './index.css';

function AppContent() {
  return (
    <>
      <CommandPalette />
      <div className="min-h-screen bg-background text-foreground">
        <Header />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            {/* Politician routes - all render PoliticianSearch component */}
            <Route path="/" element={<PoliticianSearch />} />
            <Route path="/politician" element={<PoliticianSearch />} />
            <Route path="/politician/:id" element={<PoliticianSearch />} />
            <Route path="/politician/compare" element={<PoliticianSearch />} />

            {/* Donor routes - all render DonorSearch component */}
            <Route path="/donor" element={<DonorSearch />} />
            <Route path="/donor/:id" element={<DonorSearch />} />

            {/* Other routes */}
            <Route path="/feedback" element={<Feedback />} />
          </Routes>
        </main>
      </div>
    </>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  );
}

export default App;
