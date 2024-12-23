import Navbar from "../components/Navbar.js";
import { useState, useEffect } from "react";
import "./View.css";

// TODO: specify maximum table width

function View() {

    const [data, setData] = useState(null);

    useEffect(() => {

        async function createTable() {

            const response = await fetch("http://0.0.0.0:8000/api/get_data", {
                method: 'GET'
            });
    
            const data = await response.json();
    
            const output = data.map(score => 
                <tr className="rowTable" key={score.id}>
                    <td>{score.Year}</td>
                    <td>{score.Status}</td>
                    <td>{score.School}</td>
                    <td>{score.Program}</td>
                    <td>{score.Average}</td>
                    <td>{score["Decision Date"]}</td>
                </tr>
            );
    
            setData(output);
        }

        createTable();

    }, []);


    return (
        <div>
            <Navbar></Navbar>
            <table className="viewTable">
                <tbody>
                    <tr>
                        <th>Year</th>
                        <th>Status</th>
                        <th>School</th>
                        <th>Program</th>
                        <th>Average</th>
                        <th>Decision Date</th>
                    </tr>
                    {data}
                </tbody>
            </table>
        </div>
    )
};


export default View;