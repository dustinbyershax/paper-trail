/**
 * Main application component with React Router setup
 * Defines routes for Politician Search, Donor Search, and Feedback pages
 */
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import PoliticianSearch from './pages/PoliticianSearch';
import DonorSearch from './pages/DonorSearch';
import Feedback from './pages/Feedback';
import './index.css';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <Header />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<PoliticianSearch />} />
            <Route path="/donor_search" element={<DonorSearch />} />
            <Route path="/feedback" element={<Feedback />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
