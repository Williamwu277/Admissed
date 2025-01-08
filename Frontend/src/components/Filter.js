import { useState, useContext } from "react";
import { useNavigate} from "react-router-dom";
import { DataContext, GraphContext, AlertContext } from "../Context";
import "./Filter.css";


function Filter() {

    const navigate = useNavigate();
    const {data, setData} = useContext(DataContext);
    const {graphs, setGraphs} = useContext(GraphContext);
    const {alert, setAlert} = useContext(AlertContext);
    const [selected, setSelected] = useState(null);

    let filteredData = data.filter(score => score["Flag"] === "N");
    const yearList = [... (new Set(filteredData.map(score => score["Year"])))].sort();
    const schoolList = [... (new Set(filteredData.map(score => score["School"])))].sort();
    const programList = [... (new Set(filteredData.map(score => score["Program"])))].sort();

    const [selectYear, setSelectYear] = useState(yearList.length === 0 ? null : yearList[0]);
    const [selectSchool, setSelectSchool] = useState(schoolList.length === 0 ? null : schoolList[0]);
    const [selectProgram, setSelectProgram] = useState(programList.length === 0 ? null : programList[0]);

    const [subYears, setSubYears] = useState([]);
    const [subSchools, setSubSchools] = useState([]);
    const [subPrograms, setSubPrograms] = useState([]);
    let uploadClicked = false;

    if(data.length === 0)
    {
        return (
            <>
                <p>Please consider uploading data first</p>
            </>
        )
    }

    async function generateGraphs() {

        if(uploadClicked){
            return;
        }

        uploadClicked = true;
        await fetch("http://0.0.0.0:8000/api/get_graphs", {

            method: 'POST',
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                "data": data,
                "main_query": {
                    "Year": selected[0],
                    "School": selected[1],
                    "Program": selected[2]
                },
                "filters": {
                    "Year": subYears,
                    "School": subSchools,
                    "Program": subPrograms
                }
            })
        }).then((response) => {

            return response.json();

        }).then((response) => {

            if("detail" in response){
                setAlert(response["detail"]);
            }else{
                setGraphs(response);
                navigate("/report");
            }

        }).catch((error) => {

            setAlert("Error When Generating Report");

        });

        uploadClicked = false;

    }

    function renderScrollBar(arr, chosenValue, subSetter, subArr) {
        return (
            <div className="scrollBox">
                {arr.map(v => {
                    if (v === chosenValue){
                        return (
                            
                            <div key={v} className="scrollLine">
                                <p className="chosenP">{v}</p>
                                <div></div>
                            </div>
                            /*<>
                                <p key={v} className="chosenP">{v}</p>
                                <div key={v+"2"}></div>
                            </>*/
                        )
                    }else{
                        return (
                            <div key={v} className="scrollLine">
                                <p className="scrollP">{v}</p>
                                <input className="filterBox" value={v} type="checkbox" disabled={subArr.length >= 5 && !subArr.includes(v)} onChange={
                                    (t) => {
                                        if(subArr.includes(t.target.value)){
                                            subSetter(subArr.filter((s) => s != t.target.value));
                                        }else{
                                            subSetter(subArr.concat(t.target.value));
                                        }
                                    }
                                }></input>
                            </div>
                        )
                    }
                }
            )}
            </div>
        )
    }

    function renderSecondary() {

        if (selected === null){
            return <></>
        }

        return (
            <div className="secondarySelection">
                <p>Select Secondary Categories (5 each maximum)</p>
                <div className="scrollSection">
                    {renderScrollBar(yearList, selected[0], setSubYears, subYears)}
                    {renderScrollBar(schoolList, selected[1], setSubSchools, subSchools)}
                    {renderScrollBar(programList, selected[2], setSubPrograms, subPrograms)}
                </div>
                <button className="filterButton generateButton" onClick={generateGraphs}>Generate</button>
            </div>
        )
    }

    return (
        <>
            <div className={"mainSelection "+(selected===null?"roundBorders":"roundTopBorders")}>
                <h4>Select Main Program:</h4>
                <select onChange={(v) => setSelectYear(v.target.value)}>
                {
                    yearList.map(year => 
                        <option key={year} value={year}>{year}</option>
                    )
                }
                </select>
                <select onChange={(v) => setSelectSchool(v.target.value)}>
                {
                    schoolList.map(school => 
                        <option key={school} value={school}>{school}</option>
                    )
                }
                </select>
                <select onChange={(v) => setSelectProgram(v.target.value)}>
                {
                    programList.map(program => 
                        <option key={program} value={program}>{program}</option>
                    )
                }
                </select>
                <button className="filterButton selectButton" onClick={() => {
                    if(selectYear != null && selectSchool != null && selectProgram != null){
                        setSelected([selectYear, selectSchool, selectProgram]);
                    }
                }}>Select</button>
            </div>
            <div>
                {renderSecondary()}
            </div>
        </>
    )

}


export default Filter;