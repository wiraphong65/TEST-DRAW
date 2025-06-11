// frontend/src/App.jsx
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import MainLayout from './components/layout/MainLayout';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import TopologyEditorPage from './pages/TopologyEditorPage';
// We might not need App.css for this shell, or it can be cleared/modified later
// import './App.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          <Route index element={<DashboardPage />} /> {/* Default page for / */}
          <Route path="login" element={<LoginPage />} />
          <Route path="register" element={<RegisterPage />} />
          <Route path="project/:projectId/edit" element={<TopologyEditorPage />} />
          {/* Add other routes as needed */}
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
export default App;
