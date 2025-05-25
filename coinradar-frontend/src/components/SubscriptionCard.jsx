export default function SubscriptionCard({ subscription }) {
    const lastNotified = subscription.last_notified;

    return (
        <li className="coin-card list-unstyled">
        {/* <span className="coin-card-field d-flex flex-row align-items-center"> 
            <img src={ hasIcon ? coin.image : notAvaliableIcon} style={{width: 40 + "px", height: 40 + "px"}} alt="coin-icon"/>
            <p>{coin.name}</p>
        </span> */}
        <span className="coin-card-field">
            <p>{subscription.coin_name}</p>
        </span>
        <span className="coin-card-field">
            <p>{(subscription.coin_ticker).toUpperCase()}</p>
        </span>
        <span className="coin-card-field">
            <p>{subscription.threshold_percent}%</p>
        </span>
        <span className="coin-card-field">
            <p>{subscription.created_at}</p>
        </span>
        <span className="coin-card-field">
            <p>{lastNotified ? subscription.last_notified : "-"}</p>
        </span>
        </li>
    );
}
