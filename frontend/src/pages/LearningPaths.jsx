import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import api from "../services/api";

function LearningPaths() {

    const [paths, setPaths] = useState([]);

    const [form, setForm] = useState({
        title: "",
        description: ""
    });

    const [editingId, setEditingId] = useState(null);

    useEffect(() => {
        fetchPaths();
    }, []);

    const fetchPaths = async () => {
        try {
            const res = await api.get("/learning/paths");
            setPaths(res.data);
        } catch (err) {
            console.error(err);
        }
    };

    const handleChange = (e) => {
        setForm({
            ...form,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {

        e.preventDefault();

        try {

            if (editingId) {

                await api.put(
                    `/learning/paths/${editingId}`,
                    form
                );

            } else {

                await api.post(
                    "/learning/paths",
                    form
                );

            }

            setForm({
                title: "",
                description: ""
            });

            setEditingId(null);

            fetchPaths();

        } catch (err) {
            console.error(err);
        }

    };

    const editPath = (path) => {

        setEditingId(path.id);

        setForm({
            title: path.title,
            description: path.description
        });

    };

    const deletePath = async (id) => {

        if (!window.confirm("Delete this learning path?"))
            return;

        await api.delete(`/learning/paths/${id}`);

        fetchPaths();

    };

    return (

        <>
            <Navbar />

            <div className="d-flex">

                <Sidebar />

                <div className="container-fluid p-4">

                    <h2>Learning Paths</h2>

                    <form
                        className="card p-3 mb-4"
                        onSubmit={handleSubmit}
                    >

                        <input
                            className="form-control mb-3"
                            placeholder="Learning Path Title"
                            name="title"
                            value={form.title}
                            onChange={handleChange}
                            required
                        />

                        <textarea
                            className="form-control mb-3"
                            placeholder="Description"
                            name="description"
                            value={form.description}
                            onChange={handleChange}
                        />

                        <button className="btn btn-primary">

                            {editingId
                                ? "Update Path"
                                : "Create Path"}

                        </button>

                    </form>

                    <table className="table table-bordered shadow">

                        <thead>

                            <tr>
                                <th>ID</th>
                                <th>Title</th>
                                <th>Description</th>
                                <th>Actions</th>
                            </tr>

                        </thead>

                        <tbody>

                            {paths.map((path) => (

                                <tr key={path.id}>

                                    <td>{path.id}</td>

                                    <td>{path.title}</td>

                                    <td>{path.description}</td>

                                    <td>

                                        <button
                                            className="btn btn-warning btn-sm me-2"
                                            onClick={() => editPath(path)}
                                        >
                                            Edit
                                        </button>

                                        <button
                                            className="btn btn-danger btn-sm"
                                            onClick={() => deletePath(path.id)}
                                        >
                                            Delete
                                        </button>

                                    </td>

                                </tr>

                            ))}

                        </tbody>

                    </table>

                </div>

            </div>

        </>

    );

}

export default LearningPaths;
