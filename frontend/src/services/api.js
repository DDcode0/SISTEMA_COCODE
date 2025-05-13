


// src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL,  // ya no VITE_, sino REACT_APP_
});

export default api;



