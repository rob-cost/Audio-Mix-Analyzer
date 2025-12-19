from analysis.audio.audio_features import (
    load_audio,
    get_tempo_features, 
    get_loudness_features, 
    get_frequency_spectrum_energy,
    get_transient_features, 
    get_stereo_imaging_features
)
from analysis.audio.audio_converter import convert_to_wav_in_memory
import time
import librosa

    
def analyze_uploaded_track_complete(audio_bytes: bytes, mime_type: str):
    """
    Extract ALL features in one pass.
    Loads audio only once per sample rate needed.
    """

    start_time = time.time()


    # --- CONVERT AUDIO TO WAV ---

    single_time = time.time()

    try:
        wav_bytes = convert_to_wav_in_memory(audio_bytes, mime_type)
    except ValueError as e:
        print(f"Skipping conversion: {e}")
        wav_bytes = None # mark as unavailable
    
    conversion_time = time.time() - single_time
    print(f"\n{'='*50}")
    print(f"Audio conversion to WAV took {conversion_time:.2f} seconds.")
    print(f"\n{'='*50}")


    # --- LOAD AUDIO ---
    try:

        # Load audio in stereo
        y_stereo, sr_stereo = load_audio(wav_bytes, sr=None, mono=False)
        # Load audio in mono
        y_mono = librosa.to_mono(y_stereo)
        sr_mono = sr_stereo
        # Load audio for harmonic_features
        # y_harmonic = librosa.resample(y_mono, orig_sr=sr_mono, target_sr=22050)
        # sr_harmonic = 22050
        # Calculate onset
        onset_env = librosa.onset.onset_strength(y=y_mono, sr=sr_mono)

    except Exception as e:
        print(f"Failed to load audio: {e}")


    # --- TEMPO FEATURES ---

    tempo_features = None
    if wav_bytes:
        single_time = time.time()
        try:
            tempo_features = get_tempo_features(y_mono, sr_mono, onset_env=onset_env)
        except Exception as e:
            print(f"Skipping tempo features: {e}")
        tempo_time = time.time() - single_time
        print(f"\n{'='*50}")
        print("TEMPO FEATURES")
        print(tempo_features)
        print(f"Tempo feature extraction took {tempo_time:.2f} seconds.")
        print(f"\n{'='*50}")


    # --- LOUDNESS FEATURES ---

    loudness_features = None
    if wav_bytes:
        single_time = time.time()

        try:
            loudness_features = get_loudness_features(y_stereo, sr_stereo)
        except Exception as e:
            print(f"Skipping loudness features: {e}")
        loudness_time = time.time() - single_time
        print(f"\n{'='*50}")
        print("LOUDNESS FEATURES")
        print(loudness_features)
        print(f"Loudness feature extraction took {loudness_time:.2f} seconds.")
        print(f"\n{'='*50}")


    # --- TRANSIENT FEATURES ---
    if loudness_features["dynamic_range_db"] < 8:
        transient_features = None
        if wav_bytes:
            single_time = time.time()
            try:
                transient_features = get_transient_features(y_mono, sr_mono, max_duration=120)
            except Exception as e:
                print(f"Skipping transient features: {e}")
            transient_time = time.time() - single_time
            print(f"\n{'='*50}")
            print("TRANSIENT FEATURES")
            print(transient_features)
            print(f"Transient feature extraction took {transient_time:.2f} seconds.")
            print(f"\n{'='*50}")
    else:
        transient_features = {"note": "Transient features skipped."}


    # --- HARMONIC FEATURES --- (currently disabled) ---

    # harmonic_features = None
    # if wav_bytes:
    #     single_time = time.time()
    #     try:
    #         harmonic_features = get_harmonic_content_features(y_harmonic, sr_harmonic)
    #     except Exception as e:
    #         print(f"Skipping harmonic features: {e}")
    #     harmonic_time = time.time() - single_time
    #     print(f"\n{'='*50}")
    #     print("HARMONIC FEATURES")
    #     print(harmonic_features)
    #     print(f"Harmonic content feature extraction took {harmonic_time:.2f} seconds.")
    #     print(f"\n{'='*50}")


    # --- FREQUENCY SPECTRUM ENERGY ---

    frequency_spectrum_energy = None
    if wav_bytes:
        single_time = time.time()
        try:
            frequency_spectrum_energy = get_frequency_spectrum_energy(y_mono, sr_mono)
        except Exception as e:
            print(f"Skippin frequency spectrum features: {e}")
        frequency_spectrum_time = time.time() - single_time
        print(f"\n{'='*50}")
        print("FREQUENCY SPECTRUM FEATURES")
        print(frequency_spectrum_energy)
        print(f"Frequency Spectrum extraction took {frequency_spectrum_time:.2f} seconds.")
        print(f"\n{'='*50}")


    # --- STEREO IMAGE FEATURES ---

    stereo_imaging_features = None
    if wav_bytes:
        single_time = time.time()
        try:
            stereo_imaging_features = get_stereo_imaging_features(y_stereo, sr_stereo)
        except Exception as e:
            print(f"Skipping stereo imaging feature: {e}")
        stere_imaging_time = time.time() - single_time
        print(f"\n{'='*50}")
        print("STEREO IMAGING FEATURES")
        print(stereo_imaging_features)
        print(f"Stereo Imaging content feature extraction took {stere_imaging_time:.2f} seconds.")
        print(f"\n{'='*50}")


        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"\n{'='*50}")
        print(f"Analysis completed in {elapsed_time:.2f} seconds.")
        print(f"\n{'='*50}")

        return {
            "tempo_features": tempo_features,
            "loudness_features": loudness_features,
            "transient_features": transient_features,
            # "harmonic_features": harmonic_features,
            "frequency_spectrum_energy": frequency_spectrum_energy,
            "stereo_image_features": stereo_imaging_features
        }
        