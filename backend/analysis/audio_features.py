import librosa
import numpy as np
import pyloudnorm as pyln
import pandas as pd
from scipy.signal import resample_poly
import io


def get_tempo_features (audio_bytes, sr=None):
    """
    Get tempo features

    Arguments: 
        audio_bytes : bytes of audio file, 
        sr : sample rate (None for original)

    Return: 
        Dictionary of tempo features
    """
    
    # Load audio
    audio_buffer = io.BytesIO(audio_bytes)
    y, sr = librosa.load(audio_buffer, sr=sr, mono=True)

    # Onset envelope
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)

    # Detect tempo using multiple methods for better accuracy
    try:
        # Use autocorrelation-based tempo estimate
        tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr, aggregate=None)
        # Pick median as global tempo
        tempo_bpm = float(np.median(tempo))
    except Exception:
        # Fallback
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


def get_loudness_features(audio_bytes, sr=None): 
    """
    Get loudness features for given audio bytes.

    Arguments: 
        audio_bytes : bytes of audio file
        sr : sample rate (None for original)

    Returns: 
        Dictionary of loudness features
    """

    # Load audio file (keep stereo)
    audio_buffer = io.BytesIO(audio_bytes)
    y, sr = librosa.load(audio_buffer, sr=sr, mono=False)
    
    # Ensure stereo
    if y.ndim == 1:
        y = np.vstack([y, y])
    left, right = y

    # Mono signal for integrated loudness & peak calculation
    mono = (left + right) / 2

    # --- Integrated Loudness (LUFS) ---
    meter = pyln.Meter(sr)  # Creates LUFS meter
    stereo_signal = y.T  # shape: (samples, channels)
    loudness_lufs = meter.integrated_loudness(stereo_signal)

    # --- RMS ---
    rms = np.sqrt(np.mean(mono**2))
    rms_db = 20 * np.log10(rms + 1e-12) 

    # --- RMS per frame ---
    rms_frame = librosa.feature.rms(y=mono, frame_length=2048, hop_length=512)[0]

    # --- Dynamic Range ---
    dynamic_range = float(np.max(rms_frame) - np.min(rms_frame))

    # --- Peak amplitude ---
    peak = np.max(np.abs(mono))
    peak_db = 20 * np.log10(peak + 1e-12)

    # --- True Peak ---
    upsample = 4  # 4× oversampling
    y_os = resample_poly(mono, upsample, 1)
    true_peak = np.max(np.abs(y_os))
    true_peak_db = 20 * np.log10(true_peak + 1e-12)

    # --- Crest Factor ---
    crest_factor = peak / (rms + 1e-12)

    # --- Loudness evolution (per 30s section) ---
    section_length_sec = 30
    frame_len = sr * section_length_sec
    num_sections = int(np.ceil(len(mono) / frame_len))

    section_rms = [
        float(np.sqrt(np.mean(mono[int(i*frame_len):int(min((i+1)*frame_len, len(mono))) ]**2)))
        for i in range(num_sections)
    ]

    # --- Collect features ---
    features = {
        "loudness_lufs": float(loudness_lufs),
        "rms_db": float(rms_db),
        "dynamic_range": float(dynamic_range),
        "peak_db": float(peak_db),
        "true_peak_db": float(true_peak_db),
        "crest_factor": float(crest_factor),
        "loudness_evolution": section_rms
    }

    return features


def get_transient_features(audio_bytes, sr=None):
    """
    Fast transient analysis for audio bytes.
    
    Args:
        audio_bytes: bytes of audio file
        sr: sample rate (None to keep original)
    
    Returns:
        Dictionary with essential transient features
    """

    # Load mono audio
    audio_buffer = io.BytesIO(audio_bytes)
    y, sr = librosa.load(audio_buffer, sr=sr, mono=True)

    if len(y) == 0:
        return {
            "transient_density": 0.0,
            "percussion_energy_pct": 0.0
        }

    duration_sec = len(y) / sr

    # Onset detection 
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


def get_harmonic_content_features(audio_bytes, sr=None):

    """
    Analyse the harmonic content of an audio signal.

    Parameters: audio_bytes : bytes of audio file, sr : sample rate (None for original)

    Returns: Dictionary of harmonic content features

    """

    # Load audio file
    audio_buffer = io.BytesIO(audio_bytes)
    y, sr = librosa.load(audio_buffer, sr=sr, mono=True)

    # Harmonic/Percussive source separation
    y_harm, _ = librosa.effects.hpss(y)

    C = librosa.cqt(y_harm, sr=sr, bins_per_octave=36, n_bins=7*36)
    chroma = librosa.feature.chroma_cqt(C=C, sr=sr)


    chroma_mean = chroma.mean(axis=1)
    key_index = np.argmax(chroma_mean)
    pitch_names = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
    estimated_key = pitch_names[key_index]

    # Harmonic richness
    spectral_centroid = librosa.feature.spectral_centroid(y=y_harm, sr=sr)  # calculate brightness
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y_harm, sr=sr)
    spectral_contrast = librosa.feature.spectral_contrast(y=y_harm, sr=sr) # calculate amount of harmonics presence
    harmonic_rolloff = librosa.feature.spectral_rolloff(y=y_harm, sr=sr)    

    # Tonal stability
    chroma_std = chroma.std(axis=1)   # variability of each pitch class
    tonal_stability = 1 / (1 + chroma_std.mean())

    
    features = []
    features.append({
        "harmonic_centroid": float(spectral_centroid.mean()),
        "harmonic_bandwidth": float(spectral_bandwidth.mean()),
        "harmonic_contrast": float(spectral_contrast.mean()),
        "harmonic_rolloff": float(harmonic_rolloff.mean()),
        "tonal_stability": float(tonal_stability),
        "estimated_key": estimated_key,
        "chroma_mean": chroma_mean.tolist(),
    })
    return features[0]


def get_frequency_spectrum_energy(audio_bytes, sr=None):

    # Load audio file
    audio_buffer = io.BytesIO(audio_bytes)
    y, sr = librosa.load(audio_buffer, sr=sr, mono=True)
    # Compute FFT
    fft_complex = np.fft.rfft(y)

    # Magnitude spectrum
    magnitudes = np.abs(fft_complex)

    # Frequency array (same shape as magnitudes)
    frequencies = np.fft.rfftfreq(len(y), 1.0 / sr)
    
    # Calculate frequency spectrum energy
    # Frequency bands energy
    bands = {
        "Sub": (20, 60),
        "Bass": (61, 200),
        "Low_mids": (201, 600),
        "Mids": (601, 3000),
        "High_mids": (3001, 8000),  
        "Air": (8001 ,20000)
    }

    try:
        energy_bands = {}

        for name, (f_low, f_high) in bands.items():
            # find frequency bins inside the band
            idx = np.where((frequencies >= f_low) & (frequencies <= f_high))[0]
            
            if len(idx) == 0:
                energy_bands[name] = 0.0
                continue

            # energy = sum of squared magnitudes inside band
            energy = np.sum(magnitudes[idx] ** 2)
            energy_bands[name] = float(energy)

        # normalize so bands sum to 1 (percentage of total energy)
        total_energy = sum(energy_bands.values())
        if total_energy > 0:
            for k in energy_bands:
                energy_bands[k] = energy_bands[k] / total_energy

    except Exception as e:
        print(f"energy band calculation failed: {e}")

    
    # Spectral tilt
    freqs = frequencies.copy()
    freqs[freqs == 0] = 1  
    log_freqs = np.log10(freqs)
    a, b = np.polyfit(log_freqs, magnitudes, 1)
    spectral_tilt = float(a)

    return {
        "energy_bands": energy_bands,
        "spetral_tilt": spectral_tilt,
    }


def get_stereo_imaging_features(audio_bytes, sr=None, bands=None, n_fft=2048, hop_length=1024):
    """

    Analyze the stereo imaging of the track
    
    Returns: Dicitonary with imaging metrics.

    """
    # Load audio file
    audio_buffer = io.BytesIO(audio_bytes)
    y, sr = librosa.load(audio_buffer, sr=sr, mono=False)

    # Default bands
    if bands is None:
        bands = {
            "Sub": (20, 60),
            "Bass": (61, 200),
            "Low_mids": (201, 600),
            "Mids": (601, 3000),
            "High_mids": (3001, 8000),
            "Air": (8001, min(sr//2, 20000))
        }

    # Accept (n,2) or (2,n)
    if y is None or len(y) == 0:
        return {"error": "empty audio"}

    y = np.asarray(y)
    if y.ndim == 1:
        # mono -> duplicate to make stereo (so metrics are defined)
        y = np.vstack([y, y])
    elif y.ndim == 2 and y.shape[1] == 2:
        # shape (n,2) -> transpose
        y = y.T
    elif y.ndim == 2 and y.shape[0] == 2:
        pass
    else:
        raise ValueError("Input audio must be shape (n,) or (n,2) or (2,n)")

    left = y[0].astype(np.float64)
    right = y[1].astype(np.float64)

    # Basic RMS (global)
    def rms(x):
        return float(np.sqrt(np.mean(x**2))) if x.size > 0 else 0.0

    rms_L = rms(left)
    rms_R = rms(right)
    lr_balance = (rms_L - rms_R) / max(rms_L + rms_R, 1e-12)  # -1..+1 (neg = right louder)

    # Correlation / phase correlation (Pearson's r)
    # if constant signal produce safe result
    if left.std() < 1e-12 or right.std() < 1e-12:
        correlation = 1.0 if np.allclose(left, right) else 0.0
    else:
        correlation = float(np.corrcoef(left, right)[0, 1])

    # Mid / Side signals
    mid = (left + right) / 2.0
    side = (left - right) / 2.0
    mid_energy = float(np.sum(mid**2))
    side_energy = float(np.sum(side**2))
    ms_ratio = float(mid_energy / max(mid_energy + side_energy, 1e-12))  # fraction center
    side_ratio = float(side_energy / max(mid_energy + side_energy, 1e-12))  # fraction side

    # STFT (magnitude) for band analysis
    S_left = np.abs(librosa.stft(left, n_fft=n_fft, hop_length=hop_length))
    S_right = np.abs(librosa.stft(right, n_fft=n_fft, hop_length=hop_length))
    freqs = librosa.fft_frequencies(sr=sr, n_fft=n_fft)

    # Per-band M/S energies and width
    band_ms = {}
    band_widths = {}
    for name, (f_low, f_high) in bands.items():
        # ensure f_high within Nyquist
        f_high = min(f_high if f_high is not None else sr//2, sr//2)
        mask = (freqs >= f_low) & (freqs <= f_high)
        if not np.any(mask):
            band_ms[name] = {"mid_energy": 0.0, "side_energy": 0.0}
            band_widths[name] = 0.0
            continue

        L_mag = S_left[mask, :]
        R_mag = S_right[mask, :]

        # compute energy = sum over freq bins and frames of mag^2
        L_energy = float(np.sum(L_mag**2))
        R_energy = float(np.sum(R_mag**2))

        # mid/side energy per band (using magnitudes -> energies)
        band_mid_energy = (L_energy + R_energy + 2.0 * np.sum(L_mag * R_mag)) / 4.0
        band_side_energy = (L_energy + R_energy - 2.0 * np.sum(L_mag * R_mag)) / 4.0

        # numerical safety
        band_mid_energy = float(max(band_mid_energy, 0.0))
        band_side_energy = float(max(band_side_energy, 0.0))

        band_ms[name] = {
            "mid_energy": band_mid_energy,
            "side_energy": band_side_energy
        }

        # width metric: side / (mid+side) in [0..1]
        denom = band_mid_energy + band_side_energy
        width = float(band_side_energy / denom) if denom > 1e-12 else 0.0
        band_widths[name] = width

    # Global width (from STFT energies)
    # compute global frame-wise mid and side RMS to capture time variation
    frames = S_left.shape[1]
    frame_mid = []
    frame_side = []
    for f_idx in range(frames):
        Lf = S_left[:, f_idx]
        Rf = S_right[:, f_idx]
        mid_f = np.sum((Lf + Rf)**2) / 4.0
        side_f = np.sum((Lf - Rf)**2) / 4.0
        frame_mid.append(mid_f)
        frame_side.append(side_f)

    frame_mid = np.array(frame_mid)
    frame_side = np.array(frame_side)
    frame_denom = frame_mid + frame_side + 1e-12
    frame_width = frame_side / frame_denom  # per frame

    mean_frame_width = float(np.mean(frame_width)) if frame_width.size > 0 else 0.0
    std_frame_width = float(np.std(frame_width)) if frame_width.size > 0 else 0.0

    # Left/Right balance over time: compute short-time RMS and report mean/std
    frame_rms_L = librosa.feature.rms(y=left, frame_length=n_fft, hop_length=hop_length)[0]
    frame_rms_R = librosa.feature.rms(y=right, frame_length=n_fft, hop_length=hop_length)[0]
    # convert to python lists if desired, but we'll compute summary stats
    # balance per frame: (L-R)/(L+R)
    denom = frame_rms_L + frame_rms_R + 1e-12
    frame_balance = (frame_rms_L - frame_rms_R) / denom
    mean_frame_balance = float(np.mean(frame_balance)) if frame_balance.size > 0 else 0.0
    std_frame_balance = float(np.std(frame_balance)) if frame_balance.size > 0 else 0.0

    results = {
        "rms_left": float(rms_L),
        "rms_right": float(rms_R),
        "lr_balance": float(lr_balance),               # -1..+1 (neg = right louder)
        "correlation": float(correlation),             # -1..+1 (1 = mono identical)
        "mid_energy": float(mid_energy),
        "side_energy": float(side_energy),
        "ms_center_fraction": float(ms_ratio),
        "ms_side_fraction": float(side_ratio),
        "band_ms": band_ms,                            # nested dict with mid/side energies
        "band_widths": band_widths,                    # side/(mid+side) per band
        "mean_frame_width": mean_frame_width,
        "std_frame_width": std_frame_width,
        "mean_frame_balance": mean_frame_balance,
        "std_frame_balance": std_frame_balance
    }

    return results

