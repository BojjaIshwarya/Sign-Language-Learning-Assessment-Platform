import { Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Learning from "./pages/Learning";
import Assessment from "./pages/Assessment";
import WebcamAssessment from "./pages/WebcamAssessment";
import History from "./pages/History";
import Profile from "./pages/Profile";
import CourseDetails from "./pages/CourseDetails";
import LessonContent from "./pages/LessonContent";
import LearningPaths from "./pages/LearningPaths";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" />} />

      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/learning" element={<Learning />} />
      <Route path="/assessment" element={<Assessment />} />
      <Route path="/webcam" element={<WebcamAssessment />} />
      <Route path="/history" element={<History />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="/courses/:id" element={<CourseDetails />} />
      <Route path="/lessons/:id" element={<LessonContent />} />
      <Route path="/learning-paths" element={<LearningPaths />} />
    </Routes>
  );
}

export default App;
