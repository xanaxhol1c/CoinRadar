import notAvaliableIcon from '../img/not-avaliable-icon.png';
import starSubscribedIcon from '../img/star-subscribed-icon.png';
import { deleteSubscription, patchSubscription } from '../api/coinApi';
import { useState } from 'react';

export default function SubscriptionCard({ subscription, onSubscribe }) {
    const [threshold, setThreshold] = useState(subscription.threshold_percent);
    const [editThreshold, setEditThreshold] = useState(subscription.threshold_percent);
    const [isEditing, setIsEditing] = useState(false);
    const [error, setError] = useState('');

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

    const handleSaveThreshold = async () => {
        const parsedValue = parseFloat(editThreshold);
        if (isNaN(parsedValue) || parsedValue < 5) {
            const errorMessage = `Threshold must be a number ≥ 5`
            setError(errorMessage);
            return;
        }
        try {
            await patchSubscription({
                coin_slug: subscription.coin_ticker,
                threshold_percent: parsedValue
            });
            setThreshold(parsedValue);
            setIsEditing(false);
            setError('');
            if (onSubscribe) onSubscribe();
        } catch (error) {
            console.error("Failed to update threshold:", error);
        }
    };

    const handleCancelEdit = () => {
        setEditThreshold(threshold);
        setIsEditing(false);
        setError('');
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
            <span className="coin-card-field d-flex align-items-center gap-2 flex-column">
                {isEditing ? (
                    <>
                        <input
                            type="number"
                            value={editThreshold}
                            onChange={(e) => setEditThreshold(e.target.value)}
                            className={`form-control ${error ? 'is-invalid' : ''}`}
                            style={{
                                width: '110px',
                                padding: '2px 6px',
                                borderRadius: '4px'
                            }}
                        />
                        {error && (
                            <div
                                className="invalid-feedback"
                                style={{ width: '110px', display: 'block', whiteSpace: 'normal' }}
                                dangerouslySetInnerHTML={{ __html: error.replace('\n', '<br />') }}
                            />
                        )}

                        <div className='mt-2 d-flex flex-row' style={{ gap: '5px' }}>
                            <button className="btn btn-success btn-sm" onClick={handleSaveThreshold}>Save</button>
                            <button className="btn btn-secondary btn-sm" onClick={handleCancelEdit}>Cancel</button>
                        </div>
                    </>
                ) : (
                    <div className="d-flex flex-row align-items-center subscribe-threshold-field" style={{gap: 10 + "px"}}>
                        <span>{threshold}%</span>
                        <button className="btn btn-primary btn-sm" onClick={() => setIsEditing(true)}>Edit</button>
                    </div>
                )}
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
