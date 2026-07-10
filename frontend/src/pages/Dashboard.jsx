import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import api from "../services/api";

function Dashboard() {

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

    const [analytics, setAnalytics] = useState(null);
    const [recommendation, setRecommendation] = useState(null);
    const [skills, setSkills] = useState([]);

    useEffect(() => {
        loadAnalytics();
        loadRecommendation();
         loadSkills();
    }, []);

    const loadAnalytics = async () => {

        try {

            const response = await api.get("/learning/analytics");

            setAnalytics(response.data);

        } catch (err) {

            console.log(err);

        }

    };

    const loadRecommendation = async () => {

        try {

            const response = await api.get("/learning/recommendation");

            setRecommendation(response.data);

        } catch (err) {

            console.log(err);

        }

    };
    
    const loadSkills = async () => {

        try {

            const response = await api.get("/learning/skill-mastery");

            setSkills(response.data);

        } catch (err) {

            console.log(err);

        }

    };

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

                                <div className="card-body text-center">

                                    <h5>Lessons</h5>

                                    <h2>{analytics?.lessons_completed ?? 0}</h2>

                                </div>

                            </div>

                        </div>

                        <div className="col-md-3">

                            <div className="card shadow">

                                <div className="card-body text-center">

                                    <h5>Practice Sessions</h5>

                                    <h2>{analytics?.practice_sessions ?? 0}</h2>

                                </div>

                            </div>

                        </div>

                        <div className="col-md-3">

                            <div className="card shadow">

                                <div className="card-body text-center">

                                    <h5>Accuracy</h5>

                                    <h2>{analytics?.average_assessment_score ?? 0}%</h2>

                                </div>

                            </div>

                        </div>

                        <div className="col-md-3">

                            <div className="card shadow">

                                <div className="card-body text-center">

                                    <h5>Level</h5>

                                    <h2>{analytics?.current_level ?? "Beginner"}</h2>

                                </div>

                            </div>

                        </div>

                    </div>

                    <div className="row mt-4">

                        <div className="col-md-12">

                            <div className="card shadow">

                                <div className="card-body">

                                    <h4>📚 Recommended Next Lesson</h4>

                                    {recommendation ? (

                                        <>

                                            <h5>{recommendation.lesson_title}</h5>

                                            <p>{recommendation.reason}</p>

                                            {recommendation.lesson_id !== 0 ? (

                                                <button
                                                    className="btn btn-success"
                                                    onClick={() => navigate(`/lessons/${recommendation.lesson_id}`)}
                                                >
                                                    Start Learning
                                                </button>

                                            ) : (

                                                <button
                                                    className="btn btn-primary"
                                                    onClick={() => navigate("/assessment")}
                                                >
                                                    Practice Assessment
                                                </button>

                                            )}

                                        </>

                                    ) : (

                                        <p>Loading recommendation...</p>

                                    )}

                                </div>

                            </div>

                        </div>

                    </div>
                    
                    <div className="row mt-4">

                        <div className="col-md-12">

                            <div className="card shadow">

                                <div className="card-body">

                                    <h4>🏆 Skill Mastery</h4>

                                    {skills.length === 0 ? (

                                        <p>No skills available.</p>

                                    ) : (

                                        skills.map((skill) => (

                                            <div key={skill.skill_name} className="mb-3">

                                                <div className="d-flex justify-content-between">

                                                    <strong>{skill.skill_name}</strong>

                                                    <span>{skill.mastery_percentage}%</span>

                                                </div>

                                                <div className="progress">

                                                    <div
                                                        className="progress-bar bg-success"
                                                            role="progressbar"
                                                            style={{ width: `${skill.mastery_percentage}%` }}
                                                    >
                                                        {skill.skill_level}
                                                    </div>

                                                </div>

                                            </div>

                                        ))

                                    )}

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
