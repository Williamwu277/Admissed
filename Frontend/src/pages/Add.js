import Uploadbar from "../components/Uploadbar.js";
import Navbar from "../components/Navbar.js";
import "./Add.css";

function Add() {
    return (
        <div>
            <Navbar></Navbar>
            <div className="homepage">
                <h1 className="title">AdmissEd</h1>
                <Uploadbar />
            </div>
        </div>
    )
};


export default Add;