import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../services/api";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import { useNavigate } from "react-router-dom";

function CourseDetails() {

    const { id } = useParams();

    const [course, setCourse] = useState(null);
    
    const [modules, setModules] = useState([]);
    
    const [lessons, setLessons] = useState([]);
    
    const [progress, setProgress] = useState(null);
    
    const navigate = useNavigate();

    useEffect(() => {
        loadCourse();
        loadModules();
        loadLessons();
        loadProgress();
    }, []);

    const loadCourse = async () => {
        try {
            const response = await api.get(`/courses/${id}`);
            setCourse(response.data);
        } catch (err) {
            console.log(err);
        }
    };

    const loadModules = async () => {
        try {
            const response = await api.get(`/courses/${id}/modules`);
            setModules(response.data);
        } catch (err) {
            console.log(err);
        }
    };
    
    const loadLessons = async () => {
        try {
            const response = await api.get(`/courses/${id}/lessons`);
            setLessons(response.data);
        } catch (err) {
            console.log(err);
        }
    };
    
    const loadProgress = async () => {
        try {

            const response = await api.get(`/learning/course-progress/${id}`);

            setProgress(response.data);

        } catch (err) {

            console.log(err);

        }
    };

    if (!course) {
        return <h3 className="text-center mt-5">Loading...</h3>;
    }
    return (
        <>
            <Navbar />

            <div className="d-flex">

                <Sidebar />

                <div className="container-fluid p-4">

                    <h2>{course.title}</h2>

                    <p>{course.description}</p>

                    <span className="badge bg-primary">
                    {course.level}
                    </span>
                    
                    <hr />

                    <h4>Course Progress</h4>

                    {progress && (

                        <>

                            <div className="progress mb-2" style={{ height: "25px" }}>

                                <div
                                    className="progress-bar bg-success"
                                    role="progressbar"
                                    style={{
                                        width: `${progress.progress_percentage}%`
                                    }}
                                >
                                    {progress.progress_percentage}%
                                </div>

                            </div>

                            <p>
                                {progress.completed_lessons} / {progress.total_lessons} Lessons Completed
                            </p>

                        </>

                    )}

                    <hr />

                    <hr />

                    <h3>Modules</h3>

                    {modules.length === 0 ? (

                        <p>No modules available.</p>

                    ) : (

                        modules.map(module => (

                            <div
                                key={module.id}
                                className="card mb-3"
                            >

                                <div className="card-body">

                                    <h5>{module.title}</h5>

                                    <p>{module.description}</p>

                                </div>

                            </div>

                        ))

                    )}
                    
                    <hr />

                    <h3>Lessons</h3>

                    {lessons.length === 0 ? (

                        <p>No lessons available.</p>

                    ) : (

                        lessons.map((lesson) => (

                            <div
                                key={lesson.id}
                                className="card mb-3 border-success"
        >

                                <div className="card-body">

                                    <h5>{lesson.title}</h5>

                                    <p>{lesson.description}</p>

                                    <button
                                        className="btn btn-success"
                                        onClick={() => navigate(`/lessons/${lesson.id}`)}
                                    >
                                        Start Lesson
                                    </button>

                                </div>

                            </div>

                        ))

                    )}
                       
                </div>

            </div>

        </>
    );
    
}

export default CourseDetails;
