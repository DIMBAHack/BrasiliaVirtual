import { Routes, Route } from 'react-router-dom'; // Remova o BrowserRouter daqui
import Login from './pages/home';
import AnalysisPage from './pages/Analysis';
import HomePageContent from './pages/HomePageContent'; // Página inicial
import MyAnalysesPage from './pages/MyAnalysesPage';

function AppRoutes() {
  return (
    // Deixe apenas o Routes e as Route
    <Routes>
      <Route path="/" element={<HomePageContent />} />
      <Route path="/login" element={<Login />} />
      <Route path="/minhasanalises" element={<MyAnalysesPage />} />
      <Route path="/analise" element={<AnalysisPage />} />
      {/* Adicione outras aqui */}
    </Routes>
  );
}

export default AppRoutes;