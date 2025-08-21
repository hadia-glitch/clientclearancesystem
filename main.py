#!/usr/bin/env python3
"""
AI-Based Recommendation System for Client Clearance
Main application entry point
"""

import sys
import os
import argparse
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.cli.interface import CLIInterface
from src.engine.recommendation_engine import RecommendationEngine
from src.data.dataset_generator import DatasetGenerator
from src.utils.formatter import RecommendationFormatter

def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(
        description="AI-Based Recommendation System for Client Clearance",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Interactive mode
  python main.py --batch           # Run batch analysis
  python main.py --generate-data   # Generate dataset
  python main.py --test            # Run test scenarios
        """
    )
    
    parser.add_argument(
        '--batch',
        action='store_true',
        help='Run batch analysis on sample data'
    )
    
    parser.add_argument(
        '--dataset-info',
        action='store_true',
        help='Show dataset information'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run test scenarios'
    )
    
    parser.add_argument(
        '--input',
        type=str,
        help='Provide input text for analysis'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        help='Output file for recommendation (JSON format)'
    )
    
    args = parser.parse_args()
    
    # Initialize components
    engine = RecommendationEngine()
    formatter = RecommendationFormatter()
    dataset_loader = DatasetGenerator()
    
    if args.dataset_info:
        print("Loading dataset information...")
        try:
            stats = dataset_loader.get_dataset_stats()
            print(f"Dataset loaded successfully!")
            print(f"Total entries: {stats['total_entries']}")
            print(f"Platform distribution: {stats['platform_distribution']}")
            print(f"Portability distribution: {stats['portability_distribution']}")
            print(f"Notification distribution: {stats['notification_distribution']}")
        except Exception as e:
            print(f"Error loading dataset: {e}")
        return
    
    if args.test:
        print("Running test scenarios...")
        test_scenarios = [
            "I need an online store to sell my products",
            "I want a mobile app for food delivery",
            "I need a patient management system for my clinic",
            "I want an e-learning platform for my courses",
            "I need a logistics tracking system",
            "I want a banking app for my customers",
            "I need a property listing website",
            "I want a desktop app for project management",
            "I need something to help manage my business",
            "I want to digitize my operations"
        ]
        
        results = []
        for i, scenario in enumerate(test_scenarios, 1):
            print(f"\nTest {i}: {scenario}")
            recommendation = engine.generate_recommendation(scenario)
            summary = formatter.format_summary(recommendation)
            print(summary)
            results.append(recommendation)
        
        # Calculate test statistics
        platforms = [r['platform_recommendation']['platform'] for r in results]
        costs = [r['cost_estimate']['total_cost'] for r in results]
        confidences = [r['confidence_score'] for r in results]
        
        print(f"\nTest Results Summary:")
        print(f"Average Cost: ${sum(costs)/len(costs):,.2f}")
        print(f"Average Confidence: {sum(confidences)/len(confidences):.2f}")
        print(f"Platform Distribution: {dict(zip(set(platforms), [platforms.count(p) for p in set(platforms)]))}")
        return
    
    if args.input:
        print(f"Analyzing input: {args.input}")
        recommendation = engine.generate_recommendation(args.input)
        
        if args.output:
            import json
            with open(args.output, 'w') as f:
                json.dump(recommendation, f, indent=2)
            print(f"Recommendation saved to {args.output}")
        else:
            formatted_output = formatter.format_recommendation(recommendation)
            print(formatted_output)
        return
    
    if args.batch:
        print("Running batch analysis...")
        try:
            requirements = dataset_loader.load_dataset()
            num_samples = min(10, len(requirements))
            
            results = []
            for req in requirements[:num_samples]:
                recommendation = engine.generate_recommendation(req['input_text'])
                results.append({
                    'input': req['input_text'],
                    'recommendation': recommendation
                })
            
            # Display summary
            platforms = [r['recommendation']['platform_recommendation']['platform'] for r in results]
            costs = [r['recommendation']['cost_estimate']['total_cost'] for r in results]
            confidences = [r['recommendation']['confidence_score'] for r in results]
            
            print(f"Batch Analysis Results:")
            print(f"Samples analyzed: {len(results)}")
            print(f"Average Cost: ${sum(costs)/len(costs):,.2f}")
            print(f"Average Confidence: {sum(confidences)/len(confidences):.2f}")
            print(f"Platform Distribution: {dict(zip(set(platforms), [platforms.count(p) for p in set(platforms)]))}")
            
        except Exception as e:
            print(f"Error in batch analysis: {e}")
        return
    
    # Default: Interactive mode
    print("🤖 AI-Based Recommendation System for Client Clearance")
    print("=" * 60)
    cli = CLIInterface()
    cli.run()

if __name__ == "__main__":
    main() 