import React from "react"
import { useNavigate } from "react-router-dom";
import './Home.css';

const Home = (props) => {
    const navigate = useNavigate();
    
    const onButtonClick = () => {
        navigate('/CreateUser');
    }

    return (
        <div className="mainContainer">
            <div className="titleContainer">
                <div>Bienvenido a La Cosa!</div>
            </div>
            <div className="buttonContainer">
                    <input
                        className="inputButton"
                        type="button"
                        onClick={onButtonClick}
                        value="Entrar" />
            </div>

        </div>
    )
}

export default Home