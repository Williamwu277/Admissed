import { Link } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
    return (
        <nav className="navbar">
            <h1 className="logoTitle">AdmissEd</h1>
            <div className="navButtons">
                <Link to="/add"><input type="button" value="Add Data" className="navButton"></input></Link>
                <Link to="/view"><input type="button" value="View Data" className="navButton"></input></Link>
                <Link to="/report"><input type="button" value="Report" className="navButton"></input></Link>
            </div>
        </nav>
    )
}

export default Navbar;