'use client';

import React, { useEffect, useRef, useState } from 'react';
import { Box, Paper, Typography } from '@mui/material';

interface WaveformVisualizerProps {
  audioUrl?: string;
  audioFile?: File;
}

export const WaveformVisualizer: React.FC<WaveformVisualizerProps> = ({
  audioUrl,
  audioFile,
}) => {
  const waveformRef = useRef<HTMLDivElement>(null);
  const wavesurferRef = useRef<any>(null);
  const [wavesurferReady, setWavesurferReady] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!waveformRef.current) return;

    let cancelled = false;

    import('wavesurfer.js').then(({ default: WaveSurfer }) => {
      if (cancelled || !waveformRef.current) return;

      const wavesurfer = WaveSurfer.create({
        container: waveformRef.current,
        waveColor: '#4f81bd',
        progressColor: '#1976d2',
        height: 128,
        barWidth: 2,
        barRadius: 3,
        barGap: 2,
      });

      wavesurferRef.current = wavesurfer;
      setWavesurferReady(true);
    });

    return () => {
      cancelled = true;
      wavesurferRef.current?.destroy();
      wavesurferRef.current = null;
      setWavesurferReady(false);
    };
  }, []);

  useEffect(() => {
    const wavesurfer = wavesurferRef.current;
    if (!wavesurfer || !wavesurferReady) return;

    setLoading(true);

    if (audioFile) {
      const objectUrl = URL.createObjectURL(audioFile);
      wavesurfer.load(objectUrl);
      wavesurfer.once('ready', () => {
        URL.revokeObjectURL(objectUrl);
        setLoading(false);
      });
    } else if (audioUrl) {
      wavesurfer.load(audioUrl);
      wavesurfer.once('ready', () => setLoading(false));
    } else {
      setLoading(false);
    }
  }, [audioFile, audioUrl, wavesurferReady]);

  return (
    <Paper sx={{ p: 2 }}>
      <Typography variant="subtitle2" gutterBottom>
        Waveform
      </Typography>
      <Box
        ref={waveformRef}
        sx={{
          opacity: loading ? 0.5 : 1,
          transition: 'opacity 0.3s',
        }}
      />
    </Paper>
  );
};
