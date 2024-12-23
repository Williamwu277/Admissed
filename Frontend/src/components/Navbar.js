import { Link } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
    return (
        <nav className="navbar">
            <p>AdmissEd</p>
            <Link to="/add">Add Data</Link>
            <Link to="/view">View Data</Link>
            <p>View Statistics</p>
            <p>Settings</p>
        </nav>
    )
}

export default Navbar;