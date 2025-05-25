import notAvaliableIcon from '../img/not-avaliable-icon.png'

export default function CoinCard({ coin }) {
    const isNegative = coin.percent_change_24h < 0;
    const hasIcon = coin.image;

    function numberWithCommas(x) {
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    return (
        <li className="coin-card list-unstyled">
        <span className="coin-card-field d-flex flex-row align-items-center"> 
            <img src={ hasIcon ? coin.image : notAvaliableIcon} style={{width: 40 + "px", height: 40 + "px"}} alt="coin-icon"/>
            <p>{coin.name}</p>
        </span>
        <span className="coin-card-field">
            <p>{coin.ticker}</p>
        </span>
        <span className="coin-card-field">
            <p>{numberWithCommas(Number(coin.price).toFixed(2))}$</p>
        </span>
        <span className="coin-card-field">
            <p>{numberWithCommas(coin.market_cap)}$</p>
        </span>
        <span className="coin-card-field">
            <p>{numberWithCommas(coin.volume_24h)}$</p>
        </span>
        <span className="coin-card-field">
            <p style={{ color: isNegative ? 'red' : 'green'}}>{coin.percent_change_24h}%</p>
        </span>
        </li>
    );
}
