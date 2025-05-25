import { useState } from 'react';
import { loginUser } from '../api/coinApi';

export default function Login() {
  const [form, setForm] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      const res = await loginUser(form);
      const { access, refresh } = res;
      localStorage.setItem('access', access);
      localStorage.setItem('refresh', refresh);
      setSuccess('Login successful');
      window.location.href = '/coins/';
    } catch (err) {
      setError(err.message || 'Something went wrong');
    }
  };

  return (
    <div className="container mt-4">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <input
            type="email"
            name="email"
            className="form-control"
            placeholder="Email"
            value={form.email}
            onChange={handleChange}
            required
          />
        </div>
        <div className="mb-3">
          <input
            type="password"
            name="password"
            className="form-control"
            placeholder="Password"
            value={form.password}
            onChange={handleChange}
            required
          />
        </div>
        {error && <p className="text-danger">{error}</p>}
        {success && <p className="text-success">{success}</p>}
        <button type="submit" className="btn btn-primary">Login</button>
      </form>
      <div className="mt-1">
            <p>
                Don't have an account?{' '}
                <a href="/register">Register</a>
            </p>
      </div>
    </div>
  );
}
