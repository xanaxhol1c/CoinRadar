import { useEffect, useState } from 'react';
import { getCoins} from '../api/coinApi';
import CoinCard from '../components/CoinCard';
import loadingImg from '../img/loading.webp';

export default function Home() {
  const [coins, setCoins] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchCoins= async () => {
    try {
      const coinsData = await getCoins(5);
      setCoins(coinsData);
      setLoading(false);
    } catch (error) {
      console.error(error);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCoins();

    const intervalId = setInterval(() => {
      fetchCoins();
    }, 15000);

    return () => clearInterval(intervalId);
  }, []);

  if (loading)
    return (
      <div className="d-flex flex-column justify-content-center align-items-center" style={{ marginTop: '15%' }}>
        <h1>Loading top coins...</h1>
        <img className="loading-img" src={loadingImg} alt="loading img" />
      </div>
    );

  return (
    <div>
      <div>
        <h2>Welcome to CoinRadar!</h2>
        <h5 style={{fontWeight: 400}}>Track cryptocurrency prices and manage your subscriptions with ease.</h5>
      </div>
      <div className="mt-4">
        <div className="coin-card-titles list-unstyled font-weight-bold" style={{ display: 'flex', gap: '1rem', marginBottom: '1rem' }}>
          <span style={{ flex: 2 }}>Name</span>
          <span style={{ flex: 1 }}>Ticker</span>
          <span style={{ flex: 1 }}>Price</span>
          <span style={{ flex: 2 }}>Market Cap</span>
          <span style={{ flex: 2 }}>Volume 24h</span>
          <span style={{ flex: 1 }}>Change 24h</span>
        </div>
        <ul className="list-unstyled" style={{ paddingLeft: 0 }}>
          {coins.map(coin => (
            <CoinCard
              key={coin.id}
              coin={coin}
              isSubscribed={false}
              onSubscribe={null}
              showSubscribeStar={false}  
            />
          ))}
        </ul>
      </div>
    </div>
  );
}
