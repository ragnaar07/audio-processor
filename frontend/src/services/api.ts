import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const audioApi = {
  uploadAudio: (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return apiClient.post('/api/audio/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },

  getAudioFile: (fileId: string) => apiClient.get(`/api/audio/${fileId}`),
};

export const jobsApi = {
  createJob: (jobData: any) => apiClient.post('/api/jobs/', jobData),
  getJob: (jobId: string) => apiClient.get(`/api/jobs/${jobId}`),
  getDownloadUrl: (jobId: string) => `${API_BASE_URL}/api/jobs/${jobId}/download`,
  listJobs: (skip = 0, limit = 10) => 
    apiClient.get('/api/jobs/', { params: { skip, limit } }),
};

export const healthApi = {
  check: () => apiClient.get('/health'),
};
