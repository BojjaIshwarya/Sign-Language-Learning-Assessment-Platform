import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import { useEffect, useState } from "react";
import api from "../services/api";

function Dashboard() {

    const userData = localStorage.getItem("user");

    let user = null;
    
    const [analytics, setAnalytics] = useState(null);
    
    useEffect(() => {
    loadAnalytics();
}, []);

    const loadAnalytics = async () => {

        try {

            const response = await api.get("/learning/analytics");

            setAnalytics(response.data);

        } catch (err) {

            console.log(err);

        }

    };

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

                                    <h2>{analytics?.lessons_completed ?? 0}</h2>

                                </div>

                            </div>

                        </div>

                        <div className="col-md-3">

                            <div className="card shadow">

                                <div className="card-body">

                                    <h5>Assessments</h5>

                                    <h2>{analytics?.practice_sessions ?? 0}</h2>

                                </div>

                            </div>

                        </div>

                        <div className="col-md-3">

                            <div className="card shadow">

                                <div className="card-body">

                                    <h5>Accuracy</h5>

                                    <h2>{analytics?.average_assessment_score ?? 0}%</h2>

                                </div>

                            </div>

                        </div>

                        <div className="col-md-3">

                            <div className="card shadow">

                                <div className="card-body">

                                    <h5>Level</h5>

                                    <h2>{analytics?.current_level ?? "Beginner"}</h2>

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
