import Navbar from "../components/Navbar.js";
import "./PageNotFound.css";


function PageNotFound() {

    return (
        <>
            <Navbar></Navbar>
            <div className="notFoundPadder"></div>
            <div className="notFound">
                <h1>Page Not Found</h1>
            </div>
        </>
    )

}


export default PageNotFound;