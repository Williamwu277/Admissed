import Navbar from "../components/Navbar.js";
import { useState, useContext } from "react";
import { DataContext } from "./../DataContext";
import "./View.css";

// TODO: specify maximum table width
// TODO: Sort, Filter, Delete

function View() {

    const TABLE_SIZE = 100;
    const tableHeaders = ["Year", "Status", "School", "Program", "Average", "Decision Date"];
    const {data, setData} = useContext(DataContext);
    const [page, setPage] = useState(1);
    const [mode, setMode] = useState("view");
    // view mode, sort mode, filter mode, delete mode
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
        
        if (mode === "view" || mode === "edit"){
            return (
                <tr>
                    {
                        tableHeaders.map(header =>
                            <th>{header}</th>
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
                            <th>
                                <button onClick={() => {setSort([header, "Up"])}}>↑</button>
                                <button onClick={() => {setSort([header, "Down"])}}>↓</button>
                            </th>
                        )
                    }
                </tr>
            )
        }else if(mode == "filter"){
            return (
                <tr>
                    <th><input type="text" placeholder="Year" onChange={(v) => {setFilter({...filter, ["Year"]: v.target.value})}} value={filter["Year"]}></input></th>
                    <th><input type="text" placeholder="Status" onChange={(v) => {setFilter({...filter, ["Status"]: v.target.value})}} value={filter["Status"]}></input></th>
                    <th><input type="text" placeholder="School" onChange={(v) => {setFilter({...filter, ["School"]: v.target.value})}} value={filter["School"]}></input></th>
                    <th><input type="text" placeholder="Program" onChange={(v) => {setFilter({...filter, ["Program"]: v.target.value})}} value={filter["Program"]}></input></th>
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
            return (sortBy[1] === "Up" ? a[sortBy[0]] < b[sortBy[0]] : a[sortBy[0]] > b[sortBy[0]]);
        });

        const rangeStart = (page - 1) * 100;
        const rangeEnd = Math.min(data.length, page * 100);

        const output = filteredData.slice(rangeStart, rangeEnd).map(score =>
            <tr className="rowTable" key={score.id}>
                {
                    (mode === "edit" ? 
                        (tableHeaders.map(header => 
                            <td><input type="text" id={header+String(score.id)} defaultValue={score[header]}></input></td>
                        ))
                        : 
                        (tableHeaders.map(header => 
                            <td>{score[header]}</td>
                        )))
                }
                {(mode === "edit" ? <td><button onClick={() => {setData(data.filter((v) => v.id !== score.id))}}></button></td> : null)}
            </tr>
        );

        return output;
    }

    function sortHandler() {
        if(mode === "sort"){
            setMode("view");
        }else{
            if(mode === "edit"){
                propagateEdits();
            }
            setMode("sort");
        }
    }

    function filterHandler() {
        if(mode === "filter"){
            setMode("view");
        }else{
            if(mode === "edit"){
                propagateEdits();
            }
            setMode("filter");
        }
    }

    function editHandler() {
        if(mode === "edit"){
            propagateEdits();
            setMode("view");
        }else{
            setMode("edit");
        }
    }

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
    }

    return (
        <div>
            <Navbar></Navbar>
            <table className="optionTable">
                <tbody>
                    <tr>
                        <td><button onClick={sortHandler}>Sort</button></td>
                        <td><button onClick={filterHandler}>Filter</button></td>
                        <td><button onClick={editHandler}>Edit</button></td>
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
    )
};


export default View;