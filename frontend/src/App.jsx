import AppRoutes from './AppRoutes';
import './App.css';

function App() {
  return (
    <div className="app-container">
      {/* O AppRoutes decide qual "página" exibir com base na URL */}
      <AppRoutes />
    </div>
  );
}

export default App;