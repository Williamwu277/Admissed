import Uploadbar from "../components/Uploadbar.js";
import Navbar from "../components/Navbar.js";
import spreadsheetImage from "./../image/AdmissedSpreadsheet.png";
import chartImage from "./../image/AdmissedChart.svg";
import messageImage from "./../image/AdmissedMessage.svg";
import "./Add.css";

function Add() {
    return (
        <div>
            <Navbar></Navbar>
            <div className="homepage">
                <h1 className="title">AdmissEd</h1>
                <Uploadbar />
                <div className="infoBar">
                    <img className="icon" src={spreadsheetImage}></img>
                    <p>
                        Procure Ontario university admission statistics data. 
                        Ensure columns Year, Status, School, Program, Average and Decision Date (D/M/Y) exist (Case Sensitive).
                        Upload a spreadsheet CSV file
                    </p>
                </div>
                <div className="infoBar">
                    <img className="icon" src={chartImage}></img>
                    <p>
                        View, sort, filter and delete uploaded data.
                        Choose a year, program and school of interest as well as secondary fields
                        to generate a report
                    </p>
                </div>
                <div className="infoBar">
                    <img className="icon" src={messageImage}></img>
                    <p>
                        Access the Github for sample data.
                        Otherwise, contact here for other inquiries
                    </p>
                </div>
            </div>
        </div>
    )
};


export default Add;