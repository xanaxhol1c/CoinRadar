import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000/api/v1';

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

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

        return api(originalRequest); 
      } catch (refreshError) {
        console.error('Token refresh failed:', refreshError);
        logoutUser();
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export async function getCoins() {
  try {
    const res = await api.get('/coins/');
    return res.data;
  } catch (error) {
    console.error(error);
    throw new Error(error.response?.data?.detail || 'Failed to fetch coins');
  }
}

export async function getCoinDetails(slug) {
    try {
      const res = await api.get(`${BASE_URL}/coins/${slug}/`);
      return res.data;
    } catch (error) {
    throw new Error('Failed to get coin by slug');
  }
}

export async function getCoinHistory(slug, days=null) {
    if (days)
      try {
        const res = await api.get(`${BASE_URL}/coins/${slug}/history/?days=${days}`);
        return res.data;
      } catch (error) {
      throw new Error('Failed to get coin by slug');
      }
    else  
      try {
        const res = await api.get(`${BASE_URL}/coins/${slug}/history/`);
        return res.data;
      } catch (error) {
      throw new Error('Failed to get coin by slug');
      }
}


export async function registerUser(form) {
  try {
    const res = await api.post(`${BASE_URL}/users/register/`, {
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
    const res = await api.post(`${BASE_URL}/users/login/`, {
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

export async function getSubscriptions() {
  try {
    const res = await api.get('/subscriptions/');
    return res.data;
  } catch (error) {
    console.error(error);
    throw new Error(error.response?.data?.detail || 'Failed to get subscriptions');
  }
}

export async function createSubscription({coin_id}) {
        try {
            const res = await api.post('/subscriptions/', {
            coin_id
            });
            return res.data;
        } catch (error) {
            console.error(error);
            throw new Error(error.response?.data?.detail || 'Failed to create subscription');
        }
    }

export async function patchSubscription({coin_slug, threshold_percent}) {
    try {
        const res = await api.patch(`/subscriptions/${coin_slug}/`, {
            threshold_percent : threshold_percent
        });
        return res.data;
    } catch (error) {
        console.error(error);
        throw new Error('Failed to patch subscriptions');
    }
}

export async function deleteSubscription(coin_slug) {
  try {
    const res = await api.delete(`/subscriptions/${coin_slug}/`);
    return res.data;
  } catch (error) {
    console.error(error);
    throw new Error('Failed to delete subscriptions');
  }
}

export function logoutUser() {
  localStorage.removeItem('access');
  localStorage.removeItem('refresh');
}
