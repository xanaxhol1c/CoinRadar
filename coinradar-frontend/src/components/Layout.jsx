import { Link, Outlet } from 'react-router-dom';
import '../App.css';

export default function Layout() {
  return (
    <div>
      <header className="header">
            <Link to="/" style={{ textDecoration: 'none', color: 'white', marginTop: -5 + 'px'}}>
                <h2 className="logo">CoinRadar</h2>
            </Link>
            <nav>
                <Link to="/coins"><h5>Coins</h5></Link>
                <Link to="/subscriptions"><h5>Subscriptions</h5></Link>
            </nav>
      </header>

      <main className="container mt-4">
        <Outlet /> 
      </main>
    </div>
  );
}
