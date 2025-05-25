import { Link, Outlet } from 'react-router-dom';
import '../App.css';

export default function Layout() {
  return (
    <div>
      <header className="header">
            <Link to="/" style={{ textDecoration: 'none', color: 'white', marginTop: -5 + 'px'}}>
                <h2 className="logo">CoinRadar</h2>
            </Link>
            <span className='d-flex flex-row justify-content-between' style={{width: 90 + "%"}}>
                <nav>
                    <Link to="/coins"><h5>Coins</h5></Link>
                    <Link to="/subscriptions"><h5>Subscriptions</h5></Link>
                </nav>
                <nav>
                  <Link to="/login"><h5>Login</h5></Link>
                  <Link to="/register"><h5>Register</h5></Link>
                </nav>
            </span>
      </header>

      <main className="container mt-4">
        <Outlet /> 
      </main>
    </div>
  );
}
