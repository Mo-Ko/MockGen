import axios from 'axios';

export async function generateApi(formData) {
  const res = await axios.post('/generate', formData);
  return res.data;
}

export async function getHistory(params = {}) {
  // Optionally accept params for flexibility
  const res = await axios.get('/history', { params });
  return res.data;
}

export async function checkHealth() {
  const res = await axios.get('/health');
  return res.data;
} 