import {Link} from 'react-router-dom'
import { useEffect, useState } from 'react'
import { getCoins } from '../api/coinApi';

export default function Coins() {
    const [coins, setCoins] = useState([]);

    const [loading, setLoading] = useState([true]);

    useEffect(() => {
        getCoins()
            .then(data => setCoins(data))
            .catch(err => console.error(err))
            .finally(() => setLoading(false))
    }, []);

    if (loading) return <p>Loading coins...</p>;

    return (
        <div>
            <h2>Coins</h2>
            <ul>
                {
                    coins.map(coin => <li key = {coin.id}>{coin.name} - {coin.price}$</li>)
                }
            </ul>
        </div>
    )

}

