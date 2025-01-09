import Add from './pages/Add.js';
import View from './pages/View.js';
import Statistics from "./pages/Statistics.js";
import BetterAlert from "./components/BetterAlert.js";
import PageNotFound from "./pages/PageNotFound.js";
import { DataContext, GraphContext, AlertContext } from "./Context";
import { Routes, Route } from "react-router-dom";
import { useState } from "react";
import './App.css';

function App() {

  const [data, setData] = useState([]);
  const [graphs, setGraphs] = useState(null);
  const [alert, setAlert] = useState("");

  return (
    <DataContext.Provider value={{data, setData}}>
      <GraphContext.Provider value={{graphs, setGraphs}}>
        <AlertContext.Provider value={{alert, setAlert}}>
          <BetterAlert></BetterAlert>
          <Routes>
              <Route path="/" element={<Add />} />
              <Route path="/add" element={<Add />} />
              <Route path="/view" element={<View />} />
              <Route path="/report" element={<Statistics />} />
              <Route path="/*" element={<PageNotFound />} />
          </Routes>
        </AlertContext.Provider>
      </GraphContext.Provider>
    </DataContext.Provider>
  );
}

export default App;
