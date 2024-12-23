import Add from './pages/Add.js';
import View from './pages/View.js';
import { Routes, Route } from "react-router-dom";
import './App.css';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Add />} />
      <Route path="/add" element={<Add />} />
      <Route path="/view" element={<View />} />
    </Routes>
  );
}

export default App;
