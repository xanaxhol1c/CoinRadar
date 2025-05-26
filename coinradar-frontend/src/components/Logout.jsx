import { logoutUser } from '../api/coinApi';
import { useNavigate } from 'react-router-dom';

export default function Logout({ onLogout }) {
  const navigate = useNavigate();

  const handleLogout = (e) => {
    e.preventDefault();
    logoutUser();
    if (onLogout) onLogout();   
    navigate('/');
  };

  return (
    <a href='/' onClick={handleLogout} style={{ cursor: 'pointer', color: 'inherit', textDecoration: 'none' }}>
      <h5>Logout</h5>
    </a>
  );
}
