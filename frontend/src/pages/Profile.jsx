import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import api from "../services/api";

function Profile() {

    const [profile, setProfile] = useState(null);

    const user = JSON.parse(localStorage.getItem("user"));

    useEffect(() => {
        loadProfile();
    }, []);

    const loadProfile = async () => {

        try {

            const response = await api.get("/learning/profile");

            setProfile(response.data);

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

                    <h2>My Profile</h2>

                    <div className="card shadow mt-4">

                        <div className="card-body">

                            <h4>{user.name}</h4>

                            <hr />

                            <p>
                                <strong>Email:</strong> {user.email}
                            </p>

                            <p>
                                <strong>Role:</strong> {user.role}
                            </p>

                            {profile && (
                                <>
                                    <p>
                                        <strong>Learning Level:</strong>{" "}
                                        {profile.learning_level}
                                    </p>

                                    <p>
                                        <strong>Preferred Language:</strong>{" "}
                                        {profile.preferred_language}
                                    </p>
                                </>
                            )}

                        </div>

                    </div>

                </div>

            </div>

        </>

    );

}

export default Profile;
