import axios from 'axios';

const BASE_URL = "http://127.0.0.1:8000/api/v1";

export async function getCoins() {
    try {
        const response = await axios.get(`${BASE_URL}/coins/`);
        return response.data;  
    } catch (error) {
        throw new Error("Failed to fetch coins");
    }
}

export async function registerUser(form) {
    try {
        const response = await axios.post(`${BASE_URL}/users/register/`, {
            username: form.username,
            email: form.email,
            password: form.password
            });
        return response.data;  
    } catch (error) {
        throw new Error(error.response?.data?.detail || "Failed to register user");
    }
}

export async function loginUser(form) {
    try {
        const response = await axios.post(`${BASE_URL}/users/login/`, {
          email: form.email,
          password: form.password
        });
        return response.data;
    } catch (error) {
        throw new Error(error.response?.data?.detail || "Failed to login");
    }
}

export async function refreshToken(refreshToken){
    try {
        const response = await axios.post(`${BASE_URL}/users/token/refresh/`, {
            refresh: refreshToken
        });
        return response.data.access;
    } catch (error) {
        throw new Error("Failed to refresh access token");
    }
}