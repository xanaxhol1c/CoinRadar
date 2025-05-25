import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000/api/v1';

// Створюємо axios-екземпляр
const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Додаємо токен до кожного запиту
api.interceptors.request.use(
  config => {
    const access = localStorage.getItem('access');
    if (access) {
      config.headers['Authorization'] = `Bearer ${access}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

// Автоматичне оновлення токену при 401
api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refresh = localStorage.getItem('refresh');
        if (!refresh) throw new Error('No refresh token');

        const res = await axios.post(`${BASE_URL}/users/token/refresh/`, { refresh });
        const newAccess = res.data.access;

        localStorage.setItem('access', newAccess);
        originalRequest.headers['Authorization'] = `Bearer ${newAccess}`;

        return api(originalRequest); // Повторний запит з новим токеном
      } catch (refreshError) {
        console.error('Token refresh failed:', refreshError);
        logoutUser();
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// 🔐 API функції
export async function getCoins() {
  try {
    const res = await api.get('/coins/');
    return res.data;
  } catch (error) {
    console.error(error);
    throw new Error(error.response?.data?.detail || 'Failed to fetch coins');
  }
}

export async function registerUser(form) {
  try {
    const res = await axios.post(`${BASE_URL}/users/register/`, {
      username: form.username,
      email: form.email,
      password: form.password,
    });
    return res.data;
  } catch (error) {
    console.error(error);
    throw new Error(error.response?.data?.detail || 'Failed to register user');
  }
}

export async function loginUser(form) {
  try {
    const res = await axios.post(`${BASE_URL}/users/login/`, {
      email: form.email,
      password: form.password,
    });

    localStorage.setItem('access', res.data.access);
    localStorage.setItem('refresh', res.data.refresh);

    return res.data;
  } catch (error) {
    console.error(error);
    throw new Error(error.response?.data?.detail || 'Failed to login');
  }
}

export function logoutUser() {
  localStorage.removeItem('access');
  localStorage.removeItem('refresh');
}
