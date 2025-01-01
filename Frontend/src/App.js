import Add from './pages/Add.js';
import View from './pages/View.js';
import Statistics from "./pages/Statistics.js";
import { DataContext, GraphContext } from "./Context";
import { Routes, Route } from "react-router-dom";
import { useState } from "react";
import './App.css';

function App() {

  const [data, setData] = useState([]);
  const [graphs, setGraphs] = useState(null);

  return (
    <DataContext.Provider value={{data, setData}}>
      <GraphContext.Provider value={{graphs, setGraphs}}>
        <Routes>
            <Route path="/" element={<Add />} />
            <Route path="/add" element={<Add />} />
            <Route path="/view" element={<View />} />
            <Route path="/report" element={<Statistics />} />
        </Routes>
      </GraphContext.Provider>
    </DataContext.Provider>
  );
}

export default App;
