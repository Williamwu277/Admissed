import Add from './pages/Add.js';
import View from './pages/View.js';
import Statistics from "./pages/Statistics.js";
import { DataContext } from "./DataContext";
import { Routes, Route } from "react-router-dom";
import { useState } from "react";
import './App.css';

function App() {

  const [data, setData] = useState([]);

  return (
    <DataContext.Provider value={{data, setData}}>
      <Routes>
          <Route path="/" element={<Add />} />
          <Route path="/add" element={<Add />} />
          <Route path="/view" element={<View />} />
          <Route path="/statistics" element={<Statistics />} />
      </Routes>
    </DataContext.Provider>
  );
}

export default App;
