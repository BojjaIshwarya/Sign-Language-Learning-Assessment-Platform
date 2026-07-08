import { useNavigate } from "react-router-dom";

function Navbar() {

    const navigate = useNavigate();

    const userData = localStorage.getItem("user");

    let user = null;

    if (userData && userData !== "undefined") {
        try {
            user = JSON.parse(userData);
        } catch (e) {
            console.error("Invalid user data:", userData);
        }
    }

    const logout = () => {
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        navigate("/login");
    };

    return (

        <nav className="navbar navbar-dark bg-primary">

            <div className="container-fluid">

                <span className="navbar-brand">
                    Sign Language Learning Platform
                </span>

                <div className="text-white">

                    Welcome, {user?.name}

                    <button
                        className="btn btn-light btn-sm ms-3"
                        onClick={logout}
                    >
                        Logout
                    </button>

                </div>

            </div>

        </nav>

    );

}

export default Navbar;
