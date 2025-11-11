import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  googleLogin: (token) => api.post('/auth/google-login', { token }),
  login: (email, password) => api.post('/auth/login', { email, password }),
};

export const userAPI = {
  getMe: () => api.get('/user/me'),
  getDetails: () => api.get('/user/details'),
  updateDetails: (data) => api.put('/user/details', data),
};

export const qrAPI = {
  createQR: (data) => api.post('/qr/create', data),
  scanQR: (qrId, latitude, longitude) => 
    api.get(`/qr/scan/${qrId}`, { params: { latitude, longitude } }),
  getQRDetails: (qrId) => api.get(`/qr/details/${qrId}`),
  updatePermissions: (qrId, data) => api.put(`/qr/update-permissions/${qrId}`, data),
  bindQR: (qrId) => api.put(`/qr/bind/${qrId}`),
  getMyQRCodes: () => api.get('/qr/my-qr-codes'),
};

export default api;

