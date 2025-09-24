import axios from 'axios';

const api = axios.create({
	baseURL: import.meta.env.VITE_API_BASE || 'http://localhost:8000',
	withCredentials: false,
});

api.interceptors.request.use((config) => {
	const token = localStorage.getItem('access');
	if (token) {
		config.headers = config.headers || {};
		config.headers['Authorization'] = `Bearer ${token}`;
	}
	return config;
});

api.interceptors.response.use(
	(resp) => resp,
	async (error) => {
		const original = error.config;
		if (error.response && error.response.status === 401 && !original._retry) {
			original._retry = true;
			const refresh = localStorage.getItem('refresh');
			if (refresh) {
				try {
					const r = await axios.post(`${api.defaults.baseURL}/api/auth/token/refresh/`, { refresh });
					localStorage.setItem('access', r.data.access);
					original.headers['Authorization'] = `Bearer ${r.data.access}`;
					return api(original);
				} catch (e) {
					localStorage.removeItem('access');
					localStorage.removeItem('refresh');
				}
			}
		}
		return Promise.reject(error);
	}
);

export default api;
