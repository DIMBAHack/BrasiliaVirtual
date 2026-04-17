// src/pages/Home.jsx
import { useState } from 'react';
import reactLogo from '../assets/react.svg'; // Note o ../ para subir uma pasta
import viteLogo from '../assets/vite.svg';

function Home() {
  const [count, setCount] = useState(0);

  return (
    <section id="center">
      <h1>Brasília Virtual</h1>
      <div className="hero">
        <img src={viteLogo} className="vite" alt="Vite logo" />
      </div>
      
      <div className="card">
        <p>O front-end em React está pronto para conectar com o Python.</p>
        <button onClick={() => setCount((count) => count + 1)}>
          Testando Estado: {count}
        </button>
      </div>

      <p className="read-the-docs">
        Edite <code>src/pages/Home.jsx</code> para começar a criar sua interface.
      </p>
    </section>
  );
}

export default Home;