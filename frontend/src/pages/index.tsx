'use client';

import React, { useState } from 'react';
import {
  Container,
  Typography,
  AppBar,
  Toolbar,
  Grid,
  Paper,
} from '@mui/material';
import LibraryMusicIcon from '@mui/icons-material/LibraryMusic';
import { AudioUpload } from '@/components/AudioUpload';
import { WaveformVisualizer } from '@/components/WaveformVisualizer';
import { ProcessingControls } from '@/components/ProcessingControls';
import { JobStatus } from '@/components/JobStatus';

export default function Home() {
  const [audioFileId, setAudioFileId] = useState<string | null>(null);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [jobId, setJobId] = useState<string | null>(null);

  const handleFileUpload = (fileData: any, file: File) => {
    setAudioFileId(fileData.id);
    setUploadedFile(file);
  };

  const handleJobCreated = (jobData: any) => {
    setJobId(jobData.id);
  };

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <LibraryMusicIcon sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Audio Processor
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Upload Audio
              </Typography>
              <AudioUpload onFileUpload={handleFileUpload} />
            </Paper>
          </Grid>

          <Grid item xs={12} md={6}>
            <JobStatus jobId={jobId ?? undefined} />
          </Grid>

          {audioFileId && (
            <Grid item xs={12}>
              <WaveformVisualizer audioFile={uploadedFile ?? undefined} />
            </Grid>
          )}

          {audioFileId && (
            <Grid item xs={12}>
              <ProcessingControls
                audioFileId={audioFileId}
                onJobCreated={handleJobCreated}
              />
            </Grid>
          )}
        </Grid>
      </Container>
    </>
  );
}
