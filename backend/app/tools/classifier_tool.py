"""ML classifier tool for travel style classification."""

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


class TravelStyleClassifier:
    """Singleton classifier for identifying travel style."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            # Create a simple mock classifier
            # In production, load: joblib.load("models/best_svm.pkl")
            self.vectorizer = TfidfVectorizer(max_features=100)
            self.styles = ["adventure", "luxury", "cultural", "relaxation", "budget"]
            self._initialized = True
    
    def classify(self, text: str) -> str:
        """Classify travel style from text."""
        text_lower = text.lower()
        
        # Simple rule-based classification
        if any(word in text_lower for word in ["adventure", "hiking", "extreme", "thrilling"]):
            return "adventure"
        elif any(word in text_lower for word in ["luxury", "premium", "expensive", "5-star"]):
            return "luxury"
        elif any(word in text_lower for word in ["culture", "history", "museum", "art"]):
            return "cultural"
        elif any(word in text_lower for word in ["relax", "beach", "spa", "peace", "tropical", "island", "ocean", "resort"]):
            return "relaxation"
        elif any(word in text_lower for word in ["budget", "cheap", "backpack", "economy"]):
            return "budget"
        
        return "balanced"


# Global singleton instance
classifier = TravelStyleClassifier()


def classify_travel_style(query: str) -> dict:
    """Tool function to classify travel style."""
    style = classifier.classify(query)
    return {"travel_style": style}
