import { useState, useContext } from "react";
import { AlertContext } from "../Context"; 
import cancelImage from "./../image/AdmissedCancel.svg";
import "./BetterAlert.css";


function BetterAlert() {

    
    const { alert, setAlert } = useContext(AlertContext);

    function onClose() {
        console.log(alert);
        setAlert([]); 
    }

    if(alert.length == 0){
        return <></>
    }else{
        return (
            <>
                <div className={alert[1] === "Error" ? "alertBox errorAlert" : "alertBox loadingAlert"}>
                    <img className="cancelButton" onClick={onClose} src={cancelImage}></img>
                    <h4>{alert[0]}</h4>
                </div>
            </>
        )
    }
        
};

export default BetterAlert;