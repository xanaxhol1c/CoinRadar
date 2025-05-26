import notAvaliableIcon from '../img/not-avaliable-icon.png';
import starUnsubscribedIcon from '../img/star-unsubscribed-icon.png';
import starSubscribedIcon from '../img/star-subscribed-icon.png';
import { createSubscription, deleteSubscription } from '../api/coinApi';
import { useNavigate } from 'react-router-dom';

export default function CoinCard({ coin, isSubscribed, onSubscribe, showSubscribeStar = true  }) {
    const isNegative = coin.percent_change_24h < 0;

    const navigate = useNavigate();

    function numberWithCommas(x) {
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    const handleToggleSubscribe = async (e) => {
        e.stopPropagation();
        try {
            if (isSubscribed) {
                await deleteSubscription(coin.slug);
            } else {
                await createSubscription({ coin_id: coin.id });
            }
            if (onSubscribe) onSubscribe(); 
        } catch (error) {
            console.error("Subscription toggle failed:", error);
        }
    };

    const handleCoinCardClick = () => {
        navigate(`/coins/${coin.slug}/`);
    };

    return (
        <div onClick={handleCoinCardClick} style={{cursor: "pointer"}}>
            <li className="coin-card list-unstyled">
                <span className="coin-card-field d-flex flex-row align-items-center"> 
                <div className="d-flex gap-2 align-items-center">
                    {showSubscribeStar && (
                    <img
                        src={isSubscribed ? starSubscribedIcon : starUnsubscribedIcon}
                        onClick={handleToggleSubscribe}
                        alt={isSubscribed ? "Subscribed" : "Not subscribed"}
                        style={{width: "25px", height: "25px", cursor: "pointer"}}
                    />
                    )}
                </div>
                <img src={coin.image || notAvaliableIcon} style={{width: "40px", height: "40px"}} alt="coin-icon"/>
                <p>{coin.name}</p>
                </span>
                <span className="coin-card-field"><p>{coin.ticker}</p></span>
                <span className="coin-card-field"><p>{numberWithCommas(Number(coin.price).toFixed(2))}$</p></span>
                <span className="coin-card-field"><p>{numberWithCommas(coin.market_cap)}$</p></span>
                <span className="coin-card-field"><p>{numberWithCommas(coin.volume_24h)}$</p></span>
                <span className="coin-card-field">
                    <p style={{ color: isNegative ? 'red' : 'green' }}>
                        {coin.percent_change_24h}%
                    </p>
                </span>
            </li>
        </div>
    );
}