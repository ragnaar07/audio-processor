'use client';

import React, { useEffect, useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  LinearProgress,
  Alert,
  Button,
  CircularProgress,
} from '@mui/material';
import { jobsApi } from '@/services/api';

interface JobStatusProps {
  jobId?: string;
}

export const JobStatus: React.FC<JobStatusProps> = ({ jobId }) => {
  const [job, setJob] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!jobId) return;
    let cancelled = false;
    let timeoutId: ReturnType<typeof setTimeout> | undefined;

    const fetchJob = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await jobsApi.getJob(jobId);
        if (cancelled) return;
        setJob(response.data);
        if (!['completed', 'failed'].includes(response.data.status)) {
          timeoutId = setTimeout(fetchJob, 2000);
        }
      } catch (err: any) {
        if (cancelled) return;
        setError(err.response?.data?.detail || 'Failed to fetch job status');
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    fetchJob();

    return () => {
      cancelled = true;
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
    };
  }, [jobId]);

  if (!jobId) {
    return (
      <Paper sx={{ p: 3 }}>
        <Typography variant="body2" color="textSecondary">
          Create a job to see status
        </Typography>
      </Paper>
    );
  }

  if (loading && !job) {
    return (
      <Paper sx={{ p: 3, textAlign: 'center' }}>
        <CircularProgress />
      </Paper>
    );
  }

  if (error) {
    return (
      <Alert severity="error">{error}</Alert>
    );
  }

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        Processing Status
      </Typography>

      {job && (
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Box>
            <Typography variant="body2" color="textSecondary">
              Status: <strong>{job.status}</strong>
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Progress:
            </Typography>
            <LinearProgress
              variant="determinate"
              value={job.progress}
              sx={{ mt: 1 }}
            />
            <Typography variant="caption" display="block" sx={{ mt: 1 }}>
              {job.progress}%
            </Typography>
          </Box>

          {job.error_message && (
            <Alert severity="error">{job.error_message}</Alert>
          )}

          {job.status === 'completed' && job.output_file_path && (
            <Alert severity="success">
              Processing completed.
            </Alert>
          )}

          {job.status === 'completed' && job.output_file_path && (
            <Button
              variant="contained"
              href={jobsApi.getDownloadUrl(job.id)}
              download
            >
              Download Processed Audio
            </Button>
          )}
        </Box>
      )}
    </Paper>
  );
};
