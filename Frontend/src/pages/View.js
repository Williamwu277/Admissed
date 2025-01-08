import Navbar from "../components/Navbar.js";
import Filter from "../components/Filter.js";
import { useState, useContext } from "react";
import { DataContext } from "../Context.js";
import dataImage from "./../image/AdmissedData.png";
import sortImage from "./../image/AdmissedSort.svg";
import fileImage from "./../image/AdmissedFile.svg";
import cancelImage from "./../image/AdmissedCancel.svg";
import "./View.css";


function View() {

    const TABLE_SIZE = 100;
    const tableHeaders = ["Year", "Status", "School", "Program", "Average", "Decision Date"];
    const {data, setData} = useContext(DataContext);
    const [page, setPage] = useState(1);
    const [mode, setMode] = useState("view");
    // view mode, sort mode, filter mode, delete mode, incomplete mode
    const [sortBy, setSort] = useState(["Year", "Up"]);
    // filters
    const [filter, setFilter] = useState({
        "Year": "",
        "Status": "",
        "School": "",
        "Program": "",
        "Average": "",
        "Decision Date": ""
    });

    function renderMode() {
        
        const tableWidth = ["100px", "150px", "250px", "250px", "100px", "150px"]
        if (mode === "view" || mode === "edit" || mode === "incomplete"){
            return (
                <tr>
                    {
                        tableHeaders.map((header, id) =>
                            <th key={header} width={tableWidth[id]}>{header}</th>
                        )
                    }
                    {(mode === "edit" ? <th></th> : null)}
                </tr>
            )
        }else if(mode === "sort"){
            return (
                <tr>
                    {
                        tableHeaders.map(header =>
                            <th key={header}>
                                <button className="viewButton sortButton" onClick={() => {setSort([header, "Up"])}}>↑</button>
                                <button className="viewButton sortButton" onClick={() => {setSort([header, "Down"])}}>↓</button>
                            </th>
                        )
                    }
                </tr>
            )
        }else if(mode == "filter"){
            return (
                <tr>
                    <th><input className="filterText" type="text" placeholder="Year" onChange={(v) => {setFilter({...filter, ["Year"]: v.target.value})}} value={filter["Year"]}></input></th>
                    <th><input className="filterText" type="text" placeholder="Status" onChange={(v) => {setFilter({...filter, ["Status"]: v.target.value})}} value={filter["Status"]}></input></th>
                    <th><input className="filterText" type="text" placeholder="School" onChange={(v) => {setFilter({...filter, ["School"]: v.target.value})}} value={filter["School"]}></input></th>
                    <th><input className="filterText" type="text" placeholder="Program" onChange={(v) => {setFilter({...filter, ["Program"]: v.target.value})}} value={filter["Program"]}></input></th>
                    <th>Average</th>
                    <th>Decision Date</th>
                </tr>
            )
        }
    }

    function renderData(){

        let filteredData = data.filter(score => {
            const v = tableHeaders.map(
                header => filter[header] !== "" && !score[header].startsWith(filter[header])
            );
            return !v.includes(true);
            }
        );

        filteredData.sort((a, b) => {
            return (sortBy[1] == "Up" ? (
                a[sortBy[0]] < b[sortBy[0]] ? 1 : -1
             ) : (
                a[sortBy[0]] > b[sortBy[0]]) ? 1 : -1
            );
        });

        const rangeStart = (page - 1) * 100;
        const rangeEnd = Math.min(data.length, page * 100);

        const output = filteredData.slice(rangeStart, rangeEnd).map(score =>
            <tr className={score["Flag"] === "Y" ? " red" : "rowTable" } key={score.id}>
                {
                    //(mode === "edit" ? 
                    //    (tableHeaders.map(header => 
                    //        <td><input type="text" id={header+String(score.id)} defaultValue={score[header]}></input></td>
                    //    ))
                    //    : 
                        (tableHeaders.map(header => 
                            <td key={header}>{score[header]}</td>
                        ))//)
                }
                {(mode === "edit" ? <td><img src={cancelImage} className="delete" onClick={() => {setData(data.filter((v) => v.id !== score.id))}}></img></td> : null)}
            </tr>
        );

        return output;
    }

    function sortHandler() {
        if(mode === "sort"){
            setMode("view");
        }else{
            //if(mode === "edit"){
            //    propagateEdits();
            //}
            setMode("sort");
        }
    }

    function filterHandler() {
        if(mode === "filter"){
            setMode("view");
        }else{
            //if(mode === "edit"){
            //    propagateEdits();
            //}
            setMode("filter");
        }
    }

    function editHandler() {
        if(mode === "edit"){
            //propagateEdits();
            setMode("view");
        }else{
            setMode("edit");
        }
    }

    /*
    function propagateEdits() {
        const newData = data.map(score => {
            let row = {...score};
            tableHeaders.map(header => {
                const it = document.getElementById(header+String(score.id));
                if (it != null) {
                    row[header] = document.getElementById(header+String(score.id)).value;
                }
            });
            return row;
        })
        setData(newData);
    }*/

    return (
        <div>
            <Navbar></Navbar>
            <div className="viewPadder"></div>
            {data.length > 0 ?
                <div>
                    <div className="viewInfoBar">
                        <div className="viewInfoCell">
                            <img className="viewImage" src={dataImage}></img>
                            <p>
                                AdmissEd will try its best to sanitize the uploaded
                                data. If something is not recognized, it will be red
                            </p>
                        </div>
                        <div className="viewInfoCell">
                            <img className="viewImage" src={sortImage}></img>
                            <p>
                                You can use the sort, filter, delete and incomplete options
                                to explore the resulting table and/or clean it up
                            </p>
                        </div>
                        <div className="viewInfoCell">
                            <img className="viewImage" src={fileImage}></img>
                            <p>
                                Select a main program of interest and corresponding secondary fields 
                                to compare it with to generate an analysis
                            </p>
                        </div>
                    </div>
                    <Filter></Filter>
                    <table className="optionTable">
                        <tbody>
                            <tr>
                                <td><button className="viewButton optionButton" onClick={sortHandler}>Sort</button></td>
                                <td><button className="viewButton optionButton" onClick={filterHandler}>Filter</button></td>
                                <td><button className="viewButton optionButton" onClick={editHandler}>Delete</button></td>
                                <td><button className="viewButton optionButton" onClick={
                                    () => {
                                        if(sortBy[0] == "Flag" && sortBy[1] == "Up"){
                                            setSort(["Flag", "Down"]);
                                        }else {
                                            setSort(["Flag", "Up"]);
                                        }
                                    }
                                }>Incomplete</button></td>
                                <td>Page {page}</td>
                                <td><input type="range" min="1" max={Math.ceil(data.length / TABLE_SIZE)} value={page} onChange={(v)=>setPage(v.target.value)}></input></td>
                            </tr>
                        </tbody>
                    </table>
                    <table className="viewTable">
                        <tbody>
                            {renderMode()}
                            {renderData()}
                        </tbody>
                    </table>
                </div>
                :
                <div className="viewNA">
                    <h1>
                        Submit Data to View Table
                    </h1>
                </div>
            }
        </div>
    )
};


export default View;