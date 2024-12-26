import { Link } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
    return (
        <nav className="navbar">
            <h1 className="logoTitle">AdmissEd</h1>
            <Link to="/add"><input type="button" value="Add Data" className="navButton"></input></Link>
            <Link to="/view"><input type="button" value="View Data" className="navButton"></input></Link>
            <Link to="/statistics"><input type="button" value="Statistics" className="navButton"></input></Link>
        </nav>
    )
}

export default Navbar;