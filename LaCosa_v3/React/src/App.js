import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './Home';
import CreateUser from './CreateUser';
import GamesHome from './GamesHome';
import GamesLobby from './GamesLobby';

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
          <Route path="/GamesHome/:playerId" element={<GamesHome />} />

          {/* Ruta para la página del lobby de un juego */}
          <Route path="/games/:game_name/join/:playerId" element={<GamesLobby />} />
        </Routes>
      </Router>
    </div>
  );
};

export default App;
