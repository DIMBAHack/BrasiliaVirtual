import { Routes, Route } from 'react-router-dom'; // Remova o BrowserRouter daqui
import Home from './pages/home';
import AnalysisPage from './pages/Analysis';
import HomePageContent from './pages/HomePageContent'; // Importe o novo componente
import MyAnalysesPage from './pages/MyAnalysesPage';

function AppRoutes() {
  return (
    // Deixe apenas o Routes e as Route
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/home" element={<HomePageContent />} />
      <Route path="/minhasanalises" element={<MyAnalysesPage />} />
      <Route path="/analise" element={<AnalysisPage />} />
      {/* Adicione outras aqui */}
    </Routes>
  );
}

export default AppRoutes;