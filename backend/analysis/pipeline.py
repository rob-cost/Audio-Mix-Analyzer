from .audio_features import (
    get_tempo_features, 
    get_loudness_features, 
    get_frequency_spectrum_energy,
    get_harmonic_content_features, 
    get_transient_features, 
    get_stereo_imaging_features
)
from .embeddings import embedding_from_bytes
from .audio_utils import convert_to_wav_in_memory
import time


def analyze_uploaded_track(audio_bytes: bytes, mime_type: str):
    start_time = time.time()

    # Convert uploaded audio to WAV in memory
    single_time = time.time()
    try:
        wav_bytes = convert_to_wav_in_memory(audio_bytes, mime_type)
    except ValueError as e:
        print(f"Skipping conversion: {e}")
        wav_bytes = None  # mark as unavailable
    
    conversion_time = time.time() - single_time
    print(f"\n{'='*50}")
    print(f"Audio conversion to WAV took {conversion_time:.2f} seconds.")
    print(f"\n{'='*50}")
  
  
    # Tempo features
    tempo_features = None
    if wav_bytes:
        single_time = time.time()
        try:
            tempo_features = get_tempo_features(wav_bytes)
        except Exception as e:
            print(f"Skipping tempo features: {e}")
        tempo_time = time.time() - single_time
        print(f"\n{'='*50}")
        print("TEMPO FEATURES")
        print(tempo_features)
        print(f"Tempo feature extraction took {tempo_time:.2f} seconds.")
        print(f"\n{'='*50}")
    

    # Loudness features
    loudness_features = None
    if wav_bytes:
        single_time = time.time()
        try:
            loudness_features = get_loudness_features(wav_bytes)
        except Exception as e:
            print(f"Skipping loudness features: {e}")
        loudness_time = time.time() - single_time
        print(f"\n{'='*50}")
        print("LOUDNESS FEATURES")
        print(loudness_features)
        print(f"Loudness feature extraction took {loudness_time:.2f} seconds.")
        print(f"\n{'='*50}")
    
    # Transient features
    transient_features = None
    if wav_bytes:
        single_time = time.time()
        try:
            transient_features = get_transient_features(wav_bytes)
        except Exception as e:
            print(f"Skipping transient features: {e}")
        transient_time = time.time() - single_time
        print(f"\n{'='*50}")
        print("TRANSIENT FEATURES")
        print(transient_features)
        print(f"Transient feature extraction took {transient_time:.2f} seconds.")
        print(f"\n{'='*50}")

    
    # Harmonic content features
    harmonic_features = None
    if wav_bytes:
        single_time = time.time()
        try:
            harmonic_features = get_harmonic_content_features(wav_bytes)
        except Exception as e:
            print(f"Skipping harmonic features: {e}")
        harmonic_time = time.time() - single_time
        print(f"\n{'='*50}")
        print("HARMONIC FEATURES")
        print(harmonic_features)
        print(f"Harmonic content feature extraction took {harmonic_time:.2f} seconds.")
        print(f"\n{'='*50}")


    # Frequency Spectrum Energy
    frequency_spectrum_features = None
    if wav_bytes:
        single_time = time.time()
        try:
            frequency_spectrum_features = get_frequency_spectrum_energy(wav_bytes)
        except Exception as e:
            print(f"Skippin frequency spectrum features: {e}")
        frequency_spectrum_time = time.time() - single_time
        print(f"\n{'='*50}")
        print("FREQUENCY SPECTRUM FEATURES")
        print(frequency_spectrum_features)
        print(f"Frequency Spectrum extraction took {frequency_spectrum_time:.2f} seconds.")
        print(f"\n{'='*50}")


    # Stereo imaging features
    stereo_imaging_features = None
    if wav_bytes:
        single_time = time.time()
        try:
            stereo_imaging_features = get_stereo_imaging_features(wav_bytes)
        except Exception as e:
            print(f"Skipping stereo imaging feature: {e}")
        stere_imaging_time = time.time() - single_time
        print(f"\n{'='*50}")
        print("STEREO IMAGING FEATURES")
        print(stereo_imaging_features)
        print(f"Stereo Imaging content feature extraction took {stere_imaging_time:.2f} seconds.")
        print(f"\n{'='*50}")
    
    # Music embeddings
    # emb = None
    # if wav_bytes:
    #     single_time = time.time()
    #     try:
    #         emb = embedding_from_bytes(wav_bytes)
    #     except Exception as e:
    #         print(f"Skipping music embeddings: {e}")
    #     emb_time = time.time() - single_time
    #     print(f"Music embedding extraction took {emb_time:.2f} seconds.")
    #     print(f"\n{'='*50}")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\n{'='*50}")
    print(f"Analysis completed in {elapsed_time:.2f} seconds.")
    print(f"\n{'='*50}")

    return {
        "tempo_features": tempo_features,
        "loudness_features": loudness_features,
        "transient_features": transient_features,
        "harmonic_features": harmonic_features,
        "frequency_spectrum_energy": frequency_spectrum_features,
        "stereo_imaging_feature": stereo_imaging_features
    }
   



