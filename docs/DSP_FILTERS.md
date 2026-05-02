# DSP Filters & Audio Processing

## Overview

The DSP Engine implements industry-standard digital signal processing algorithms for audio filtering and analysis.

## Implemented Filters

### 1. Butterworth Filters

#### Low-Pass Filter
Attenuates high frequencies above cutoff frequency.

**Parameters**:
- `cutoff_freq`: Cutoff frequency (Hz)
- `order`: Filter order (higher = steeper rolloff)

**Use Cases**:
- Noise reduction
- Removing high-frequency artifacts
- Anti-aliasing

**Example**:
```json
{
  "filter_type": "lowpass",
  "filter_params": "{\"cutoff_freq\": 5000, \"order\": 5}"
}
```

#### High-Pass Filter
Attenuates low frequencies below cutoff frequency.

**Parameters**:
- `cutoff_freq`: Cutoff frequency (Hz)
- `order`: Filter order

**Use Cases**:
- Removing DC offset
- Eliminating low-frequency rumble
- Bass reduction

**Example**:
```json
{
  "filter_type": "highpass",
  "filter_params": "{\"cutoff_freq\": 100, \"order\": 5}"
}
```

#### Band-Pass Filter
Allows frequencies within a band to pass through.

**Parameters**:
- `low_freq`: Lower cutoff frequency (Hz)
- `high_freq`: Upper cutoff frequency (Hz)
- `order`: Filter order

**Use Cases**:
- Telephony filtering (300-3400 Hz)
- Isolating specific frequency ranges
- Instrument isolation

**Example**:
```json
{
  "filter_type": "bandpass",
  "filter_params": "{\"low_freq\": 300, \"high_freq\": 3400, \"order\": 5}"
}
```

### 2. Notch Filter (IIR Notch)
Attenuates a specific frequency (narrow band).

**Parameters**:
- `center_freq`: Center frequency to attenuate (Hz)
- `quality`: Quality factor (higher = narrower notch)

**Use Cases**:
- Removing 50/60 Hz hum
- Eliminating single-frequency interference
- Power line noise removal

**Example**:
```json
{
  "filter_type": "notch",
  "filter_params": "{\"center_freq\": 60, \"quality\": 30}"
}
```

### 3. FIR Filter (Finite Impulse Response)
Non-recursive filter with linear phase response.

**Parameters**:
- `num_taps`: Number of filter coefficients (higher = better frequency response)

**Advantages**:
- Linear phase (no phase distortion)
- Always stable
- No feedback

**Disadvantages**:
- Requires more computation
- Longer filter order needed for steep rolloff

**Example**:
```json
{
  "filter_type": "fir",
  "filter_params": "{\"num_taps\": 101}"
}
```

### 4. IIR Filter (Infinite Impulse Response)
Recursive filter with feedback.

**Parameters**:
- `cutoff_freq`: Cutoff frequency (Hz)

**Advantages**:
- Computationally efficient
- Achieves steeper rolloff with lower order

**Disadvantages**:
- Can have phase distortion
- Potential stability issues

**Example**:
```json
{
  "filter_type": "iir",
  "filter_params": "{\"cutoff_freq\": 5000}"
}
```

## Noise Reduction

### Spectral Subtraction
Simple but effective noise reduction algorithm.

**How it works**:
1. Estimate noise spectrum from silent portion of audio
2. Subtract noise spectrum from each frame
3. Reconstruct audio using inverse FFT

**Limitations**:
- Works best with stationary noise
- May introduce artifacts ("musical noise")
- Assumes noise is predictable

**Parameters**:
- `noise_duration`: Length of noise profile (seconds)

## FFT Analysis

Performs Fast Fourier Transform for frequency domain analysis.

**Output**:
- Frequencies (Hz)
- Magnitudes (amplitude)

**Use Cases**:
- Spectral visualization
- Frequency analysis
- Peak detection

## Filter Design Recommendations

| Use Case | Recommended Filter | Parameters |
|----------|-------------------|-----------|
| Voice Enhancement | Band-pass | 300-3400 Hz, order=4 |
| 50/60 Hz Hum | Notch | center=50 or 60, Q=30 |
| Bass Reduction | High-pass | cutoff=100-200, order=5 |
| Treble Boost | High-pass | cutoff=2000, order=3 |
| General Cleanup | Low-pass | cutoff=8000-12000, order=5 |
| Music Production | Low-pass | cutoff=15000-20000, order=2 |

## Audio Processing Pipeline

```
Input Audio
    ↓
[Preprocessing: Normalize, Handle DC offset]
    ↓
[Filtering: Apply selected filter]
    ↓
[Noise Reduction: Optional spectral subtraction]
    ↓
[FFT Analysis: Extract frequency information]
    ↓
[Normalization: Prevent clipping]
    ↓
Output Audio
```

## Implementation Details

### Frequency Characteristics

**Butterworth Filter Response**:
- Maximally flat passband
- Monotonic rolloff in stopband
- -3dB point at cutoff frequency
- Rolloff rate: 20*N dB/decade (N = filter order)

**FIR Filter**:
- Linear phase
- No feedback
- Requires higher order for sharp cutoff

**Notch Filter**:
- Sharp attenuation at center frequency
- Quality factor determines sharpness
- Q = center_freq / bandwidth

## Performance Considerations

| Filter Type | Computation | Latency | Notes |
|------------|------------|---------|-------|
| Butterworth (IIR) | Low | Very Low | Real-time capable |
| FIR | Medium | Medium | Linear phase advantage |
| Notch | Very Low | Very Low | Highly efficient |

## Future Enhancements

- [ ] Parametric EQ (multiple band control)
- [ ] Dynamic range compression
- [ ] Advanced noise reduction (AI-based)
- [ ] Adaptive filtering
- [ ] Real-time convolution reverb
- [ ] Multiband processing

## References

- Butterworth Filter Design: [SciPy Documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.butter.html)
- FFT Analysis: [NumPy FFT](https://numpy.org/doc/stable/reference/routines.fft.html)
- Spectral Subtraction: [IEEE Paper](https://ieeexplore.ieee.org/)
