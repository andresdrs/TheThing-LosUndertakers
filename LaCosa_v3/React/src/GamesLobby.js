import React, { useState, useEffect, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from './api';
import './GamesLobby.css';

const GamesLobby = () => {
  const { game_name, playerId } = useParams();
  const [playersList, setPlayersList] = useState([]);
  const navigate = useNavigate();

  // Función para tener listado de jugadores
  const fetchPlayersList = useCallback(async () => {
    try {
      const response = await api.get(`/games/${game_name}/players`);
      if (response && response.data) {
        setPlayersList(response.data);
      } else {
        console.error("Invalid response format");
      }
    } catch (error) {
      console.error("Error al obtener la lista de jugadores:", error);
    }
  }, [game_name]);

// Hook que hace que se actualice la lista de jugadores cada 2 segundos y que ingrese a todos
// los jugadores al juego si la partida está iniciada.
  useEffect(() => {
    const fetchData = async () => {
      await fetchPlayersList();
    };

    fetchData();

    const fetchPlayersInterval = setInterval(async () => {
      await fetchPlayersList();
    }, 2000);

    const checkGameStarted = async () => {
      try {
        const response = await api.get(`/games/${game_name}/status`);
        if (response && response.data && response.data.gameStarted) {
          navigate(`/games/${game_name}/play/${playerId}`);
          clearInterval(fetchPlayersInterval);
        }
      } catch (error) {
        console.error("Error al verificar el estado del juego:", error);
      }
    };

    const pollingInterval = setInterval(checkGameStarted, 2000);

    return () => {
      clearInterval(pollingInterval);
      clearInterval(fetchPlayersInterval);
    };

  }, [game_name, fetchPlayersList, navigate, playerId]);


  // Función que inicia un juego
  const handleStartGame = async () => {
    try {
      await api.post(`/games/${game_name}/start/${playerId}`); // manda petición de iniciar juego
    } catch (error) {
      alert('Necesitas ser el creador para iniciar la partida.');
    }
  };

 // código httml
  return (
    <div className="mainContainer-GamesLobby">
      <div className="gameInfoContainer">
        <label className="titleContainer-GamesLobby">Partida: {game_name}</label>
        <button onClick={handleStartGame}>Iniciar Partida</button>
      </div>
      <div className="listContainer-GamesLobby">
        <h2 className="titleContainer-GamesLobby">Lista de Jugadores:</h2>
        <div className="playersInfo">
          {playersList.map((player) => (
            <div key={player.user_id} className="playerInfo">
               {player.nickname}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default GamesLobby;
