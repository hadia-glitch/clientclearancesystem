

import re
import spacy
import nltk
from textblob import TextBlob
from typing import Dict, List, Tuple, Any


class TextAnalyzer:
    def __init__(self):
        """Initialize the text analyzer with NLP models"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
           
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
        
        # Download NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        # Business keywords for classification
        self.business_keywords = {
            'retail': ['store', 'shop', 'retail', 'ecommerce', 'online store', 'marketplace', 'selling', 'products'],
            'restaurant': ['restaurant', 'food', 'delivery', 'takeout', 'dining', 'cafe', 'menu', 'kitchen'],
            'healthcare': ['medical', 'healthcare', 'clinic', 'hospital', 'patient', 'doctor', 'health', 'medicine'],
            'education': ['school', 'education', 'learning', 'course', 'training', 'academy', 'student', 'teaching'],
            'logistics': ['logistics', 'shipping', 'delivery', 'warehouse', 'supply chain', 'transport', 'freight'],
            'finance': ['banking', 'finance', 'investment', 'accounting', 'budget', 'money', 'financial'],
            'real_estate': ['real estate', 'property', 'housing', 'rental', 'mortgage', 'realty', 'home'],
            'consulting': ['consulting', 'consultant', 'advisory', 'professional services', 'business advice']
        }
        
        # Platform indicators
        self.platform_indicators = {
            'mobile': ['mobile', 'phone', 'android', 'ios', 'smartphone', 'tablet'],
            'web': ['website', 'web', 'online', 'browser', 'internet', 'web application'],
            'desktop': ['desktop', 'computer', 'pc', 'software', 'application', 'program']
        }
        
        # Feature keywords
        self.feature_keywords = {
            'inventory': ['inventory', 'stock', 'products', 'items', 'catalog'],
            'payment': ['payment', 'billing', 'checkout', 'pay', 'money', 'transaction'],
            'tracking': ['tracking', 'monitoring', 'analytics', 'reports', 'dashboard'],
            'user_management': ['users', 'accounts', 'profiles', 'registration', 'login'],
            'communication': ['chat', 'messaging', 'email', 'notifications', 'alerts'],
            'scheduling': ['appointments', 'booking', 'calendar', 'schedule', 'reservations'],
            'reporting': ['reports', 'analytics', 'statistics', 'data', 'insights']
        }

    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyze client input text and extract key information"""
        # Preprocess text
        processed_text = self._preprocess_text(text)
        
        # Analyze different aspects
        analysis = {
            'original_text': text,
            'processed_text': processed_text,
            'clarity_score': self._calculate_clarity_score(text),
            'business_type': self._classify_business_type(text),
            'platform_preference': self._detect_platform_preference(text),
            'detected_features': self._extract_features(text),
            'sentiment': self._analyze_sentiment(text),
            'urgency_level': self._detect_urgency(text),
            'budget_indicators': self._extract_budget_indicators(text),
            'timeline_indicators': self._extract_timeline_indicators(text),
            'portability': self._detect_portability_requirement(text),
            'notification_requirement': self._detect_notification_requirement(text)
        }
        
        return analysis

    def _preprocess_text(self, text: str) -> str:
        """Clean and preprocess input text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep important ones
        text = re.sub(r'[^\w\s\-\.\,\!\?]', '', text)
        
        return text.strip()

    def _calculate_clarity_score(self, text: str) -> float:
        """Calculate how clear and specific the input is"""
        doc = self.nlp(text.lower())
        
        # Count specific business terms
        business_terms = sum(1 for token in doc if any(keyword in token.text for keywords in self.business_keywords.values() for keyword in keywords))
        
        # Count platform indicators
        platform_terms = sum(1 for token in doc if any(keyword in token.text for keywords in self.platform_indicators.values() for keyword in keywords))
        
        # Count feature keywords
        feature_terms = sum(1 for token in doc if any(keyword in token.text for keywords in self.feature_keywords.values() for keyword in keywords))
        
        # Calculate clarity based on specificity
        total_indicators = business_terms + platform_terms + feature_terms
        text_length = len(text.split())
        
        if text_length == 0:
            return 0.0
        
        # Normalize by text length and add base clarity
        clarity = min(1.0, (total_indicators / text_length) * 10 + 0.2)
        
        return round(clarity, 2)

    def _classify_business_type(self, text: str) -> Tuple[str, float]:
        """Classify the business type based on keywords"""
        text_lower = text.lower()
        scores = {}
        
        for business_type, keywords in self.business_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[business_type] = score
        
        if not any(scores.values()):
            return ('unknown', 0.0)
        
        # Find the business type with highest score
        best_type = max(scores, key=scores.get)
        confidence = scores[best_type] / max(len(keywords) for keywords in self.business_keywords.values())
        
        return (best_type, round(confidence, 2))

    def _detect_platform_preference(self, text: str) -> Tuple[str, float]:
        """Detect platform preference (mobile/web/desktop)"""
        text_lower = text.lower()
        scores = {}
        
        for platform, keywords in self.platform_indicators.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[platform] = score
        
        if not any(scores.values()):
            return ('web', 0.3)  # Default to web
        
        best_platform = max(scores, key=scores.get)
        confidence = scores[best_platform] / max(len(keywords) for keywords in self.platform_indicators.values())
        
        return (best_platform, round(confidence, 2))

    def _extract_features(self, text: str) -> List[str]:
        """Extract suggested features from the text"""
        text_lower = text.lower()
        detected_features = []
        
        for feature_category, keywords in self.feature_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_features.append(feature_category)
        
        return detected_features

    def _analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment of the input"""
        blob = TextBlob(text)
        sentiment = blob.sentiment
        
        return {
            'polarity': round(sentiment.polarity, 2),
            'subjectivity': round(sentiment.subjectivity, 2)
        }

    def _detect_urgency(self, text: str) -> str:
        """Detect urgency level in the text"""
        urgency_keywords = ['urgent', 'asap', 'quickly', 'fast', 'immediate', 'emergency', 'rush']
        text_lower = text.lower()
        
        urgency_count = sum(1 for keyword in urgency_keywords if keyword in text_lower)
        
        if urgency_count >= 2:
            return 'high'
        elif urgency_count == 1:
            return 'medium'
        else:
            return 'low'

    def _extract_budget_indicators(self, text: str) -> Dict[str, Any]:
        """Extract budget-related information"""
        # Look for budget keywords
        budget_keywords = ['budget', 'cost', 'price', 'affordable', 'cheap', 'expensive', 'money']
        text_lower = text.lower()
        
        budget_mentioned = any(keyword in text_lower for keyword in budget_keywords)
        
        # Extract numbers that might be budget amounts
        numbers = re.findall(r'\$?(\d+(?:,\d{3})*(?:\.\d{2})?)', text)
        budget_amounts = [int(num.replace(',', '')) for num in numbers if int(num.replace(',', '')) > 100]
        
        return {
            'budget_mentioned': budget_mentioned,
            'budget_amounts': budget_amounts,
            'has_budget_info': len(budget_amounts) > 0
        }

    def _extract_timeline_indicators(self, text: str) -> Dict[str, Any]:
        """Extract timeline-related information"""
        timeline_keywords = ['timeline', 'deadline', 'schedule', 'time', 'when', 'duration']
        text_lower = text.lower()
        
        timeline_mentioned = any(keyword in text_lower for keyword in timeline_keywords)
        
        # Extract time-related words
        time_words = ['week', 'month', 'year', 'day', 'hour']
        time_indicators = [word for word in time_words if word in text_lower]
        
        return {
            'timeline_mentioned': timeline_mentioned,
            'time_indicators': time_indicators,
            'has_timeline_info': len(time_indicators) > 0
        }

    def needs_clarification(self, analysis: Dict[str, Any]) -> bool:
        """Determine if the input needs clarification"""
        clarity_score = analysis['clarity_score']
        business_type, confidence = analysis['business_type']
        
        # Need clarification if:
        # 1. Clarity score is low
        # 2. Business type is unknown or low confidence
        # 3. No specific features detected
        # 4. No platform preference detected
        
        return (clarity_score < 0.5 or 
                business_type == 'unknown' or 
                confidence < 0.3 or
                len(analysis['detected_features']) == 0)

    def generate_clarification_questions(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate follow-up questions based on analysis"""
        questions = []
        
        business_type, confidence = analysis['business_type']
        
        if business_type == 'unknown' or confidence < 0.3:
            questions.append("What type of business do you operate?")
        
        if len(analysis['detected_features']) == 0:
            questions.append("What specific features or functionality do you need?")
        
        if not analysis['budget_indicators']['budget_mentioned']:
            questions.append("Do you have a budget range in mind for this project?")
        
        if not analysis['timeline_indicators']['timeline_mentioned']:
            questions.append("When do you need this system to be completed?")
        
        if analysis['clarity_score'] < 0.4:
            questions.append("Can you provide more details about your business requirements?")
        
        return questions[:3]  # Limit to 3 questions

    def _detect_portability_requirement(self, text: str) -> str:
        """Detect if the client needs high portability (mobile access)"""
        text_lower = text.lower()
        
        # High portability indicators
        high_portability_keywords = [
            'mobile', 'phone', 'smartphone', 'tablet', 'ios', 'android',
            'on-the-go', 'portable', 'travel', 'remote', 'field', 'outdoor',
            'delivery', 'tracking', 'location', 'gps', 'real-time', 'instant',
            'anywhere', 'everywhere', 'accessible', 'mobile-first', 'responsive'
        ]
        
        # Medium portability indicators
        medium_portability_keywords = [
            'web', 'website', 'online', 'browser', 'responsive', 'tablet-friendly',
            'cross-platform', 'accessible', 'remote access', 'cloud-based'
        ]
        
        # Low portability indicators
        low_portability_keywords = [
            'desktop', 'computer', 'pc', 'workstation', 'office', 'stationary',
            'fixed', 'local', 'internal', 'enterprise', 'corporate'
        ]
        
        # Count keyword matches
        high_count = sum(1 for keyword in high_portability_keywords if keyword in text_lower)
        medium_count = sum(1 for keyword in medium_portability_keywords if keyword in text_lower)
        low_count = sum(1 for keyword in low_portability_keywords if keyword in text_lower)
        
        # Determine portability level
        if high_count > 0:
            return 'high'
        elif medium_count > 0:
            return 'medium'
        elif low_count > 0:
            return 'low'
        else:
            return 'medium'  # Default to medium if no clear indicators

    def _detect_notification_requirement(self, text: str) -> str:
        """Detect if the client needs major notification features"""
        text_lower = text.lower()
        
        # Major notification indicators
        major_notification_keywords = [
            'notification', 'alert', 'push', 'real-time', 'instant', 'immediate',
            'urgent', 'emergency', 'critical', 'important', 'reminder', 'ping',
            'message', 'update', 'status', 'tracking', 'monitoring', 'live',
            'notify', 'alarm', 'warning', 'announcement', 'broadcast'
        ]
        
        # Minor notification indicators
        minor_notification_keywords = [
            'email', 'report', 'summary', 'daily', 'weekly', 'monthly',
            'newsletter', 'update', 'news', 'information', 'communication'
        ]
        
        # Count keyword matches
        major_count = sum(1 for keyword in major_notification_keywords if keyword in text_lower)
        minor_count = sum(1 for keyword in minor_notification_keywords if keyword in text_lower)
        
        # Determine notification requirement level
        if major_count >= 2:  # Need at least 2 major indicators
            return 'major'
        elif minor_count > 0:
            return 'minor'
        else:
            return 'none' 