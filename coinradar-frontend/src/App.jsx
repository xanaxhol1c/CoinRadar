import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import Coins from './pages/Coins';
import Subscriptions from './pages/Subscriptions';
import Login from './pages/Login';
import Register  from './pages/Register';
import RequireAuth from './components/RequireAuth';
import Logout from './components/Logout';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="/coins" element={
              <RequireAuth>
                <Coins />
              </RequireAuth>
              }/>
          <Route path="/subscriptions" element={
              <RequireAuth>
                <Subscriptions />
              </RequireAuth>
          }/>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/logout" element={<Logout />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
