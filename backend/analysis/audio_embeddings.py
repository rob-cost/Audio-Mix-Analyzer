import io
import librosa
import openl3
import numpy as np

def embedding_from_bytes(audio_bytes, sr=48000):
    audio_buffer = io.BytesIO(audio_bytes)
    y, sr = librosa.load(audio_buffer, sr=sr, mono=False)

    # Ensure stereo shape [2, n_samples]
    if y.ndim == 1:
        y = np.vstack([y, y])

    # OpenL3 embedding (music, content type 'music')
    emb, ts = openl3.get_audio_embedding(
        y.T, sr, content_type='music', input_repr='mel256', embedding_size=512
    )

    # Mean embedding for full track
    emb_mean = emb.mean(axis=0)
    return {"embedding_music": emb_mean.tolist()}
