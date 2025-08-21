"""
Test cases for the Recommendation Engine
"""

import unittest
import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.engine.recommendation_engine import RecommendationEngine
from src.models.text_analyzer import TextAnalyzer
from src.utils.formatter import RecommendationFormatter

class TestRecommendationEngine(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.engine = RecommendationEngine()
        self.analyzer = TextAnalyzer()
        self.formatter = RecommendationFormatter()

    def test_text_analyzer_initialization(self):
        """Test that text analyzer initializes correctly"""
        self.assertIsNotNone(self.analyzer.nlp)
        self.assertIsNotNone(self.analyzer.business_keywords)
        self.assertIsNotNone(self.analyzer.platform_indicators)

    def test_analyze_clear_input(self):
        """Test analysis of clear input"""
        input_text = "I need an online store to sell my products"
        analysis = self.analyzer.analyze_text(input_text)
        
        self.assertIsInstance(analysis, dict)
        self.assertIn('clarity_score', analysis)
        self.assertIn('business_type', analysis)
        self.assertIn('platform_preference', analysis)
        
        # Should have high clarity for clear input
        self.assertGreater(analysis['clarity_score'], 0.5)
        
        # Should detect retail business
        business_type, confidence = analysis['business_type']
        self.assertEqual(business_type, 'retail')

    def test_analyze_vague_input(self):
        """Test analysis of vague input"""
        input_text = "I need something to help manage my business"
        analysis = self.analyzer.analyze_text(input_text)
        
        # Should have lower clarity for vague input
        self.assertLess(analysis['clarity_score'], 0.6)
        
        # Should need clarification
        needs_clarification = self.analyzer.needs_clarification(analysis)
        self.assertTrue(needs_clarification)

    def test_generate_recommendation(self):
        """Test recommendation generation"""
        input_text = "I need an online store to sell my products"
        recommendation = self.engine.generate_recommendation(input_text)
        
        self.assertIsInstance(recommendation, dict)
        self.assertIn('platform_recommendation', recommendation)
        self.assertIn('feature_recommendations', recommendation)
        self.assertIn('tech_stack_recommendation', recommendation)
        self.assertIn('cost_estimate', recommendation)
        self.assertIn('timeline_estimate', recommendation)
        self.assertIn('confidence_score', recommendation)

    def test_platform_recommendation(self):
        """Test platform recommendation logic"""
        # Test retail business
        analysis = self.analyzer.analyze_text("I need an online store")
        platform_rec = self.engine._recommend_platform(analysis)
        self.assertEqual(platform_rec['platform'], 'web')
        
        # Test restaurant business
        analysis = self.analyzer.analyze_text("I want a food delivery app")
        platform_rec = self.engine._recommend_platform(analysis)
        self.assertEqual(platform_rec['platform'], 'mobile')

    def test_feature_recommendation(self):
        """Test feature recommendation logic"""
        analysis = self.analyzer.analyze_text("I need an online store to sell my products")
        features_rec = self.engine._recommend_features(analysis)
        
        self.assertIsInstance(features_rec, list)
        self.assertGreater(len(features_rec), 0)
        
        # Check that features have required fields
        for feature in features_rec:
            self.assertIn('feature', feature)
            self.assertIn('description', feature)
            self.assertIn('priority', feature)
            self.assertIn('estimated_effort', feature)
            self.assertIn('estimated_cost', feature)

    def test_tech_stack_recommendation(self):
        """Test technology stack recommendation"""
        platform_rec = {'platform': 'web', 'confidence': 0.8}
        analysis = self.analyzer.analyze_text("I need an online store")
        tech_stack_rec = self.engine._recommend_tech_stack(platform_rec, analysis)
        
        self.assertIsInstance(tech_stack_rec, dict)
        self.assertIn('tech_stack', tech_stack_rec)
        self.assertIn('name', tech_stack_rec)
        self.assertIn('description', tech_stack_rec)
        self.assertIn('pros', tech_stack_rec)
        self.assertIn('cons', tech_stack_rec)

    def test_cost_estimation(self):
        """Test cost estimation"""
        platform_rec = {'platform': 'web', 'confidence': 0.8}
        features_rec = [
            {'estimated_cost': 2000, 'estimated_effort': 4},
            {'estimated_cost': 3000, 'estimated_effort': 6}
        ]
        tech_stack_rec = {'cost_factor': 1.0, 'timeline_factor': 1.0}
        
        cost_estimate = self.engine._estimate_cost(platform_rec, features_rec, tech_stack_rec)
        
        self.assertIsInstance(cost_estimate, dict)
        self.assertIn('total_cost', cost_estimate)
        self.assertIn('cost_range', cost_estimate)
        self.assertGreater(cost_estimate['total_cost'], 0)

    def test_timeline_estimation(self):
        """Test timeline estimation"""
        platform_rec = {'platform': 'web', 'confidence': 0.8}
        features_rec = [
            {'estimated_cost': 2000, 'estimated_effort': 4},
            {'estimated_cost': 3000, 'estimated_effort': 6}
        ]
        tech_stack_rec = {'cost_factor': 1.0, 'timeline_factor': 1.0}
        
        timeline_estimate = self.engine._estimate_timeline(platform_rec, features_rec, tech_stack_rec)
        
        self.assertIsInstance(timeline_estimate, dict)
        self.assertIn('total_timeline', timeline_estimate)
        self.assertIn('timeline_range', timeline_estimate)
        self.assertGreater(timeline_estimate['total_timeline'], 0)

    def test_formatter(self):
        """Test recommendation formatter"""
        input_text = "I need an online store to sell my products"
        recommendation = self.engine.generate_recommendation(input_text)
        
        # Test full formatting
        formatted = self.formatter.format_recommendation(recommendation)
        self.assertIsInstance(formatted, str)
        self.assertIn("AI RECOMMENDATION REPORT", formatted)
        
        # Test summary formatting
        summary = self.formatter.format_summary(recommendation)
        self.assertIsInstance(summary, str)
        self.assertIn("QUICK SUMMARY", summary)
        
        # Test JSON formatting
        json_output = self.formatter.format_json(recommendation)
        self.assertIsInstance(json_output, str)

    def test_clarification_questions(self):
        """Test clarification question generation"""
        # Test vague input
        analysis = self.analyzer.analyze_text("I need something for my business")
        questions = self.analyzer.generate_clarification_questions(analysis)
        
        self.assertIsInstance(questions, list)
        self.assertGreater(len(questions), 0)
        
        # Test clear input
        analysis = self.analyzer.analyze_text("I need an online store to sell my products")
        questions = self.analyzer.generate_clarification_questions(analysis)
        
        # Should have fewer questions for clear input
        self.assertLessEqual(len(questions), 3)

    def test_confidence_calculation(self):
        """Test confidence score calculation"""
        input_text = "I need an online store to sell my products"
        recommendation = self.engine.generate_recommendation(input_text)
        
        confidence = recommendation['confidence_score']
        self.assertIsInstance(confidence, float)
        self.assertGreaterEqual(confidence, 0.0)
        self.assertLessEqual(confidence, 1.0)

if __name__ == '__main__':
    unittest.main() 