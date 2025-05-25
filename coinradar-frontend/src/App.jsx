import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import Coins from './pages/Coins';
import Subscriptions from './pages/Subscriptions';
import Login from './pages/Login';
import Register  from './pages/Register';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="/coins" element={<Coins />} />
          <Route path="/subscriptions" element={<Subscriptions />} />
            <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
