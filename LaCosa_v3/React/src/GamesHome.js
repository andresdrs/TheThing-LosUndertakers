import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from './api'
import './GamesHome.css';

const GamesHome = () => {
  const { playerId } = useParams();
  const [gameName, setGameName] = useState("");
  const [minPlayers, setMinPlayers] = useState(2);
  const [maxPlayers, setMaxPlayers] = useState(4);
  const [gamesList, setGamesList] = useState([]);
  const navigate = useNavigate();

  const handleCreateGame = async () => {
    try {
      const gameData = {
        game_name: gameName,
        min_players: minPlayers,
        max_players: maxPlayers,
        id_creator: playerId  // Include playerId in the request body
      };

      const response = await api.post(`/games/`, gameData);

      const nameGame = response.data.game_name;

      alert('Partida creada exitosamente');
      fetchGamesList();
      joinGame(nameGame, playerId);
    } catch (error) {
      alert('Error al crear la partida. Intente nuevamente.');
    }
  };

  const joinGame = async (nameGame, playerId) => {
    console.log('Joining game with ID:', playerId);
  
    try {
      await api.post(`/games/${nameGame}/join/${playerId}`);
      navigate(`/games/${nameGame}/join/${playerId}`);
      alert('Te has unido a la partida.');
    } catch (error) {
      alert('Error al unirse a la partida. Intente nuevamente.');
    }
  };
  

  const fetchGamesList = async () => {
    try {
      const response = await api.get("/games_list/");
      setGamesList(response.data);
    } catch (error) {
      console.error("Error al obtener la lista de partidas:", error);
    }
  };

  useEffect(() => {
    fetchGamesList();
  }, []);

  return (
    <div>
      <div className="mainContainer-GamesHome">
      <label className="titleContainer-GamesHome">Crear partida</label>
      <div>
        <label htmlFor="gameName">Nombre de la Partida:</label>
        <input
          type="text"
          id="gameName"
          value={gameName}
          onChange={(e) => setGameName(e.target.value)}
        />
      </div>
      <div>
        <label htmlFor="minPlayers">Cantidad Mínima de Jugadores:</label>
        <input
          type="number"
          id="minPlayers"
          value={minPlayers}
          onChange={(e) => setMinPlayers(parseInt(e.target.value, 10))}
        />
      </div>
      <div>
        <label htmlFor="maxPlayers">Cantidad Máxima de Jugadores:</label>
        <input
          type="number"
          id="maxPlayers"
          value={maxPlayers}
          onChange={(e) => setMaxPlayers(parseInt(e.target.value, 10))}
        />
      </div>
      <button onClick={handleCreateGame}>Crear Partida</button>
      </div>
      <div className="listContainer-GamesHome">
        <h2 className="titleContainer-GamesHome">Lista de Partidas:</h2>
        <ul>
        {gamesList.map((game) => (
          <li key={game.game_name}>
            <div className="gameInfo">
              <strong>Nombre de la Partida:</strong> {game.game_name}
            </div>
            <div className="joinButtonContainer">
              <button onClick={() => joinGame(game.game_name, playerId)}>Unirse</button>
            </div>
          </li>
        ))}
        </ul>
      </div>
    </div>
  );
};

export default GamesHome;
