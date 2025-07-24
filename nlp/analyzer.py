from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import spacy
from textblob import TextBlob
import re
from typing import Dict, List

class ContextualNLPAnalyzer:
    def __init__(self):
        # Load models
        self.nlp = spacy.load("en_core_web_sm")
        self.intent_classifier = pipeline(
            "text-classification",
            model="mrm8488/distilroberta-finetuned-sentiment-analysis"
        )
        self.aggression_detector = self._load_custom_model()
        
        # Define patterns
        self.aggressive_patterns = [
            r"\b(shut\s+up|go\s+away|leave\s+me\s+alone)\b",
            r"\b(don'?t\s+talk|stop\s+following)\b",
            r"\b(angry|furious|mad)\s+(at\s+me|with\s+me)\b"
        ]
        
        self.trigger_patterns = [
            r"\b(help|emergency|danger|scared)\b",
            r"\b(please|need)\s+(help|assistance)\b"
        ]
        
    def analyze_text(self, text: str, context: Dict = None) -> Dict:
        # Basic NLP processing
        doc = self.nlp(text)
        
        # Multi-model sentiment analysis
        sentiment_blob = TextBlob(text)
        sentiment_transformer = self.intent_classifier(text)
        
        # Pattern matching with context awareness
        aggressive_matches = self._find_contextual_matches(
            text, self.aggressive_patterns, context
        )
        trigger_matches = self._find_contextual_matches(
            text, self.trigger_patterns, context
        )
        
        # Intent classification
        intent = self._classify_intent(text, context)
        
        # Entity extraction
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        
        # Repetition detection
        repetitions = self._detect_repetitions(doc)
        
        return {
            "transcript": text,
            "sentiment": {
                "textblob": sentiment_blob.sentiment.polarity,
                "transformer": sentiment_transformer[0]
            },
            "aggressive_phrases": aggressive_matches,
            "trigger_terms": trigger_matches,
            "intent": intent,
            "entities": entities,
            "repetitions": repetitions,
            "confidence": self._calculate_confidence(text)
        }
    
    def _find_contextual_matches(self, text: str, patterns: List[str], context: Dict = None) -> List[str]:
        matches = []
        for pattern in patterns:
            found = re.findall(pattern, text, re.IGNORECASE)
            if found:
                matches.extend(found)
        return matches
    
    def _classify_intent(self, text: str, context: Dict = None) -> str:
        # Custom logic combining multiple signals
        base_intent = self.intent_classifier(text)[0]['label']
        
        # Adjust based on context
        if context and context.get('previous_transcripts'):
            # Check for escalation patterns
            if self._detect_escalation(context['previous_transcripts']):
                return "escalating_" + base_intent
                
        return base_intent
    
    def _detect_repetitions(self, doc) -> Dict:
        # Advanced repetition detection
        from collections import Counter
        tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]
        counts = Counter(tokens)
        
        # Find repeated phrases (bigrams, trigrams)
        bigrams = [f"{tokens[i]} {tokens[i+1]}" for i in range(len(tokens)-1)]
        trigrams = [f"{tokens[i]} {tokens[i+1]} {tokens[i+2]}" for i in range(len(tokens)-2)]
        
        return {
            "repeated_words": [word for word, count in counts.items() if count > 2],
            "repeated_bigrams": [bg for bg, count in Counter(bigrams).items() if count > 1],
            "repeated_trigrams": [tg for tg, count in Counter(trigrams).items() if count > 1]
        }
    
    def _calculate_confidence(self, text: str) -> float:
        # Confidence based on text quality and model agreement
        length_score = min(len(text) / 100, 1.0)  # Longer texts = higher confidence
        clarity_score = 1.0 - (text.count('...') / max(len(text), 1))  # Fewer hesitations = better
        return (length_score + clarity_score) / 2
    
    def _detect_escalation(self, previous_transcripts: List[str]) -> bool:
        # Simple escalation detection
        aggressive_count = sum(
            1 for transcript in previous_transcripts[-3:] 
            if any(re.search(pattern, transcript, re.IGNORECASE) 
                  for pattern in self.aggressive_patterns)
        )
        return aggressive_count >= 2