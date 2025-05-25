import { useState, useEffect } from 'react';
import { Link, Outlet } from 'react-router-dom';
import Logout from './Logout';
import '../App.css';

export default function Layout() {
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('access'));

  // Щоб стежити за змінами токена в localStorage можна використовувати подію storage
  useEffect(() => {
    function syncAuth() {
      setIsAuthenticated(!!localStorage.getItem('access'));
    }

    window.addEventListener('storage', syncAuth);
    return () => window.removeEventListener('storage', syncAuth);
  }, []);

  // Функція, яку можна передати в Logout, щоб одразу оновити стан
  const handleLogout = () => {
    setIsAuthenticated(false);
  };

  return (
    <div>
      <header className="header">
        <Link to="/" style={{ textDecoration: 'none', color: 'white', marginTop: '-5px' }}>
          <h2 className="logo">CoinRadar</h2>
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
