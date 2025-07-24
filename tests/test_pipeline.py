import pytest
import tempfile
import numpy as np
from scipy.io import wavfile
import requests

class TestAudioNLPPipeline:
    def setup_method(self):
        self.base_url = "http://localhost:8000"
        self.api_key = "your-secret-key"
        
    def create_test_audio(self, text="Please leave me alone. Stop following me.", duration=10):
        """Create synthetic test audio"""
        # In practice, you'd use a TTS service or real audio files
        sample_rate = 16000
        t = np.linspace(0, duration, int(sample_rate * duration))
        # Simple sine wave as placeholder
        audio_data = (np.sin(2 * np.pi * 440 * t) * 32767).astype(np.int16)
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            wavfile.write(f.name, sample_rate, audio_data)
            return f.name
    
    def test_basic_analysis(self):
        """Test basic audio analysis"""
        audio_file = self.create_test_audio()
        
        with open(audio_file, 'rb') as f:
            files = {'file': f}
            data = {'request': '{"webhook_url": "http://test.com/webhook"}'}
            headers = {'Authorization': f'Bearer {self.api_key}'}
            
            response = requests.post(
                f"{self.base_url}/analyze",
                files=files,
                data=data,
                headers=headers
            )
            
            assert response.status_code == 200
            result = response.json()
            
            # Validate response structure
            assert 'transcript' in result
            assert 'sentiment' in result
            assert 'confidence' in result
            
    def test_aggressive_detection(self):
        """Test detection of aggressive language"""
        audio_file = self.create_test_audio("Go away! Leave me alone!")
        
        with open(audio_file, 'rb') as f:
            files = {'file': f}
            headers = {'Authorization': f'Bearer {self.api_key}'}
            
            response = requests.post(
                f"{self.base_url}/analyze",
                files=files,
                headers=headers
            )
            
            assert response.status_code == 200
            result = response.json()
            
            # Should detect aggressive phrases
            assert len(result['aggressive_phrases']) > 0
            
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = requests.get(f"{self.base_url}/health")
        assert response.status_code == 200
        assert response.json()['status'] == 'healthy'