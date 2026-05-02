'use client';

import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  FormControlLabel,
  Checkbox,
  Button,
  Alert,
  CircularProgress,
} from '@mui/material';
import { useProcessingJob } from '@/hooks/useProcessingJob';

interface ProcessingControlsProps {
  audioFileId?: string;
  onJobCreated?: (jobData: any) => void;
}

export const ProcessingControls: React.FC<ProcessingControlsProps> = ({
  audioFileId,
  onJobCreated,
}) => {
  const [filterType, setFilterType] = useState<string>('lowpass');
  const [filterParams, setFilterParams] = useState<string>('{"cutoff_freq": 5000}');
  const [applyNoiseReduction, setApplyNoiseReduction] = useState(false);
  const { createJob, loading, error } = useProcessingJob();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!audioFileId) {
      alert('Please upload an audio file first');
      return;
    }

    try {
      const jobData = {
        audio_file_id: audioFileId,
        filter_type: filterType,
        filter_params: filterParams,
        apply_noise_reduction: applyNoiseReduction,
      };

      const result = await createJob(jobData);
      if (onJobCreated) {
        onJobCreated(result);
      }
    } catch (err) {
      console.error('Job creation failed:', err);
    }
  };

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        Processing Options
      </Typography>

      <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        <FormControl fullWidth>
          <InputLabel>Filter Type</InputLabel>
          <Select
            value={filterType}
            label="Filter Type"
            onChange={(e) => setFilterType(e.target.value)}
          >
            <MenuItem value="lowpass">Low Pass</MenuItem>
            <MenuItem value="highpass">High Pass</MenuItem>
            <MenuItem value="bandpass">Band Pass</MenuItem>
            <MenuItem value="notch">Notch</MenuItem>
            <MenuItem value="fir">FIR</MenuItem>
            <MenuItem value="iir">IIR</MenuItem>
          </Select>
        </FormControl>

        <TextField
          label="Filter Parameters (JSON)"
          multiline
          rows={4}
          value={filterParams}
          onChange={(e) => setFilterParams(e.target.value)}
          fullWidth
          placeholder='{"cutoff_freq": 5000}'
        />

        <FormControlLabel
          control={
            <Checkbox
              checked={applyNoiseReduction}
              onChange={(e) => setApplyNoiseReduction(e.target.checked)}
            />
          }
          label="Apply Noise Reduction"
        />

        <Button
          variant="contained"
          type="submit"
          disabled={loading || !audioFileId}
          sx={{ mt: 2 }}
        >
          {loading ? <CircularProgress size={24} /> : 'Process Audio'}
        </Button>

        {error && <Alert severity="error">{error}</Alert>}
      </Box>
    </Paper>
  );
};
