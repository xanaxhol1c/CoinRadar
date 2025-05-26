import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { getCoinDetails, getCoinHistory } from '../api/coinApi';
import loadingImg from '../img/loading.webp';
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
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const coinData = await getCoinDetails(slug);
        setCoin(coinData);

        const historyData = await getCoinHistory(slug, 4);
        setHistory(historyData);
      } catch (err) {
        console.error("Error fetching data:", err);
        setError('Failed to load coin data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [slug]);

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

  if (loading) {
    return (
      <div className='d-flex flex-column justify-content-center align-items-center min-vh-100'>
        <h1 className="text-primary mb-4">Loading coin details...</h1>
        <img
          className="loading-img"
          src={loadingImg}
          alt="loading"
          style={{ width: '100px', height: '100px' }}
        />
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mt-5 text-center">
        <div className="alert alert-danger" role="alert">
          {error}
        </div>
      </div>
    );
  }

  if (!coin) {
    return (
      <div className="container mt-5 text-center">
        <div className="alert alert-warning" role="alert">
          Coin not found
        </div>
      </div>
    );
  }

  const priceChangeClass = coin.percent_change_24h >= 0
    ? 'text-success'
    : 'text-danger';

return (
  <div className="container py-3">
    <div className="row align-items-stretch">
      <div className="col-md-4 d-flex flex-column">
        <div className="card shadow-sm mb-4">
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

            <div className="d-flex justify-content-center align-items-baseline my-3">
              <h3 className="me-2">${formatNumber(coin.price)}</h3>
              <span className={`badge ${priceChangeClass} fs-6`}>
                {coin.percent_change_24h >= 0 ? '+' : ''}
                {coin.percent_change_24h}%
              </span>
            </div>
          </div>
        </div>

        <div className="card shadow-sm flex-fill d-flex flex-column">
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
                    7d High
                    <span className="fw-bold">
                      ${formatNumber(Math.max(...history.map(item => parseFloat(item.price))))}
                    </span>
                  </li>
                  <li className="list-group-item d-flex justify-content-between align-items-center">
                    7d Low
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
            <h5 className="card-title">Price Chart ({history.length} days)</h5>
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
