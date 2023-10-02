import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import api from './api'
import './CreateUser.css';

const CreateUser = () => {
  const [nickname, setNickname] = useState(''); // variable que va cambiando de estado a medida que vayan ingresando nombres.
                                                // se usa el hook useState que es una construcción de React para tener una variable que sea:
                                                // valor, función que lo actualiza (todo en uno)

  const navigate = useNavigate(); // función que llamamos para cambiar de ruta


  
  // función de manejo de evento
  // se ejecuta cuando el usuario ingresa nombre en el campo de texto
  const handleNicknameChange = (event) => {
    setNickname(event.target.value); // se accede al valor del formulario 
    // event es un objeto con información que se genera al llamar a la función. 
    // Acá, event sería la información que tiene el formulario, o sea, type, classname, id, value, onChange.
    // si queremos acceder a alguno de estos campos, se usa .target y luego se especifica el campo, .value
    
  };

  // función de manejo de evento
  // se ejecuta cuando se envía el form
  const handleSubmit = async (event) => {
    event.preventDefault(); // esto evita que la página se recargue cuando se envíe el formulario
    try {
      const response = await api.post('/users/', { nickname });
      alert('Usuario creado exitosamente');
      setNickname(''); // Limpiar el valor del campo de usuario para que no quede el nickname
      navigate(`/GamesHome/${response.data.user_id}`); // Navegar a JoinGame usando directamente el ID del jugador creado
      
    } catch (error) {
      alert('Error al crear usuario. Ingrese un nombre distinto.');
    }
    
  };

  return (
    <div className="mainContainer-CreateUser">
      <form onSubmit={handleSubmit}>
      <div className="titleContainer-CreateUser">
        <div>Ingrese un nombre</div>
      </div>
      <div className='mb-3 mt-3'>
        <label htmlFor='nickname' className='form-label'>
          <input
            type="text" // campo de texto, aqui usuario pone su nombre de jugador
            className="form-control-CreateUser"
            id="nickname"
            value={nickname}
            onChange={handleNicknameChange}
          />
        </label>
      </div>
      <button className="inputButton-CreateUser" type="submit">Crear</button>
      </form>
    </div>

  );
};

export default CreateUser;
