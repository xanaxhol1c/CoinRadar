import { useState, useEffect } from 'react';
import { Link, Outlet } from 'react-router-dom';
import coinradarLogo from '../img/coinradar-logo.png';
import Logout from './Logout';
import '../App.css';

export default function Layout() {
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('access'));

  useEffect(() => {
    function syncAuth() {
      setIsAuthenticated(!!localStorage.getItem('access'));
    }

    window.addEventListener('storage', syncAuth);
    return () => window.removeEventListener('storage', syncAuth);
  }, []);

  const handleLogout = () => {
    setIsAuthenticated(false);
  };

  return (
    <div>
      <header className="header">
        <Link to="/" style={{ textDecoration: 'none', color: 'white', marginTop: '-5px' }}>
          <div className='d-flex flex-row align-items-center' style={{gap: 5 + 'px'}}>
            <img
            src={coinradarLogo}
            alt={coinradarLogo}
            style={{width: "50px", height: "50px", cursor: "pointer", marginTop: 2 + "px"}}
            />
            <h2 className="logo">CoinRadar</h2>
          </div>
        </Link>
        <span className='d-flex flex-row justify-content-between' style={{ width: '90%' }}>
          <nav>
            <Link to="/coins"><h5>Coins</h5></Link>
            <Link to="/subscriptions"><h5>Subscriptions</h5></Link>
          </nav>
          <nav>
            {!isAuthenticated ? (
              <>
                <Link to="/login"><h5>Login</h5></Link>
                <Link to="/register"><h5>Register</h5></Link>
              </>
            ) : (
              <Logout onLogout={handleLogout} />
            )}
          </nav>
        </span>
      </header>

      <main className="container mt-4">
        <Outlet />
      </main>
    </div>
  );
}
