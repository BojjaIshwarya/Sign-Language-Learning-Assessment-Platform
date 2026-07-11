import { Link } from "react-router-dom";

function Sidebar() {

    return (

        <div
            className="bg-dark text-white p-3"
            style={{
                minHeight: "100vh",
                width: "250px"
            }}
        >

            <h4 className="mb-4">
                Dashboard
            </h4>

            <ul className="nav flex-column">

                <li className="nav-item mb-3">
                    <Link
                        className="nav-link text-white"
                        to="/dashboard"
                    >
                        Home
                    </Link>
                </li>

                <li className="nav-item mb-3">
                    <Link
                        className="nav-link text-white"
                        to="/learning"
                    >
                        Learning
                    </Link>
                </li>
                
                <li className="nav-item mb-3">
                    <Link
                        className="nav-link text-white"
                        to="/learning-paths"
                    >
                        Learning Paths
                    </Link>
                </li>

                <li className="nav-item mb-3">
                    <Link
                        className="nav-link text-white"
                        to="/assessment"
                    >
                        Assessment
                    </Link>
                </li>

                <li className="nav-item mb-3">
                    <Link
                        className="nav-link text-white"
                        to="/history"
                    >
                        History
                    </Link>
                </li>

                <li className="nav-item mb-3">
                    <Link
                        className="nav-link text-white"
                        to="/profile"
                    >
                        Profile
                    </Link>
                </li>

            </ul>

        </div>

    );

}

export default Sidebar;
