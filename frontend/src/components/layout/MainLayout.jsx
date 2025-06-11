// frontend/src/components/layout/MainLayout.jsx
import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';

const MainLayout = () => {
  return (
    <div>
      <Navbar />
      <main style={{ padding: '20px' }}>
        <Outlet /> {/* Child routes will render here */}
      </main>
    </div>
  );
};
export default MainLayout;
