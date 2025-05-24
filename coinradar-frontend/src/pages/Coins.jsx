import { useEffect, useState } from 'react'
import { getCoins } from '../api/coinApi';
import CoinCard from '../components/CoinCard';

export default function Coins() {
    const [coins, setCoins] = useState([]);

    useEffect(() => {
        const fetchData = () => {
            getCoins()
                .then(data => setCoins(data))
                .catch(err => console.error(err));
        };

        fetchData();

        const intervalId = setInterval(fetchData, 15000);

        return () => clearInterval(intervalId);
    }, []);

    return (
        <div>
            <h2>Cryptocurrency Prices by Market Cap</h2>

            <div className='mt-3'>
                <div className="coin-card-titles list-unstyled font-weight-bold">
                    <span className="coin-card-field">Name</span>
                    <span className="coin-card-field">Ticker</span>
                    <span className="coin-card-field">Price</span>
                    <span className="coin-card-field">Market Cap</span>
                    <span className="coin-card-field">Volume 24h</span>
                    <span className="coin-card-field">Change 24h</span>
                </div>
                <ul className="list-unstyled">
                    {
                        coins.map(coin => <CoinCard key={coin.id} coin={coin} />)
                    }
                </ul>
            </div>
        </div>
    )
}
