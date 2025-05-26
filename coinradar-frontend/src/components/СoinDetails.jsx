import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { getCoinDetails, getCoinHistory } from '../api/coinApi';
// import loadingImg from '../img/loading.webp';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

export default function CoinDetail() {
    const { slug } = useParams();
    const [coin, setCoin] = useState(null);
    const [history, setHistory] = useState([]);
    // const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const [days, setDays] = useState(7);
    const [percentChange, setPercentChange] = useState([]);
    const [infoMessage, setInfoMessage] = useState('');

    useEffect(() => {
        let isMounted = true;

        const fetchData = async () => {
            try {
                if (!isMounted) return;
                // setLoading(true);
                setError(null);
                setInfoMessage('');

                const coinData = await getCoinDetails(slug);
                if (isMounted) setCoin(coinData);

                const historyData = await getCoinHistory(slug, days);
                
                setPercentChange(findPercentChange(historyData));

                if (isMounted) {
                    if (historyData.length < days) {
                        setInfoMessage(`Only ${historyData.length} days of data available. Showing available data for last ${historyData.length} days.`);
                    } else {
                        setInfoMessage('');
                    }
                    setHistory(historyData);
                }
            } catch (err) {
                console.error("Error fetching data:", err);
                if (isMounted) setError('Failed to load coin data');
            } 
            // finally {
            //     if (isMounted) setLoading(false);
            // }
        };

        fetchData();
        const intervalId = setInterval(fetchData, 15000); 
        return () => {
            isMounted = false;
            clearInterval(intervalId);
        };
    }, [slug, days]);


    const formatChartData = () => {
        if (!history || history.length === 0) return null;

        const sortedHistory = [...history].sort((a, b) =>
        new Date(a.date) - new Date(b.date)
        );

    return {
        labels: sortedHistory.map(item =>
            new Date(item.date).toLocaleDateString('us-EN', {
            day: 'numeric',
            month: 'short'
            })
        ),
        datasets: [
            {
                label: 'Price (USD)',
                data: sortedHistory.map(item => parseFloat(item.price)),
                borderColor: 'rgba(58, 128, 233, 1)',
                backgroundColor: 'rgba(58, 128, 233, 0.1)',
                tension: 0.4,
                fill: true,
                pointBackgroundColor: 'rgba(58, 128, 233, 1)',
                pointRadius: 3,
                pointHoverRadius: 5,
            },
        ],
        };
    };

  const chartData = formatChartData();

  const formatNumber = (num) => {
    if (!num) return '0';
    return new Intl.NumberFormat('en-US', {
      style: 'decimal',
      maximumFractionDigits: 2
    }).format(num);
  };


    const findPercentChange = (data) => {
    if (!data || data.length < 2) return 0; 

    const startPrice = parseFloat(data[data.length - 1].price);
    const endPrice = parseFloat(data[0].price);

    if (startPrice === 0) return 0; 

    const percentChange = ((endPrice - startPrice) / startPrice) * 100;

    return percentChange.toFixed(2);  
    };

//   if (loading) { 
//     return (
//         <div className='d-flex flex-column justify-content-center align-items-center'>
//             <h1 style={{marginTop: "15%"}}>Coin details are loading...</h1>
//             <img className="loading-img" src={loadingImg} alt="loading img"/>
//         </div>
//     );
//   }

  if (error) {
    return (
        <div className='d-flex flex-column justify-content-center align-items-center'>
            <h1 style={{marginTop: "15%"}}>An error occured</h1>
        </div>
    );
  }

  if (!coin) {
    return (
        <div className='d-flex flex-column justify-content-center align-items-center'>
            <h1 style={{marginTop: "15%"}}>Coins details not found</h1>
        </div>
    );
  }

  const priceChangeClass = coin.percent_change_24h >= 0
    ? 'text-success'
    : 'text-danger';

return (
  <div className="container py-3">
        {infoMessage && (
        <div className="alert alert-info mt-2 py-2 px-3">
        {infoMessage}
        </div>
    )}
    <div className="row align-items-stretch">
      <div className="col-md-4 d-flex flex-column">
        <div className="card shadow-sm mb-2">
          <div className="card-body text-center">
            <img
              src={coin.image}
              alt={coin.name}
              className="img-fluid mb-3"
              style={{ width: '80px', height: '80px' }}
            />
            <h2 className="h4">
              {coin.name} <small className="text-muted">({coin.ticker})</small>
            </h2>

            <div className="d-flex justify-content-center align-items-center my-3 flex-column">
              <h3 className="me-2">${formatNumber(coin.price)}</h3>
              <span className={`badge ${priceChangeClass} fs-6`}>
                {coin.percent_change_24h >= 0 ? '+' : ''}
                {coin.percent_change_24h}% in 24h
              </span>
            </div>
          </div>
        </div>
        <div className="mb-3">
        <label htmlFor="daysSelect" className="form-label">Show data for:</label>
        <select
            id="daysSelect"
            className="form-select"
            value={days}
            onChange={(e) => setDays(Number(e.target.value))}
        >
            <option value={1}>1 Day</option>
            <option value={3}>3 Days</option>
            <option value={7}>7 Days</option>
            <option value={14}>14 Days</option>
            <option value={30}>30 Days</option>
        </select>

        </div>
        <div className="card shadow-sm d-flex flex-column">
          <div className="card-body d-flex flex-column">
            <h5 className="card-title">Coin Stats</h5>
            <ul className="list-group list-group-flush flex-grow-1">
              <li className="list-group-item d-flex justify-content-between align-items-center">
                Market Cap
                <span className="fw-bold">${formatNumber(coin.market_cap)}</span>
              </li>
              <li className="list-group-item d-flex justify-content-between align-items-center">
                24h Trading Volume
                <span className="fw-bold">${formatNumber(coin.volume_24h)}</span>
              </li>
              {history.length > 0 && (
                <>
                  <li className="list-group-item d-flex justify-content-between align-items-center">
                    {days}d High
                    <span className="fw-bold">
                      ${formatNumber(Math.max(...history.map(item => parseFloat(item.price))))}
                    </span>
                  </li>
                  <li className="list-group-item d-flex justify-content-between align-items-center">
                    {days}d Low
                    <span className="fw-bold">
                      ${formatNumber(Math.min(...history.map(item => parseFloat(item.price))))}
                    </span>
                  </li>
                </>
              )}
            </ul>
          </div>
        </div>
      </div>

      <div className="col-md-8 d-flex">
        <div className="card shadow-sm flex-fill d-flex flex-column">
          <div className="card-body d-flex flex-column">
            <h5 className="card-title">
                Price Chart ({history.length} days){" "}
                {percentChange !== 0 && percentChange !== '0.00' && percentChange !== null && percentChange !== undefined && (
                    <span style={{ color: percentChange > 0 ? 'green' : 'red', marginLeft: '8px' }}>
                    {percentChange > 0 ? '+' : ''}
                    {percentChange}%
                    </span>
                )}
            </h5>
            {chartData ? (
              <div className="chart-container flex-fill" style={{ height: '100%' }}>
                <Line
                  data={chartData}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                      legend: { display: false },
                      tooltip: {
                        callbacks: {
                          label: (context) => `$${context.raw.toLocaleString()}`
                        }
                      }
                    },
                    scales: {
                      y: {
                        beginAtZero: false,
                        ticks: {
                          callback: (value) => `$${value.toLocaleString()}`
                        }
                      }
                    }
                  }}
                />
              </div>
            ) : (
              <div className="text-center py-4">
                <p className="text-muted">No historical data available</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  </div>
);
}
