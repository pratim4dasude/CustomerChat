import re
from typing import Tuple

NEGATIVE_KEYWORDS = [
    "frustrated", "angry", "terrible", "awful", "hate", "worst", "broken",
    "not working", "doesn't work", "won't work", "error", "fail", "failed",
    "urgent", "asap", "immediately", "help me", "can't", "cannot", "impossible",
    "stuck", "horrible", "ridiculous", "unacceptable", "disappointed", "annoyed"
]

POSITIVE_KEYWORDS = [
    "thank", "thanks", "great", "excellent", "perfect", "awesome", "amazing",
    "wonderful", "love", "appreciate", "helpful", "resolved", "fixed", "solved",
    "working", "works great", "brilliant", "fantastic", "good job"
]


def detect_sentiment(text: str) -> Tuple[str, float]:
    text_lower = text.lower()
    
    negative_count = sum(1 for keyword in NEGATIVE_KEYWORDS if keyword in text_lower)
    positive_count = sum(1 for keyword in POSITIVE_KEYWORDS if keyword in text_lower)
    
    exclamation_count = text.count('!')
    question_count = text.count('?')
    
    if exclamation_count >= 3:
        negative_count += 1
    if question_count >= 3:
        negative_count += 1
    
    total_signals = negative_count + positive_count + 1
    
    if positive_count > negative_count:
        sentiment = "positive"
        frustration_score = max(0.0, 0.3 - (positive_count * 0.1))
    elif negative_count > positive_count:
        sentiment = "negative"
        frustration_score = min(1.0, 0.5 + (negative_count * 0.1))
    else:
        sentiment = "neutral"
        frustration_score = 0.5
    
    frustration_score = max(0.0, min(1.0, frustration_score))
    
    return sentiment, frustration_score
