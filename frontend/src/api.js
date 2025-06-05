import axios from 'axios';

const api = axios.create({//here api
  baseURL: 'http://zawodev.ddns.net:8000/api/v2'
});

export default api;