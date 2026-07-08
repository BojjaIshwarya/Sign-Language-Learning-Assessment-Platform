import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import api from "../services/api";
import { useNavigate } from "react-router-dom";

function Learning() {

    const navigate = useNavigate();

    const [courses, setCourses] = useState([]);

    useEffect(() => {
        loadCourses();
    }, []);

    const loadCourses = async () => {

        try {
            console.log("TOKEN:", localStorage.getItem("token"));
            const response = await api.get("/courses/");

            console.log("COURSES RESPONSE:", response);
            console.log("COURSES DATA:", response.data);

setCourses(response.data);

            setCourses(response.data);

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

                    <h2 className="mb-4">
                        Learning Courses
                    </h2>

                    <div className="row">

                        {courses.map(course => (

                            <div
                                className="col-md-4 mb-4"
                                key={course.id}
                            >

                                <div className="card shadow h-100">

                                    <div className="card-body">

                                        <h4>
                                            {course.title}
                                        </h4>

                                        <p>
                                            {course.description}
                                        </p>

                                        <span className="badge bg-primary">
                                            {course.level}
                                        </span>

                                        <br /><br />

                                        <button
                                            className="btn btn-success"
                                            onClick={() => navigate(`/courses/${course.id}`)}
                                        >
                                            Open Course
                                        </button>

                                    </div>

                                </div>

                            </div>

                        ))}

                    </div>

                </div>

            </div>

        </>

    );

}

export default Learning;
