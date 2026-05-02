'use client';

import React, { useRef, useEffect, useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  CircularProgress,
  Alert,
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { useAudioUpload } from '@/hooks/useAudioUpload';

interface AudioUploadProps {
  onFileUpload?: (fileData: any, file: File) => void;
}

export const AudioUpload: React.FC<AudioUploadProps> = ({ onFileUpload }) => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { uploadAudio, loading, error } = useAudioUpload();
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(e.type !== 'dragleave');
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const files = e.dataTransfer.files;
    if (files && files[0]) {
      await handleFileUpload(files[0]);
    }
  };

  const handleFileUpload = async (file: File) => {
    try {
      const result = await uploadAudio(file);
      if (onFileUpload) {
        onFileUpload(result, file);
      }
    } catch (err) {
      console.error('Upload failed:', err);
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) {
      handleFileUpload(e.target.files[0]);
    }
  };

  return (
    <Box>
      <Paper
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        sx={{
          p: 4,
          textAlign: 'center',
          cursor: 'pointer',
          backgroundColor: dragActive ? '#f5f5f5' : '#fafafa',
          border: '2px dashed #ccc',
          borderRadius: 2,
          transition: 'all 0.3s',
          '&:hover': {
            borderColor: '#999',
            backgroundColor: '#f5f5f5',
          },
        }}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="audio/*"
          onChange={handleFileSelect}
          style={{ display: 'none' }}
        />

        {loading ? (
          <CircularProgress />
        ) : (
          <>
            <CloudUploadIcon sx={{ fontSize: 48, color: '#1976d2', mb: 2 }} />
            <Typography variant="h6" gutterBottom>
              Drag and drop your audio file here
            </Typography>
            <Typography variant="body2" color="textSecondary" gutterBottom>
              or
            </Typography>
            <Button
              variant="contained"
              onClick={handleClick}
              sx={{ mt: 1 }}
            >
              Select File
            </Button>
            <Typography variant="caption" display="block" sx={{ mt: 2 }}>
              Supported formats: MP3, WAV, FLAC, OGG
            </Typography>
          </>
        )}
      </Paper>

      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}
    </Box>
  );
};
