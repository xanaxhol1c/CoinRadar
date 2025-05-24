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
