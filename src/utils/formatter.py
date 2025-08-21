"""
Formatter utilities for AI Recommendation System
Formats recommendations and analysis results for display
"""

from typing import Dict, List, Any
import json

class RecommendationFormatter:
    def __init__(self):
        """Initialize the formatter"""
        pass

    def format_recommendation(self, recommendation: Dict[str, Any]) -> str:
        """Format the complete recommendation for display"""
        output = []
        
        # Header
        output.append("=" * 60)
        output.append("🤖 AI RECOMMENDATION REPORT")
        output.append("=" * 60)
        output.append("")
        
        # Input Analysis
        analysis = recommendation['input_analysis']
        output.append("📋 INPUT ANALYSIS")
        output.append("-" * 30)
        output.append(f"Original Input: {analysis['original_text']}")
        platform_rec = recommendation['platform_recommendation']
     
        business_type = platform_rec['type']
        output.append(f"Detected Business Type: {business_type}")
        
        platform_pref, _ = analysis['platform_preference']
        output.append(f"Platform Preference: {platform_pref.title()}")
        
        if analysis['detected_features']:
            output.append(f"Detected Features: {', '.join(analysis['detected_features'])}")
        
        output.append("")
        
        # Platform Recommendation
        #platform_rec = recommendation['platform_recommendation']
     
        output.append(f"Reasoning: {platform_rec['reasoning']}")
        output.append("")
        
        # Feature Recommendations
        features_rec = recommendation['feature_recommendations']
        output.append("⚙️ FEATURE RECOMMENDATIONS")
        output.append("-" * 30)
        for i, feature in enumerate(features_rec, 1):
            output.append(f"{i}. {feature['feature'].replace('_', ' ').title()}")
            if feature['description']!='None':
                 output.append(f"   Description: {feature['description']}")
            output.append(f"   Priority: {feature['priority'].upper()}")
            output.append(f"   Estimated Effort: {feature['estimated_effort']} weeks")
            output.append(f"   Estimated Cost: ${feature['estimated_cost']:,}")
            output.append("")
        
        # Technology Stack
        tech_stack_rec = recommendation['tech_stack_recommendation']
        output.append("🛠️ TECHNOLOGY STACK")
        output.append("-" * 30)
        output.append(f"Recommended Stack: {tech_stack_rec['name']}")
        output.append(f"Description: {tech_stack_rec['description']}")
        output.append("")
        
        if tech_stack_rec['pros']:
            output.append("✅ Pros:")
            for pro in tech_stack_rec['pros']:
                output.append(f"   • {pro}")
            output.append("")
        
        if tech_stack_rec['cons']:
            output.append("❌ Cons:")
            for con in tech_stack_rec['cons']:
                output.append(f"   • {con}")
            output.append("")
        
        # Cost Estimate
        cost_estimate = recommendation['cost_estimate']
        output.append("💰 COST ESTIMATE")
        output.append("-" * 30)
        output.append(f"Base Platform Cost: ${cost_estimate['base_cost']:,}")
        output.append(f"Feature Development Cost: ${cost_estimate['feature_cost']:,}")
        output.append(f"Total Estimated Cost: ${cost_estimate['total_cost']:,}")
        output.append(f"Cost Range: {cost_estimate['cost_range']}")
        output.append("")
        
        # Timeline Estimate
        timeline_estimate = recommendation['timeline_estimate']
        output.append("⏰ TIMELINE ESTIMATE")
        output.append("-" * 30)
        output.append(f"Base Platform Timeline: {timeline_estimate['base_timeline']} weeks")
        output.append(f"Feature Development Timeline: {timeline_estimate['feature_timeline']} weeks")
        output.append(f"Total Estimated Timeline: {timeline_estimate['total_timeline']} weeks")
        output.append(f"Timeline Range: {timeline_estimate['timeline_range']}")
        output.append("")
        
        
        return "\n".join(output)

    def format_json(self, recommendation: Dict[str, Any]) -> str:
        """Format recommendation as JSON"""
        return json.dumps(recommendation, indent=2)

    def format_summary(self, recommendation: Dict[str, Any]) -> str:
        """Format a brief summary of the recommendation"""
        platform = recommendation['platform_recommendation']['platform']
        tech_stack = recommendation['tech_stack_recommendation']['name']
        total_cost = recommendation['cost_estimate']['total_cost']
        total_timeline = recommendation['timeline_estimate']['total_timeline']
        summary = f"""
QUICK SUMMARY:
• Platform: {platform.upper()}
• Tech Stack: {tech_stack}
• Estimated Cost: ${total_cost:,}
• Estimated Timeline: {total_timeline} weeks
"""
        return summary

    def format_comparison(self, recommendations: List[Dict[str, Any]]) -> str:
        """Format multiple recommendations for comparison"""
        output = []
        output.append("📊 RECOMMENDATION COMPARISON")
        output.append("=" * 60)
        output.append("")
        
        for i, rec in enumerate(recommendations, 1):
            output.append(f"OPTION {i}:")
            output.append("-" * 20)
            
            platform = rec['platform_recommendation']['platform']
            tech_stack = rec['tech_stack_recommendation']['name']
            cost = rec['cost_estimate']['total_cost']
            timeline = rec['timeline_estimate']['total_timeline']
            
            output.append(f"Platform: {platform.upper()}")
            output.append(f"Tech Stack: {tech_stack}")
            output.append(f"Cost: ${cost:,}")
            output.append(f"Timeline: {timeline} weeks")
            output.append("")
        
        return "\n".join(output) 