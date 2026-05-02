'use client';

import { useState, useCallback } from 'react';
import { jobsApi } from '@/services/api';

export const useProcessingJob = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createJob = useCallback(async (jobData: any) => {
    setLoading(true);
    setError(null);
    try {
      const response = await jobsApi.createJob(jobData);
      return response.data;
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to create job';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const getJob = useCallback(async (jobId: string) => {
    setLoading(true);
    setError(null);
    try {
      const response = await jobsApi.getJob(jobId);
      return response.data;
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to fetch job';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { createJob, getJob, loading, error };
};
