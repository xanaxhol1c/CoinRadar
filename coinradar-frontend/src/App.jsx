import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import Coins from './pages/Coins';
import Subscriptions from './pages/Subscriptions';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="/coins" element={<Coins />} />
          <Route path="/subscriptions" element={<Subscriptions />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
