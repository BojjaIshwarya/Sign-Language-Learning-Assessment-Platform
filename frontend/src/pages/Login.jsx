import { useState, useContext } from "react";
import { useNavigate, Link } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import api from "../services/api";

function Login() {

    const navigate = useNavigate();

    const { login } = useContext(AuthContext);

    const [email, setEmail] = useState("");

    const [password, setPassword] = useState("");

    const handleSubmit = async (e) => {

        e.preventDefault();

        try {

            const formData = new URLSearchParams();

            formData.append("username", email);
            formData.append("password", password);

            const response = await api.post(
                "/login",
                formData,
                {
                    headers: {
                        "Content-Type":
                        "application/x-www-form-urlencoded"
                    }
                }
            );
            
            console.log("LOGIN RESPONSE:", response.data);
            console.log("USER:", response.data.user);
            console.log("STRINGIFIED:", JSON.stringify(response.data.user));

            login(response.data.access_token);

            localStorage.setItem(
                "user",
                JSON.stringify(response.data.user)
            );

            navigate("/dashboard");

        }

        catch (err) {

            alert(
                err.response?.data?.detail ||
                "Login Failed"
            );

        }

    };

    return (

        <div className="container mt-5">

            <div className="row justify-content-center">

                <div className="col-md-5">

                    <div className="card shadow p-4">

                        <h2 className="text-center mb-4">
                            Login
                        </h2>

                        <form onSubmit={handleSubmit}>

                            <input
                                className="form-control mb-3"
                                placeholder="Email"
                                value={email}
                                onChange={(e)=>
                                    setEmail(e.target.value)}
                            />

                            <input
                                type="password"
                                className="form-control mb-3"
                                placeholder="Password"
                                value={password}
                                onChange={(e)=>
                                    setPassword(e.target.value)}
                            />

                            <button
                                className="btn btn-primary w-100">

                                Login

                            </button>

                        </form>

                        <p className="mt-3 text-center">

                            Don't have an account?

                            <Link to="/register">

                                Register

                            </Link>

                        </p>

                    </div>

                </div>

            </div>

        </div>

    );

}

export default Login;
