import { useState, useContext } from "react";
import { useNavigate} from "react-router-dom";
import { DataContext, AlertContext } from "../Context"; 
import "./Uploadbar.css";


// TODO: single submit


function renderSpreadSheetUpload(fileName, uploadHandler) {
    return (
        <>
            <label htmlFor="file-upload" className="uploadFile">{fileName===""?"Upload File":fileName}</label>
            <input id="file-upload" type="file" onChange={uploadHandler} hidden></input>
        </>
    );
}

/*
function changeOneElement(arr, ind, v){
    let nw = arr;
    nw[ind] = v;
    return nw;
}

function renderSingleUpload(singleUpload, setSingleUpload) {
    // can i just write this with map instead
    return (
        <>
            <p>Year:</p>
            <input type="text" onChange={(v) => setSingleUpload(changeOneElement(singleUpload, 0, v.target.value))}></input>
            <div></div>
            <p>Status:</p>
            <select onChange={(v) => setSingleUpload(changeOneElement(singleUpload, 1, v.target.value))}>
                <option value="Accepted">Accepted</option>
                <option value="Rejected">Rejected</option>
                <option value="Deferred">Deferred</option>
            </select>
            <div></div>
            <p>School:</p>
            <input type="text" onChange={(v) => setSingleUpload(changeOneElement(singleUpload, 2, v.target.value))}></input>
            <div></div>
            <p>Program:</p>
            <input type="text" onChange={(v) => setSingleUpload(changeOneElement(singleUpload, 3, v.target.value))}></input>
            <div></div>
            <p>Average:</p>
            <input type="text" onChange={(v) => setSingleUpload(changeOneElement(singleUpload, 4, v.target.value))}></input>
            <div></div>
            <p>Decision Date:</p>
            <input type="date" onChange={(v) => setSingleUpload(changeOneElement(singleUpload, 5, v.target.value))}></input>
            <div></div>
        </>
    )
}*/

function Uploadbar() {

    const navigate = useNavigate();
    //const [state, setState] = useState("Upload");
    const [upload, setUpload] = useState();
    //const [singleUpload, setSingleUpload] = useState(["", "", "", "", "", ""]);
    const { data, setData } = useContext(DataContext);
    const { alert, setAlert } = useContext(AlertContext);
    let submitClicked = false;

    function fileUploadHandler(e) {
        setUpload(e.target.files[0]);
    }

    async function fileSubmitHandler() {

        const maxSize = 512 * 1024; // 500 KB
        if(submitClicked){
            return;
        }else if(upload == null){
            setAlert(["No File Selected", "Error"]);
            return;
        }else if (upload.type !== "text/csv"){
            setAlert(["CSV Files Only", "Error"]);
            return;
        }else if (upload.size > maxSize){
            setAlert(["File Exceeds 500 KB", "Error"]);
            return;
        }
        
        submitClicked = true;
        const curIds = data.map((value) => value.id);
        const formData = new FormData();
        formData.append('data', upload);
        formData.append('ids', curIds);

        setAlert(["Loading ... Can Take Up to 30s", "Loading"]);
        await fetch("http://0.0.0.0:8000/api/upload_spreadsheet", {

            method: 'POST',
            body: formData

        }).then((response) => {

            return response.json();

        }).then((response) => {

            if ("detail" in response){
                setAlert([response["detail"], "Error"]);
            }else{
                setAlert(["Success!", "Success"]);
                setData(data.concat(response));
                navigate("/view");
            }

        }).catch((error) => {
            
            setAlert(["Error When Fetching", "Error"]);

        });

        submitClicked = false;
        
    }

    /*
    function singleUploadHandler(){

        // TODO: check validity of data

        const result = {
            "Year": singleUpload[0],
            "Status": singleUpload[1],
            "School": singleUpload[2],
            "Program": singleUpload[3],
            "Average": singleUpload[4],
            "Decision Date": singleUpload[5]
        }

        setData(data.concat([result]));
        navigate("/view");

    }*/

    return (
        <>
            {/*<form className={state==="Upload" ? "uploadBar" : "uploadSingleBar"}>*/}
            <form className="uploadBar">
                {/*
                <select onChange={(v)=>setState(v.target.value)}>
                    <option value="Upload">Upload</option>
                    <option value="Input">Input</option>
                </select>*/}
                <p className="writing">Spreadsheet Upload</p>
                {/*{state === "Upload" ? renderSpreadSheetUpload(fileUploadHandler) : <div></div>}*/}
                {renderSpreadSheetUpload(upload===undefined?"":upload.name, fileUploadHandler)}
                {/*<button type="button" className="submit" onClick={state === "Upload" ? fileSubmitHandler : singleUploadHandler}>Upload</button>*/}
                <button type="button" className="submit" onClick={fileSubmitHandler}>Upload</button>
                {/*{state === "Input" ? renderSingleUpload(singleUpload, setSingleUpload) : <></>}*/}
            </form>
        </>
    );
        
};

export default Uploadbar;