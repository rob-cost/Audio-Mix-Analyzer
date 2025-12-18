import librosa
import numpy as np
import pyloudnorm as pyln
import pandas as pd
from scipy.signal import resample_poly
import io


def load_audio(audio_bytes, sr=None, mono= True):
    """
    Load audio once to avoid redundant I/O operations.
    
    Args:
        audio_bytes: bytes of audio file
        sr: sample rate (None for original)
        mono: whether to load as mono
    
    Returns:
        y: audio array
        sr: sample rate
    """
    audio_buffer = io.BytesIO(audio_bytes)
    y, sr = librosa.load(audio_buffer, sr=sr, mono=mono)
    return y, sr


def get_tempo_features (y, sr, onset_env=None):
    """
    Get tempo features

    Arguments: 
        y : mono audio 
        sr : sample rate
        onset_env

    Return: 
        Dictionary of tempo features

    """

    # Onset envelope
    # onset_env = librosa.onset.onset_strength(y=y, sr=sr)

    # Onset detection 
    if onset_env is None:
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)

    # --- OPTION 1 ---
    # Detect tempo using multiple methods for better accuracy
    # try:
    #     # Use autocorrelation-based tempo estimate
    #     tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr, aggregate=None)
    #     # Pick median as global tempo
    #     tempo_bpm = float(np.median(tempo))
    # except Exception:
    #     # Fallback
    #     tempo_bpm = 0.0

    # --- OPTION 2 ---
    # Detect tempo - let librosa aggregate internally
    try:
        tempo_bpm = float(librosa.beat.tempo(onset_envelope=onset_env, sr=sr)[0])
    except Exception:
        tempo_bpm = 0.0


    # Beat tracking
    try:
        _, beat_frames = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    except Exception:
        beat_times = np.array([])

    # Beat density per 30s section
    def beat_density_by_section(beat_times, section_length=30):
        if beat_times.size == 0:
            return {}
        max_t = np.max(beat_times)
        sections = int(np.ceil(max_t / section_length))
        density = {}
        for s in range(sections):
            start = s * section_length
            end = (s + 1) * section_length
            density[f"{start}-{end}s"] = int(((beat_times >= start) & (beat_times < end)).sum())
        return density

    section_density = beat_density_by_section(beat_times, 30)

    # Inter-beat interval stability
    ioi = np.diff(beat_times)
    tempo_std_s = float(np.std(ioi)) if len(ioi) > 0 else 0.0

    # Beat strengths
    beat_strengths = onset_env[beat_frames] if len(beat_frames) > 0 else []

    return {
        "tempo_bpm": tempo_bpm,
        "num_beats": int(len(beat_times)),
        "mean_beat_strength": float(np.mean(beat_strengths)) if len(beat_strengths) > 0 else 0.0,
        "tempo_std_s": tempo_std_s,
        "beat_density_per_30s": section_density,
    }


def get_loudness_features(y_stereo, sr): 
    """
    Get loudness features for given audio bytes.

    Arguments: 
        y_stereo : stereo audio
        sr : sample rate

    Returns: 
        Dictionary of loudness features
    """
    
    # Ensure stereo
    if y_stereo.ndim == 1:
        y_stereo = np.vstack([y_stereo, y_stereo])
    left, right = y_stereo

    mono = (left + right) / 2

    # Integrated LUFS
    meter = pyln.Meter(sr)
    loudness_lufs = meter.integrated_loudness(y_stereo.T)

    # RMS
    rms = np.sqrt(np.mean(mono**2))
    rms_db = 20 * np.log10(rms + 1e-12)

    # Dynamic range (400 ms blocks)
    block_size = int(sr * 0.4)
    n_blocks = len(mono) // block_size
    if n_blocks > 0:
        blocks = mono[:n_blocks * block_size].reshape(n_blocks, block_size)
        block_rms = np.sqrt(np.mean(blocks**2, axis=1))
        dynamic_range_db = 20 * np.log10(
            np.max(block_rms) / (np.min(block_rms) + 1e-12)
        )
    else:
        dynamic_range_db = 0.0

    # Peak
    peak = np.max(np.abs(mono))
    peak_db = 20 * np.log10(peak + 1e-12)

    # True peak (2× oversampling is enough for analysis)
    y_os = resample_poly(mono, 2, 1)
    true_peak = np.max(np.abs(y_os))
    true_peak_db = 20 * np.log10(true_peak + 1e-12)

    # Crest factor
    crest_factor_db = 20 * np.log10((peak / (rms + 1e-12)) + 1e-12)

    # Loudness evolution (30s RMS)
    section_len = int(sr * 30)
    loudness_evolution = [
        float(np.sqrt(np.mean(mono[i:i + section_len]**2)))
        for i in range(0, len(mono), section_len)
    ]

    return {
        "loudness_lufs": float(loudness_lufs),
        "rms_db": float(rms_db),
        "dynamic_range_db": float(dynamic_range_db),
        "peak_db": float(peak_db),
        "true_peak_db": float(true_peak_db),
        "crest_factor_db": float(crest_factor_db),
        "loudness_evolution": loudness_evolution,
    }


def get_transient_features(y, sr, max_duration = None, onset_env=None):
    """
    Fast transient analysis for audio bytes.
    
    Args:
        y: mono audio
        sr: sample rate
        max_duration: lenght of the audio
        onset_env
    
    Returns:
        Dictionary with essential transient features
    """

    if len(y) == 0:
        return {"transient_density": 0.0, "percussion_energy_pct": 0.0}

    total_duration = len(y) / sr

    # If audio is longer than max_duration, take the center segment
    if total_duration > max_duration:
        max_samples = int(max_duration * sr)
        start_idx = (len(y) - max_samples) // 2
        y = y[start_idx : start_idx + max_samples]

    duration_sec = len(y) / sr

    # Onset detection
    if onset_env is None:
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    onsets = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)
    transient_density = len(onsets) / duration_sec if duration_sec > 1e-6 else 0.0

    # Percussion energy
    y_perc = librosa.effects.percussive(y)
    total_energy = np.sum(y**2) + 1e-12
    percussion_energy_pct = float(np.sum(y_perc**2) / total_energy * 100)

    return {
        "transient_density": float(transient_density),
        "percussion_energy_pct": percussion_energy_pct
    }


def get_harmonic_content_features(y, sr): 

    """
    Analyse the harmonic content of an audio signal.

    Parameters: 
        y : mono audio
        sr : sample rate 22050 (optimal for harmonics analysis)

    Returns: Dictionary of harmonic content features

    """


    # Harmonic/Percussive source separation
    y_harm, y_perc = librosa.effects.hpss(y, kernel_size= 11)

    # Convert it into np array
    y_harm = np.asarray(y_harm)


    # --- OPTION 2 ---
    chroma = librosa.feature.chroma_stft(y=y_harm, sr=sr, n_fft=2048, hop_length=512)
    chroma_mean = chroma.mean(axis=1)


    # --- OPTION 2 ---
    key_index = np.argmax(chroma_mean)
    pitch_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    estimated_key = pitch_names[key_index]


    # Harmonic richness
    # S = np.abs(librosa.stft(y_harm, n_fft=2048))
    # spectral_centroid = librosa.feature.spectral_centroid(S=S, sr=sr) # calculate brigthness
    # spectral_bandwidth = librosa.feature.spectral_bandwidth(S=S, sr=sr)
    # spectral_contrast = librosa.feature.spectral_contrast(S=S, sr=sr) # calculate harmonic presence
    # spectral_rolloff = librosa.feature.spectral_rolloff(S=S, sr=sr)

    # Tonal stability
    chroma_std = chroma.std(axis=1)   # variability of each pitch class
    tonal_stability = 1 / (1 + chroma_std.mean())

    
    features = []
    features.append({
        # "harmonic_centroid": float(spectral_centroid.mean()),
        # "harmonic_bandwidth": float(spectral_bandwidth.mean()),
        # "harmonic_contrast": float(spectral_contrast.mean()),
        # "harmonic_rolloff": float(spectral_rolloff.mean()),
        "tonal_stability": float(tonal_stability),
        "estimated_key": estimated_key,
        # "chroma_mean": chroma_mean.tolist(),
    })
    return features[0]


def get_frequency_spectrum_energy(y, sr):
    """
    Calculate frequency spectrum energy across bands and spectral tilt.

    Args:
        y : mono audio
        sr: sample rate 

    Returns:
        Dictionary with normalized energy bands and spectral tilt.
    """

    if len(y) == 0:
        return {
            "energy_bands": {
                "Sub": 0.0,
                "Bass": 0.0,
                "Low_mids": 0.0,
                "Mids": 0.0,
                "High_mids": 0.0,
                "Air": 0.0
            },
            "spectral_tilt": 0.0
        }

    # FFT
    fft_complex = np.fft.rfft(y)
    magnitudes = np.abs(fft_complex)
    frequencies = np.fft.rfftfreq(len(y), 1.0 / sr)

    # Frequency bands
    bands = {
        "Sub": (20, 60),
        "Bass": (61, 200),
        "Low_mids": (201, 600),
        "Mids": (601, 3000),
        "High_mids": (3001, 8000),
        "Air": (8001, min(20000, sr//2))
    }

    energy_bands = {}
    for name, (f_low, f_high) in bands.items():
        # Ensure band is within frequency range
        f_high = min(f_high, sr/2)
        idx = np.where((frequencies >= f_low) & (frequencies <= f_high))[0]
        if len(idx) == 0:
            energy_bands[name] = 0.0
            continue

        # Energy = sum of squared magnitudes
        energy = np.sum(magnitudes[idx] ** 2)
        energy_bands[name] = float(energy)

    # Normalize energy so sum = 1
    total_energy = sum(energy_bands.values()) + 1e-12  # prevent divide by zero
    for k in energy_bands:
        energy_bands[k] /= total_energy

    # Spectral tilt: linear regression of log10(freq) vs magnitude
    safe_mags = magnitudes + 1e-12  # avoid log(0)
    freqs_nonzero = frequencies.copy()
    freqs_nonzero[freqs_nonzero == 0] = 1
    log_freqs = np.log10(freqs_nonzero)
    a, _ = np.polyfit(log_freqs, safe_mags, 1)
    spectral_tilt = float(a)

    return {
        "energy_bands": energy_bands,
        "spectral_tilt": spectral_tilt
    }


import numpy as np
import librosa

def get_stereo_imaging_features(y, sr, bands=None):
    """
    Analyze stereo imaging of an audio track with perceptual band weighting.

    Args:
        y: stereo or mono audio array
        sr: sample rate
        bands: dictionary of frequency bands (optional)
        
    Returns:
        Dictionary with stereo imaging metrics, including a perceptual
        stereo width score and label.
    """

    # --- Helper functions ---
    def clamp(x, lo=0.0, hi=1.0):
        return max(lo, min(hi, x))

    PERCEPTUAL_BAND_WEIGHTS = {
        "Sub": 0.05,
        "Bass": 0.1,
        "Low_mids": 0.25,
        "Mids": 0.4,
        "High_mids": 0.7,
        "Air": 0.9,
    }

    def perceptual_band_width(band_widths):
        weighted_sum = 0.0
        weight_total = 0.0
        for band, width in band_widths.items():
            w = PERCEPTUAL_BAND_WEIGHTS.get(band, 0.0)
            weighted_sum += w * width
            weight_total += w
        return weighted_sum / weight_total if weight_total > 0 else 0.0

    def stereo_width_score(ms_side_fraction, mean_frame_width, band_widths):
        # Use structural, temporal, and perceptual components
        band_component = perceptual_band_width(band_widths)
        score = (
            0.45 * clamp(ms_side_fraction * 5.0) +
            0.30 * clamp(mean_frame_width) +
            0.25 * clamp(band_component)
        )
        return clamp(score)

    def stereo_width_label(score):
        if score < 0.1:
            return "Mono / Very Narrow"
        elif score < 0.25:
            return "Narrow"
        elif score < 0.5:
            return "Balanced"
        elif score < 0.75:
            return "Wide"
        else:
            return "Very Wide"

    # --- Input validation ---
    if y is None or len(y) == 0:
        return {"error": "empty audio"}

    # Ensure stereo shape
    y = np.atleast_2d(y)
    if y.shape[0] == 1:
        y = np.vstack([y, y])
    elif y.shape[0] != 2:
        y = y.T
    left, right = y[0].astype(np.float64), y[1].astype(np.float64)

    # --- Mid/Side signals ---
    mid = (left + right) / 2
    side = (left - right) / 2

    mid_energy = float(np.sum(mid**2))
    side_energy = float(np.sum(side**2))
    ms_center_fraction = mid_energy / (mid_energy + side_energy + 1e-12)
    ms_side_fraction = side_energy / (mid_energy + side_energy + 1e-12)

    # --- Global correlation & LR balance ---
    rms_L, rms_R = np.sqrt(np.mean(left**2)), np.sqrt(np.mean(right**2))
    lr_balance = (rms_L - rms_R) / max(rms_L + rms_R, 1e-12)
    correlation = float(np.corrcoef(left, right)[0, 1]) if left.std() > 1e-12 and right.std() > 1e-12 else 1.0

    # --- STFT ---
    n_fft, hop_length = 1024, 512
    S_left = librosa.stft(left, n_fft=n_fft, hop_length=hop_length)
    S_right = librosa.stft(right, n_fft=n_fft, hop_length=hop_length)
    freqs = librosa.fft_frequencies(sr=sr, n_fft=n_fft)

    if bands is None:
        bands = {
            "Sub": (20, 60),
            "Bass": (61, 200),
            "Low_mids": (201, 600),
            "Mids": (601, 3000),
            "High_mids": (3001, 8000),
            "Air": (8001, min(sr // 2, 20000))
        }

    # --- Per-band stereo width ---
    S_mid = (S_left + S_right) / 2
    S_side = (S_left - S_right) / 2
    band_widths = {}

    for name, (f_low, f_high) in bands.items():
        mask = (freqs >= f_low) & (freqs <= f_high)
        if not np.any(mask):
            band_widths[name] = 0.0
            continue

        band_mid_energy = float(np.sum(np.abs(S_mid[mask, :])**2))
        band_side_energy = float(np.sum(np.abs(S_side[mask, :])**2))
        denom = band_mid_energy + band_side_energy
        band_widths[name] = band_side_energy / denom if denom > 1e-12 else 0.0

    # --- Frame-wise width ---
    frame_mid_rms = np.sqrt(np.mean(np.abs(S_mid)**2, axis=0))
    frame_side_rms = np.sqrt(np.mean(np.abs(S_side)**2, axis=0))
    frame_width = frame_side_rms / (frame_mid_rms + frame_side_rms + 1e-12)
    mean_frame_width, std_frame_width = float(np.mean(frame_width)), float(np.std(frame_width))

    # --- Compute stereo width score & label ---
    width_score = stereo_width_score(ms_side_fraction, mean_frame_width, band_widths)
    width_label = stereo_width_label(width_score)

    return {
        # Core stereo image metrics (for final report)
        "stereo_width_score": width_score,
        "stereo_width_label": width_label,
        "ms_side_fraction": ms_side_fraction,
        "correlation": float(correlation),
        "lr_balance": float(lr_balance),

        # Advanced / optional metrics (for detailed tabs)
        "band_widths": band_widths,
        "mean_frame_width": mean_frame_width,
        "std_frame_width": std_frame_width
    }



