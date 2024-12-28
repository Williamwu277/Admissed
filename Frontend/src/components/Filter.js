import { useState, useContext} from "react";
import { DataContext } from "./../DataContext";
import "./Filter.css";


function Filter() {

    const {data, setData} = useContext(DataContext);
    const [selected, setSelected] = useState(null);

    const yearList = [... (new Set(data.map(score => score["Year"])))].sort();
    const schoolList = [... (new Set(data.map(score => score["School"])))].sort();
    const programList = [... (new Set(data.map(score => score["Program"])))].sort();

    const [selectYear, setSelectYear] = useState(yearList.length === 0 ? null : yearList[0]);
    const [selectSchool, setSelectSchool] = useState(schoolList.length === 0 ? null : schoolList[0]);
    const [selectProgram, setSelectProgram] = useState(programList.length === 0 ? null : programList[0]);

    const [subYears, setSubYears] = useState([]);
    const [subSchools, setSubSchools] = useState([]);
    const [subPrograms, setSubPrograms] = useState([]);

    if(data.length === 0)
    {
        return (
            <>
                <p>Please consider uploading data first</p>
            </>
        )
    }

    async function generateGraphs() {

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

            console.log(response);

        });

    }

    function renderScrollBar(arr, chosenValue, subSetter, subArr) {
        return (
            <div className="scrollBox">
                {arr.map(v => {
                    if (v === chosenValue){
                        return (
                            <>
                                <p className="chosenP">{v}</p>
                                <div></div>
                            </>
                        )
                    }else{
                        return (
                            <>
                                <p className="scrollP">{v}</p>
                                <input value={v} type="checkbox" disabled={subArr.length >= 5 && !subArr.includes(v)} onChange={
                                    (t) => {
                                        if(subArr.includes(t.target.value)){
                                            subSetter(subArr.filter((s) => s != t.target.value));
                                        }else{
                                            subSetter(subArr.concat(t.target.value));
                                        }
                                    }
                                }></input>
                            </>
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
                <button onClick={generateGraphs}>Generate</button>
            </div>
        )
    }

    return (
        <>
            <div className={"mainSelection "+(selected===null?"roundBorders":"roundTopBorders")}>
                <p>Select Main Program:</p>
                <select onChange={(v) => setSelectYear(v.target.value)}>
                {
                    yearList.map(year => 
                        <option value={year}>{year}</option>
                    )
                }
                </select>
                <select onChange={(v) => setSelectSchool(v.target.value)}>
                {
                    schoolList.map(school => 
                        <option value={school}>{school}</option>
                    )
                }
                </select>
                <select onChange={(v) => setSelectProgram(v.target.value)}>
                {
                    programList.map(program => 
                        <option value={program}>{program}</option>
                    )
                }
                </select>
                <button onClick={() => {
                    setSelected([selectYear, selectSchool, selectProgram]);
                    console.log(selected);
                }}>Select</button>
            </div>
            <div>
                {renderSecondary()}
            </div>
        </>
    )

}


export default Filter;