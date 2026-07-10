import { useRef, useState } from "react";
import api from "../services/api";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

function WebcamAssessment() {

    const videoRef = useRef(null);
    
    const canvasRef = useRef(null);

    const [cameraOn, setCameraOn] = useState(false);
    const [expectedSign, setExpectedSign] = useState("A");
    const [prediction, setPrediction] = useState("");
    const [confidence, setConfidence] = useState("");
    const [feedback, setFeedback] = useState("");

    const startCamera = async () => {

        const stream = await navigator.mediaDevices.getUserMedia({
            video: true
        });

        videoRef.current.srcObject = stream;

        setCameraOn(true);

    };
    
    const captureAndAssess = async () => {

        const canvas = canvasRef.current;
        const video = videoRef.current;

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        const ctx = canvas.getContext("2d");

        ctx.drawImage(video, 0, 0);

        canvas.toBlob(async (blob) => {

            const profile = await api.get("/learning/profile");

            const formData = new FormData();

            formData.append("expected_sign", expectedSign);
            formData.append("learner_profile_id", profile.data.id);
            formData.append("image", blob, "frame.jpg");

            try {

                const response = await api.post(
                    "/assessment/predict",
                    formData
                );

                setPrediction(response.data.predicted_sign);
                setConfidence(response.data.confidence);
                setFeedback(response.data.feedback);

            } catch (err) {

                console.log(err);

            }

        }, "image/jpeg");

    };

    return (

        <>
            <Navbar />

            <div className="d-flex">

                <Sidebar />

                <div className="container-fluid p-4">

                    <h2>AI Webcam Assessment</h2>

                    <div className="card shadow p-4">

                        <video
                            ref={videoRef}
                            autoPlay
                            playsInline
                            width="640"
                            height="480"
                            className="border rounded"
                        />
                        
                        <canvas
                            ref={canvasRef}
                            style={{ display: "none" }}
                        />

                        <div className="mt-3">

                            <label className="form-label">
                                Expected Sign
                            </label>

                            <select
                                className="form-select"
                                value={expectedSign}
                                onChange={(e) => setExpectedSign(e.target.value)}
                            >

                                {"ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("").map(letter => (

                                    <option key={letter}>
                                        {letter}
                                    </option>

                                ))}

                            </select>

                        </div>

                        <button
                            className="btn btn-success mt-3"
                            onClick={captureAndAssess}
                        >
                            Capture & Assess
                        </button>

                        <hr />

                        <h5>Prediction: {prediction}</h5>

                        <h5>Confidence: {confidence}</h5>

                        <p>{feedback}</p>

                        <br />

                        {!cameraOn && (

                            <button
                                className="btn btn-primary mt-3"
                                onClick={startCamera}
                            >
                                Start Camera
                            </button>

                        )}

                    </div>

                </div>

            </div>

        </>

    );

}

export default WebcamAssessment;
