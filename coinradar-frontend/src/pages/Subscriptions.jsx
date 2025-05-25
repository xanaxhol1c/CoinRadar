import { useEffect, useState } from 'react';
import { getSubscriptions } from '../api/coinApi';
import SubscriptionCard from '../components/SubscriptionCard';

export default function Subscriptions() {
    const [subscriptions, setSubscriptions] = useState([]);

    useEffect(() => {
        const fetchData = () => {
            getSubscriptions()
                .then(data => setSubscriptions(data))
                .catch(err => console.error(err));
        };

        fetchData();

        const intervalId = setInterval(fetchData, 15000);

        return () => clearInterval(intervalId);
    }, []);

    if (subscriptions.length === 0)
        return (
        <div className='d-flex flex-column justify-content-center align-items-center'>
            <h1 className='d-flex justify-content-center' style={{marginTop : 15 + "%"}}>No active subscriptions found.</h1>
        </div>
         );

    return (
        <div>
            <h2>Active subscriptions</h2>
            <div className='mt-3'>
                <div className="coin-card-titles list-unstyled font-weight-bold">
                    <span className="coin-card-field">Name</span>
                    <span className="coin-card-field">Ticker</span>
                    <span className="coin-card-field">Threshold percent</span>
                    <span className="coin-card-field">Created at</span>
                    <span className="coin-card-field">Last notified</span>
                </div>
                <ul className="list-unstyled">
                    {
                        subscriptions.map(subscription => <SubscriptionCard key={subscriptions.id} subscription={subscription} />)
                    }
                </ul>
            </div>
        </div>
    )
}