const BASE_URL = "http://127.0.0.1:8000/api/v1";

export async function getCoins() {
    const response = await fetch(`${BASE_URL}/coins/`, {
        method: "GET"
    });

    if (!response.ok) {
        throw new Error("Failed to fetch coins")
    }
    
    return await response.json();
}