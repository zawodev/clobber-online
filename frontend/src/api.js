import axios from 'axios';

const api = axios.create({//here api
  baseURL: 'http://localhost:8000/api/v2'
});


export default api;