from pyannote.audio import Pipeline
import torch

class SpeakerDiarizer:
    def __init__(self):
        # Load pre-trained diarization pipeline
        self.pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization",
            use_auth_token="YOUR_HF_TOKEN"
        )
        
    def diarize_audio(self, audio_path: str):
        # Apply diarization
        diarization = self.pipeline(audio_path)
        
        # Extract speaker segments
        segments = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            segments.append({
                "start": turn.start,
                "end": turn.end,
                "speaker": speaker,
                "duration": turn.end - turn.start
            })
            
        return segments