import { useState } from "react";
import "./Searchbar.css";


function renderSpreadSheetUpload(message, messageHandler) {
    return (
        <>
            <input type="input" placeholder="Spreadsheet Link" className="search" value={message} onChange={messageHandler}></input>
        </>
    );
}

function renderSelfUpload() {
    return (
        <>
            <h1>HI</h1>
        </>
    );
}


function Searchbar() {
    const [state, setState] = useState('typing');
    const [mode, setMode] = useState('spreadsheet');
    const [message, setMessage] = useState('');

    function messageHandler(e) {
        setMessage(e.target.value);
    }

    function modeHandler(e) {
        setMode(e.target.value);
    }

    return (
        <form>
            <select className="modeselect" value={mode} onChange={modeHandler}>
                <option value="spreadsheet">Spreadsheet Upload</option>
                <option value="upload">Self Upload</option>
            </select>
            {mode == 'spreadsheet' ? renderSpreadSheetUpload(message, messageHandler) : renderSelfUpload()}
            <button className="submit">Submit</button>
        </form>
    );
        
};

export default Searchbar;