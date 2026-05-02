'use client';

import { useState, useCallback } from 'react';
import { audioApi } from '@/services/api';

export const useAudioUpload = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [file, setFile] = useState<File | null>(null);

  const uploadAudio = useCallback(async (audioFile: File) => {
    setLoading(true);
    setError(null);
    try {
      const response = await audioApi.uploadAudio(audioFile);
      setFile(audioFile);
      return response.data;
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to upload audio';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { uploadAudio, loading, error, file };
};
