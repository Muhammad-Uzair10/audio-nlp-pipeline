import librosa
import numpy as np
import webrtcvad
from scipy import signal

class AudioPreprocessor:
    def __init__(self):
        self.vad = webrtcvad.Vad(2)  # Aggressive VAD
        
    def enhance_audio(self, audio_path):
        # Load audio
        y, sr = librosa.load(audio_path, sr=16000)
        
        # Noise reduction
        y_denoised = self.spectral_subtraction(y)
        
        # Automatic gain control
        y_normalized = self.normalize_audio(y_denoised)
        
        # Voice activity detection
        segments = self.segment_speech(y_normalized, sr)
        
        return segments
    
    def spectral_subtraction(self, y):
        # Apply spectral subtraction for noise reduction
        stft = librosa.stft(y)
        magnitude, phase = librosa.magphase(stft)
        
        # Estimate noise floor
        noise_floor = np.mean(magnitude[:, :10], axis=1, keepdims=True)
        
        # Subtract noise
        magnitude_clean = np.maximum(magnitude - noise_floor, 0)
        
        # Reconstruct signal
        stft_clean = magnitude_clean * phase
        return librosa.istft(stft_clean)
    
    def normalize_audio(self, y):
        # Peak normalization
        return y / np.max(np.abs(y)) if np.max(np.abs(y)) > 0 else y
    
    def segment_speech(self, y, sr):
        # Frame-based VAD segmentation
        frame_duration = 0.03  # 30ms frames
        frame_length = int(sr * frame_duration)
        segments = []
        
        for i in range(0, len(y), frame_length):
            frame = y[i:i + frame_length]
            if len(frame) == frame_length:
                is_speech = self.vad.is_speech(
                    (frame * 32767).astype(np.int16).tobytes(), 
                    sr
                )
                if is_speech:
                    segments.append(frame)
        
        return np.concatenate(segments) if segments else np.array([])