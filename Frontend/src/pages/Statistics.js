import Navbar from "../components/Navbar.js";
import { GraphContext } from "../Context.js";
import { useContext } from "react";
import "./Statistics.css";


function Statistics() {

    const {graphs, setGraphs} = useContext(GraphContext);

    function renderReport(){

        if(graphs == null){
            return (
                <div className="statisticsNA">
                    <h1>
                        Submit Query to Generate Report
                    </h1>
                </div>
            )
        }

        return (
            <div className="statistics">
                <div className="report">
                    <h2 className="reportTitle">Unofficial Admission Statistics Report</h2>
                    <hr className="separator" />
                    <p>{graphs["Description"]}</p>
                    <h4 className="figureTitle">Figure 0. Table of Statistics</h4>
                    <hr className="separator" />
                    <table>
                        <tbody>
                            <tr>
                                <th>% Admission</th>
                                <th>Mean Admission Avg</th>
                                <th>Median Admission Avg</th>
                                <th>Min Admission Avg</th>
                                <th>Max Admission Avg</th>
                            </tr>
                            <tr>
                                <td>{graphs["Stats"]["Percent Admission"]}%</td>
                                <td>{graphs["Stats"]["Mean"]}%</td>
                                <td>{graphs["Stats"]["Median"]}%</td>
                                <td>{graphs["Stats"]["Min"]}%</td>
                                <td>{graphs["Stats"]["Max"]}%</td>
                            </tr>
                        </tbody>
                    </table>
                    {
                        graphs["Images"].map((img, ind) => 
                            <div key={img["Name"]} className="graph">
                                <h4 className="figureTitle">Figure {ind+1}. {img["Name"]}</h4>
                                <hr className="separator" />
                                <img src={"data:image/jpeg;base64,"+img["Image"]}></img>
                                <p>{img["Description"]}</p>
                            </div>
                        )
                    }
                    <hr className="separator" />
                    <h4>End of Report</h4>
                </div>
            </div>
        )
    }

    return (
        <>
            <Navbar></Navbar>
            <div className="padder"></div>
            {renderReport()}
        </>
    )

}


export default Statistics;