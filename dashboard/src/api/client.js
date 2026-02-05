import axios from 'axios';

// CHANGE THIS URL if using Codespaces (check your Ports tab!)
const API_BASE_URL = 'https://silver-space-giggle-pgg9rpj57v4frwrr-8000.app.github.dev';

export const api = {
  getSalesSummary: () => axios.get(`${API_BASE_URL}/api/sales/summary`),
  getTopBeers: (limit = 5) => axios.get(`${API_BASE_URL}/api/beers/top?limit=${limit}`),
  getBreweryPerformance: () => axios.get(`${API_BASE_URL}/api/breweries/performance`),
  getDailySales: () => axios.get(`${API_BASE_URL}/api/sales/daily`)
}