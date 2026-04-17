import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/home';

function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        {/* Futuramente: <Route path="/dashboard" element={<Dashboard />} /> */}
      </Routes>
    </BrowserRouter>
  );
}

export default AppRoutes;