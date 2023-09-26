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
      await api.post('/users/', { nickname });
      alert('Usuario creado exitosamente');
      setNickname(''); // aca se limpia el valor del campo de usuario para que no quede el nickname
    } catch (error) {
      console.error('Error al crear usuario:', error);
    }
    navigate('/JoinGame'); // una vez creado, navegar a JoinGame
  };

  return (
    <div className="mainContainer">
      <form onSubmit={handleSubmit}>
      <div className="titleContainer">
        <div>Ingrese un nombre</div>
      </div>
      <div className='mb-3 mt-3'>
        <label htmlFor='nickname' className='form-label'>
          <input
            type="text" // campo de texto, aqui usuario pone su nombre de jugador
            className="form-control"
            id="nickname"
            value={nickname}
            onChange={handleNicknameChange}
          />
        </label>
      </div>
      <button className="inputButton" type="submit">Crear</button>
      </form>
    </div>

  );
};

export default CreateUser;
