import whisper
import hashlib
import pickle
import os
from typing import Dict, Any

class CachedWhisper:
    def __init__(self, model_size="medium"):
        self.model = whisper.load_model(model_size)
        self.cache_dir = "./cache/transcriptions"
        os.makedirs(self.cache_dir, exist_ok=True)
        
    def transcribe_with_cache(self, audio_path: str, **kwargs) -> Dict[str, Any]:
        # Create cache key
        cache_key = self._generate_cache_key(audio_path, kwargs)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")
        
        # Check cache
        if os.path.exists(cache_file):
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        
        # Transcribe
        result = self.model.transcribe(audio_path, **kwargs)
        
        # Cache result
        with open(cache_file, 'wb') as f:
            pickle.dump(result, f)
            
        return result
    
    def _generate_cache_key(self, audio_path: str, kwargs: dict) -> str:
        content = f"{audio_path}_{str(sorted(kwargs.items()))}"
        return hashlib.md5(content.encode()).hexdigest()