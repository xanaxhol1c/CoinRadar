import notAvaliableIcon from '../img/not-avaliable-icon.png';
import starSubscribedIcon from '../img/star-subscribed-icon.png';
import { deleteSubscription } from '../api/coinApi';

export default function SubscriptionCard({ subscription, onSubscribe }) {
    const lastNotified = subscription.last_notified;
    const isNegative = subscription.coin_percent_change_24h < 0;
    const hasIcon = subscription.coin_image;
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };

    const handleToggleSubscribe = async () => {
        try {
            await deleteSubscription(subscription.coin_ticker);
            if (onSubscribe) onSubscribe();  
        } catch (error) {
            console.error("Failed to toggle subscription:", error);
        }
    };

    return (
        <li className="coin-card list-unstyled">
            <span className="coin-card-field d-flex flex-row align-items-center"> 
                <div className="d-flex gap-2 align-items-center">
                    <img
                        src={starSubscribedIcon}
                        onClick={handleToggleSubscribe}
                        alt="Subscribed"
                        style={{ width: "25px", height: "25px", cursor: "pointer" }}
                    />
                </div>
                <img src={hasIcon ? subscription.coin_image : notAvaliableIcon} style={{ width: "40px", height: "40px" }} alt="coin-icon" />
                <p>{subscription.coin_name}</p>
            </span>
            <span className="coin-card-field">
                <p>{(subscription.coin_ticker).toUpperCase()}</p>
            </span>
            <span className="coin-card-field">
                <p style={{ color: isNegative ? 'red' : 'green' }}>{subscription.coin_percent_change_24h}%</p>
            </span>
            <span className="coin-card-field">
                <p>{subscription.threshold_percent}%</p>
            </span>
            <span className="coin-card-field">
                <p>{new Date(subscription.created_at).toLocaleDateString("en-US", options)}</p>
            </span>
            <span className="coin-card-field">
                <p>{lastNotified ? new Date(subscription.last_notified).toLocaleDateString("en-US", options) : "-"}</p>
            </span>
        </li>
    );
}
