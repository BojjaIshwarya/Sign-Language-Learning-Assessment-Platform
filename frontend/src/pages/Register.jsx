import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../services/api";

function Register() {

    const navigate = useNavigate();

    const [form, setForm] = useState({
        name: "",
        email: "",
        password: "",
        role: "Learner"
    });

    const handleChange = (e) => {
        setForm({
            ...form,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {

            await api.post("/register", form);

            alert("Registration Successful!");

            navigate("/login");

        } catch (err) {

            alert(
                err.response?.data?.detail ||
                "Registration Failed"
            );

        }

    };

    return (

        <div className="container mt-5">

            <div className="row justify-content-center">

                <div className="col-md-5">

                    <div className="card shadow p-4">

                        <h2 className="text-center mb-4">
                            Register
                        </h2>

                        <form onSubmit={handleSubmit}>

                            <input
                                className="form-control mb-3"
                                placeholder="Name"
                                name="name"
                                onChange={handleChange}
                            />

                            <input
                                className="form-control mb-3"
                                placeholder="Email"
                                name="email"
                                onChange={handleChange}
                            />

                            <input
                                type="password"
                                className="form-control mb-3"
                                placeholder="Password"
                                name="password"
                                onChange={handleChange}
                            />

                            <button className="btn btn-success w-100">
                                Register
                            </button>

                        </form>

                        <p className="mt-3 text-center">

                            Already have an account?

                            <Link to="/login">
                                Login
                            </Link>

                        </p>

                    </div>

                </div>

            </div>

        </div>

    );

}

export default Register;
