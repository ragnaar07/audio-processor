"""
DSP Audio Processing Engine

Implements various digital signal processing filters and audio processing algorithms.
"""

import numpy as np
from scipy import signal
from scipy.fft import fft, fftfreq
import soundfile as sf
from typing import Tuple, Dict, Any


class AudioProcessor:
    """Core audio processing engine."""
    
    def __init__(self, audio_path: str):
        """
        Initialize audio processor.
        
        Args:
            audio_path: Path to audio file
        """
        self.audio_data, self.sample_rate = sf.read(audio_path)
        if len(self.audio_data.shape) > 1:
            self.audio_data = np.mean(self.audio_data, axis=1)  # Convert to mono
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get audio metadata."""
        return {
            'sample_rate': self.sample_rate,
            'duration': len(self.audio_data) / self.sample_rate,
            'num_samples': len(self.audio_data),
        }
    
    # ============ Filter Implementations ============
    
    def apply_lowpass_filter(self, cutoff_freq: float, order: int = 5) -> np.ndarray:
        """
        Apply low-pass filter.
        
        Args:
            cutoff_freq: Cutoff frequency in Hz
            order: Filter order
        
        Returns:
            Filtered audio
        """
        nyquist = self.sample_rate / 2
        normal_cutoff = cutoff_freq / nyquist
        b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
        return signal.filtfilt(b, a, self.audio_data)
    
    def apply_highpass_filter(self, cutoff_freq: float, order: int = 5) -> np.ndarray:
        """Apply high-pass filter."""
        nyquist = self.sample_rate / 2
        normal_cutoff = cutoff_freq / nyquist
        b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
        return signal.filtfilt(b, a, self.audio_data)
    
    def apply_bandpass_filter(
        self,
        low_freq: float,
        high_freq: float,
        order: int = 5
    ) -> np.ndarray:
        """Apply band-pass filter."""
        nyquist = self.sample_rate / 2
        low = low_freq / nyquist
        high = high_freq / nyquist
        b, a = signal.butter(order, [low, high], btype='band', analog=False)
        return signal.filtfilt(b, a, self.audio_data)
    
    def apply_notch_filter(
        self,
        center_freq: float,
        quality: float = 30.0
    ) -> np.ndarray:
        """
        Apply notch filter.
        
        Args:
            center_freq: Center frequency in Hz
            quality: Quality factor
        
        Returns:
            Filtered audio
        """
        b, a = signal.iirnotch(center_freq, quality, self.sample_rate)
        return signal.filtfilt(b, a, self.audio_data)
    
    def apply_fir_filter(self, num_taps: int = 101) -> np.ndarray:
        """
        Apply FIR low-pass filter.
        
        Args:
            num_taps: Number of filter taps
        
        Returns:
            Filtered audio
        """
        cutoff = 0.3  # Normalized cutoff frequency
        h = signal.firwin(num_taps, cutoff)
        return signal.convolve(self.audio_data, h, mode='same')
    
    def apply_iir_filter(self, cutoff_freq: float = 5000) -> np.ndarray:
        """
        Apply IIR low-pass filter.
        
        Args:
            cutoff_freq: Cutoff frequency in Hz
        
        Returns:
            Filtered audio
        """
        return self.apply_lowpass_filter(cutoff_freq)
    
    # ============ Noise Reduction ============
    
    def apply_noise_reduction(self, noise_duration: float = 1.0) -> np.ndarray:
        """
        Simple noise reduction using spectral subtraction.
        
        Args:
            noise_duration: Duration of noise profile in seconds
        
        Returns:
            Denoised audio
        """
        noise_frames = int(noise_duration * self.sample_rate)
        noise_profile = self.audio_data[:noise_frames]
        
        # Compute noise spectrum
        noise_fft = np.abs(fft(noise_profile))
        
        # Apply spectral subtraction
        output = self.audio_data.copy()
        frame_size = len(noise_profile)
        
        for i in range(0, len(output) - frame_size, frame_size // 2):
            frame = output[i:i + frame_size]
            frame_fft = fft(frame)
            
            # Subtract noise spectrum
            magnitude = np.abs(frame_fft)
            magnitude = np.maximum(magnitude - noise_fft, 0)
            phase = np.angle(frame_fft)
            
            # Reconstruct
            output[i:i + frame_size] = np.real(
                np.fft.ifft(magnitude * np.exp(1j * phase))
            )
        
        return output
    
    # ============ Analysis ============
    
    def get_fft_analysis(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Perform FFT analysis.
        
        Returns:
            Tuple of (frequencies, magnitudes)
        """
        fft_result = fft(self.audio_data)
        frequencies = fftfreq(len(self.audio_data), 1 / self.sample_rate)
        magnitudes = np.abs(fft_result)
        
        # Return only positive frequencies
        positive_freq_idx = frequencies > 0
        return frequencies[positive_freq_idx], magnitudes[positive_freq_idx]
    
    def save_audio(self, output_path: str, audio_data: np.ndarray) -> None:
        """Save processed audio to file."""
        sf.write(output_path, audio_data, self.sample_rate)


# ============ Filter Presets ============

class FilterPresets:
    """Predefined filter configurations."""
    
    @staticmethod
    def telephony_filter(audio_processor: AudioProcessor) -> np.ndarray:
        """Filter audio for telephony (300-3400 Hz)."""
        return audio_processor.apply_bandpass_filter(300, 3400)
    
    @staticmethod
    def treble_boost(audio_processor: AudioProcessor, amount: float = 1.2) -> np.ndarray:
        """Boost high frequencies."""
        # High-pass filter at 2kHz
        filtered = audio_processor.apply_highpass_filter(2000)
        return audio_processor.audio_data + amount * (filtered - audio_processor.audio_data)
    
    @staticmethod
    def bass_reduction(audio_processor: AudioProcessor) -> np.ndarray:
        """Reduce low frequencies."""
        return audio_processor.apply_highpass_filter(100)
