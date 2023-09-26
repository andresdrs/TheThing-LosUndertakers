import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './Home';
import CreateUser from './CreateUser';
import JoinGame from './JoinGame';

// app general con la definición de las rutas
const App = () => {
  return (
    <div className="App">
      <Router>
        <Routes>
          {/* Ruta para la página de inicio (predeterminada)*/}
          <Route exact path="/" element={<Home />} /> 

          {/* Ruta para la página de creación de usuario */}
          <Route path="/CreateUser" element={<CreateUser />} />

          {/* Ruta para la página de unirse a un juego */}
          <Route path="/joingame" element={<JoinGame />} />
        </Routes>
      </Router>
    </div>
  );
};

export default App;
