from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class AudioAnalysis(Base):
    __tablename__ = 'audio_analysis'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    audio_file = Column(String(255))
    transcript = Column(Text)
    sentiment_score = Column(Float)
    is_aggressive = Column(Boolean, default=False)
    has_trigger = Column(Boolean, default=False)
    confidence = Column(Float)
    processing_time = Column(Float)
    speaker_count = Column(Integer)
    
class AlertLog(Base):
    __tablename__ = 'alert_logs'
    
    id = Column(Integer, primary_key=True)
    analysis_id = Column(Integer)
    alert_type = Column(String(100))
    triggered_patterns = Column(Text)  # JSON
    confidence = Column(Float)
    sent_at = Column(DateTime, default=datetime.utcnow)
    acknowledged = Column(Boolean, default=False)
    response_time = Column(Float)

class SystemMetrics(Base):
    __tablename__ = 'system_metrics'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    cpu_usage = Column(Float)
    memory_usage = Column(Float)
    disk_usage = Column(Float)
    active_connections = Column(Integer)
    queue_length = Column(Integer)

# Database setup
engine = create_engine('sqlite:///audio_nlp.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)