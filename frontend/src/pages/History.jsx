import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import api from "../services/api";

function History() {

    const [history, setHistory] = useState([]);

    useEffect(() => {
        loadHistory();
    }, []);

    const loadHistory = async () => {

        try {

            const response = await api.get("/learning/assessment-history");

            setHistory(response.data);

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

                    <h2>Assessment History</h2>

                    {history.length === 0 ? (

                        <div className="alert alert-info mt-3">
                            No assessments found.
                        </div>

                    ) : (

                        <table className="table table-bordered table-striped mt-3">

                            <thead className="table-dark">

                                <tr>
                                    <th>ID</th>
                                    <th>Assessment</th>
                                    <th>Score</th>
                                    <th>Level</th>
                                    <th>Feedback</th>
                                    <th>Date</th>
                                </tr>

                            </thead>

                            <tbody>

                                {history.map((item) => (

                                    <tr key={item.id}>

                                        <td>{item.id}</td>

                                        <td>{item.assessment_name}</td>

                                        <td>{item.score}</td>

                                        <td>{item.level}</td>

                                        <td>{item.feedback}</td>

                                        <td>
                                            {new Date(item.assessed_on).toLocaleString()}
                                        </td>

                                    </tr>

                                ))}

                            </tbody>

                        </table>

                    )}

                </div>

            </div>

        </>

    );

}

export default History;
