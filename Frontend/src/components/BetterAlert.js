import { useState, useContext } from "react";
import { AlertContext } from "../Context"; 
import cancelImage from "./../image/AdmissedCancel.svg";
import "./BetterAlert.css";


function BetterAlert() {

    
    const { alert, setAlert } = useContext(AlertContext);

    function onClose() {
        setAlert("");
    }

    if(alert === ""){
        return <></>
    }else{
        return (
            <>
                <div className="alertBox">
                    <img className="cancelButton" onClick={onClose} src={cancelImage}></img>
                    <h4>{alert}</h4>
                </div>
            </>
        )
    }
        
};

export default BetterAlert;