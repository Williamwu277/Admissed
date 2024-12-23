import { useState } from "react";
import { useNavigate} from "react-router-dom";
import "./Uploadbar.css";


function renderSpreadSheetUpload(uploadHandler) {
    return (
        <>
            <input type="file" onChange={uploadHandler}></input>
        </>
    );
}


function Uploadbar() {

    const navigate = useNavigate();
    const [upload, setUpload] = useState();

    function fileUploadHandler(e) {
        setUpload(e.target.files[0]);
    }

    async function fileSubmitHandler() {

        if (upload.type !== "text/csv"){
            alert("CSV Only");
            return;
        }
        
        const formData = new FormData();
        formData.append('data', upload);

        const response = await fetch("http://0.0.0.0:8000/api/upload_spreadsheet", {
            method: 'POST',
            body: formData
        });

        const data = await response;

        if (data.status === 200){

            navigate("/view");

        }else{

            alert("Invalid Upload");
            
        }
        
    }

    return (
        <form>
            {renderSpreadSheetUpload(fileUploadHandler)}
            <button type="button" className="submit" onClick={fileSubmitHandler}>Upload</button>
        </form>
    );
        
};

export default Uploadbar;