import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

function Dashboard() {

    const userData = localStorage.getItem("user");

    let user = null;

    if (userData && userData !== "undefined") {
        try {
            user = JSON.parse(userData);
        } catch (e) {
            console.error("Invalid user data:", userData);
        }
    }

    return (

        <>

            <Navbar />

            <div className="d-flex">

                <Sidebar />

                <div className="container-fluid p-4">

                    <h2>
                        Welcome, {user?.name} 👋
                    </h2>

                    <p>
                        Ready to continue your sign language journey?
                    </p>

                    <div className="row mt-4">

                        <div className="col-md-3">

                            <div className="card shadow">

                                <div className="card-body">

                                    <h5>Lessons</h5>

                                    <h2>0</h2>

                                </div>

                            </div>

                        </div>

                        <div className="col-md-3">

                            <div className="card shadow">

                                <div className="card-body">

                                    <h5>Assessments</h5>

                                    <h2>0</h2>

                                </div>

                            </div>

                        </div>

                        <div className="col-md-3">

                            <div className="card shadow">

                                <div className="card-body">

                                    <h5>Accuracy</h5>

                                    <h2>0%</h2>

                                </div>

                            </div>

                        </div>

                        <div className="col-md-3">

                            <div className="card shadow">

                                <div className="card-body">

                                    <h5>Level</h5>

                                    <h2>Beginner</h2>

                                </div>

                            </div>

                        </div>

                    </div>

                </div>

            </div>

        </>

    );

}

export default Dashboard;
