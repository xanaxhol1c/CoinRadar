import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function RequireAuth({ children }) {
  const [isAuthorized, setIsAuthorized] = useState(null); // спочатку null, бо не знаємо ще
  const navigate = useNavigate();

  useEffect(() => {
    const access = localStorage.getItem('access');
    setIsAuthorized(!!access);
  }, []);

  if (isAuthorized === null) {
    // можна додати спінер тут, якщо хочеш
    return null; // поки що нічого не рендеримо
  }

  if (!isAuthorized) {
    return (
      <div style={{
        position: 'fixed',
        top: 0, left: 0, right: 0, bottom: 0,
        backgroundColor: 'rgba(0,0,0,0.8)',
        color: 'white',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: '1.5rem',
        zIndex: 9999
      }}>
        <p>Please login to view this page.</p>
        <button
          onClick={() => navigate('/login')}
          style={{
            marginTop: '20px',
            padding: '10px 20px',
            fontSize: '1rem',
            border: 'none',
            borderRadius: '5px',
            backgroundColor: '#007bff',
            color: 'white',
            cursor: 'pointer'
          }}
        >
          Go to Login
        </button>
      </div>
    );
  }

  return <>{children}</>;
}
