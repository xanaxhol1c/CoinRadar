import { getCoins, getSubscriptions } from '../api/coinApi';
import CoinCard from '../components/CoinCard';
import { useEffect, useState } from 'react';
import loadingImg from '../img/loading.webp';

export default function Coins() {
    const [coins, setCoins] = useState([]);
    const [subscriptions, setSubscriptions] = useState([]);

    const fetchCoins = async () => {
        try {
            const data = await getCoins();
            setCoins(data);
        } catch (err) {
            console.error(err);
        }
    };

    const fetchSubscriptions = async () => {
        try {
            const data = await getSubscriptions();
            setSubscriptions(data);
        } catch (err) {
            console.error(err);
        }
    };

    useEffect(() => {
        fetchCoins();
        fetchSubscriptions();

        const intervalId = setInterval(() => {
            fetchCoins();
            fetchSubscriptions();
        }, 15000);

        return () => clearInterval(intervalId);
    }, []);

    if (coins.length === 0)
        return (
        <div className='d-flex flex-column justify-content-center align-items-center'>
            <h1 style={{marginTop: "15%"}}>Coins are loading...</h1>
            <img className="loading-img" src={loadingImg} alt="loading img"/>
        </div>
         );

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
                        coins.map(coin =>
                            <CoinCard
                                key={coin.id}
                                coin={coin}
                                isSubscribed={subscriptions.some(sub => String(sub.coin_name) === String(coin.name))}
                                onSubscribe={fetchSubscriptions} 
                            />
                        )
                    }
                </ul>
            </div>
        </div>
    );
}
