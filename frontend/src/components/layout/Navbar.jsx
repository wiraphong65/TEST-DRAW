// frontend/src/components/layout/Navbar.jsx
import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav style={{ padding: '10px', background: '#eee' }}>
      <Link to="/" style={{ marginRight: '10px' }}>Home/Projects</Link>
      <Link to="/login" style={{ marginRight: '10px' }}>Login</Link>
      <Link to="/register">Register</Link>
      {/* Later, add conditional links based on auth state */}
    </nav>
  );
};
export default Navbar;
