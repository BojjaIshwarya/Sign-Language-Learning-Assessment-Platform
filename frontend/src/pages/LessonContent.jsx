import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import api from "../services/api";

function LessonContent() {

    const { id } = useParams();

    const [contents, setContents] = useState([]);

    useEffect(() => {
        loadContents();
    }, []);

    const loadContents = async () => {

        try {

            const response = await api.get(`/courses/lessons/${id}/content`);

            setContents(response.data);

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

                    <h2>Lesson Content</h2>

                    {contents.length === 0 ? (

                        <p>No content available.</p>

                    ) : (

                        contents.map(content => (

                            <div
                                key={content.id}
                                className="card mb-4 shadow"
                            >

                                <div className="card-body">

                                    <h4>{content.title}</h4>

                                    <p>{content.description}</p>

                                    {content.content_type === "Video" && (

                                        <iframe
                                            width="700"
                                            height="400"
                                            src={content.content_url}
                                            title={content.title}
                                            allowFullScreen
                                        />

                                    )}

                                    {content.content_type === "Image" && (

                                        <img
                                            src={content.content_url}
                                            alt={content.title}
                                            className="img-fluid rounded"
                                        />

                                    )}

                                    {content.content_type === "PDF" && (

                                        <a
                                            href={content.content_url}
                                            target="_blank"
                                            rel="noreferrer"
                                            className="btn btn-primary"
                                        >
                                            Open PDF
                                        </a>

                                    )}

                                </div>

                            </div>

                        ))

                    )}

                    <button className="btn btn-success btn-lg">
                        Mark Lesson Completed
                    </button>

                </div>

            </div>

        </>

    );

}

export default LessonContent;
