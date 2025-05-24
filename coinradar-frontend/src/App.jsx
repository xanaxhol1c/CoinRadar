import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import Home from './pages/Home';
import Coins from './pages/Coins';
import Subscriptions from './pages/Subscriptions';
import Login from './pages/Login';

function App() {
    return(
        <Router>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/coins" element={<Coins />} />
                <Route path="/subscriptions" element={<Subscriptions />} />
                <Route path="/login" element={<Login />} />
            </Routes>
        </Router>
    );
}

export default App;