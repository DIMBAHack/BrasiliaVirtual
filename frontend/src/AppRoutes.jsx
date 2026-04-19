import { Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import MyAnalysesPage from './pages/MyAnalysesPage';
import AnalysisPage from './pages/Analysis';
import AnalysisLoadingPage from './pages/AnalysisLoadingPage';

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/login" element={<HomePage />} />
      <Route path="/minhasanalises" element={<MyAnalysesPage />} />
      <Route path="/analisando" element={<AnalysisLoadingPage />} />
      <Route path="/analise/:id" element={<AnalysisPage />} />
    </Routes>
  );
}

export default AppRoutes;