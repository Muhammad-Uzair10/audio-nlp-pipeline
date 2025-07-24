import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict
import json

class PatternLearningEngine:
    def __init__(self, db_path: str = "patterns.db"):
        self.db_path = db_path
        self._init_db()
        
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learned_patterns (
                id INTEGER PRIMARY KEY,
                pattern_type TEXT,
                pattern TEXT,
                confidence REAL,
                frequency INTEGER DEFAULT 1,
                last_seen TIMESTAMP,
                context TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alert_history (
                id INTEGER PRIMARY KEY,
                timestamp TIMESTAMP,
                alert_type TEXT,
                content TEXT,
                confidence REAL,
                response_time REAL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def learn_from_alert(self, alert_data: Dict):
        """Learn new patterns from triggered alerts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Extract potential patterns
        patterns = self._extract_patterns(alert_data)
        
        for pattern in patterns:
            # Check if pattern exists
            cursor.execute(
                "SELECT id, frequency FROM learned_patterns WHERE pattern = ?",
                (pattern,)
            )
            result = cursor.fetchone()
            
            if result:
                # Update existing pattern
                cursor.execute(
                    "UPDATE learned_patterns SET frequency = frequency + 1, last_seen = ? WHERE id = ?",
                    (datetime.now(), result[0])
                )
            else:
                # Insert new pattern
                cursor.execute(
                    "INSERT INTO learned_patterns (pattern_type, pattern, confidence, last_seen) VALUES (?, ?, ?, ?)",
                    ("learned", pattern, 0.8, datetime.now())
                )
        
        conn.commit()
        conn.close()
    
    def get_adaptive_thresholds(self) -> Dict:
        """Get learned thresholds for adaptive detection"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT pattern, frequency FROM learned_patterns WHERE frequency > 5 ORDER BY frequency DESC LIMIT 10"
        )
        
        patterns = {row[0]: row[1] for row in cursor.fetchall()}
        conn.close()
        
        return patterns
    
    def log_alert(self, alert_type: str, content: str, confidence: float, response_time: float = 0):
        """Log alert for future learning"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO alert_history (timestamp, alert_type, content, confidence, response_time) VALUES (?, ?, ?, ?, ?)",
            (datetime.now(), alert_type, content, confidence, response_time)
        )
        
        conn.commit()
        conn.close()
    
    def _extract_patterns(self, alert_data: Dict) -> List[str]:
        """Extract potential learning patterns from alert data"""
        patterns = []
        
        # Extract from transcript
        transcript = alert_data.get('transcript', '')
        if transcript:
            # Extract key phrases
            words = transcript.split()
            for i in range(len(words) - 1):
                phrase = f"{words[i]} {words[i+1]}"
                if len(phrase.split()) >= 2:
                    patterns.append(phrase.lower())
        
        # Extract from aggressive phrases
        aggressive = alert_data.get('aggressive_phrases', [])
        patterns.extend(aggressive)
        
        return list(set(patterns))  # Remove duplicates