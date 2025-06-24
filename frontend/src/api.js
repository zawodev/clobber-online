import axios from 'axios';

const api = axios.create({//here api
  baseURL: process.env.VUE_APP_API
});


export default api;