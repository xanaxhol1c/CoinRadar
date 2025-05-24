import {Link} from 'react-router-dom'

export default function Home() {
    return (
        <div>
            <h1>Welcome to CoinRadar!</h1>
            <nav>
                <Link to="/coins">Coins</Link> |
                <Link to="/subscriptions">Subscriptions</Link>
            </nav>
        </div>
    );
}