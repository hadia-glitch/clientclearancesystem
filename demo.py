#!/usr/bin/env python3
"""
Demo script for AI-Based Recommendation System
Showcases the system's capabilities with various examples
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.engine.recommendation_engine import RecommendationEngine
from src.utils.formatter import RecommendationFormatter
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import time

def run_demo():
    """Run the demo with various examples"""
    console = Console()
    
    # Initialize components
    engine = RecommendationEngine()
    formatter = RecommendationFormatter()
    
    # Demo examples
    examples = [
        {
            "title": "🏪 E-commerce Store",
            "input": "I need an online store to sell my products with inventory management and payment processing",
            "description": "Clear retail business requirements"
        },
        {
            "title": "🍕 Food Delivery App",
            "input": "I want a mobile app for food delivery with real-time tracking and online ordering",
            "description": "Mobile app for restaurant business"
        },
        {
            "title": "🏥 Healthcare Management",
            "input": "I need a patient management system for my clinic with appointment scheduling and medical records",
            "description": "Healthcare business with compliance requirements"
        },
        {
            "title": "📚 E-learning Platform",
            "input": "I want an e-learning platform for my courses with video streaming and progress tracking",
            "description": "Education business with content delivery"
        },
        {
            "title": "🚚 Logistics Tracking",
            "input": "I need a logistics tracking system with route optimization and real-time delivery updates",
            "description": "Logistics business with complex tracking"
        },
        {
            "title": "💳 Banking App",
            "input": "I want a banking app for my customers with secure transactions and account management",
            "description": "Finance business with security requirements"
        },
        {
            "title": "🏠 Real Estate Listings",
            "input": "I need a property listing website with search filters and virtual tours",
            "description": "Real estate business with property showcase"
        },
        {
            "title": "💼 Consulting Management",
            "input": "I want a desktop app for project management with time tracking and client billing",
            "description": "Consulting business with project management"
        },
        {
            "title": "❓ Vague Requirements",
            "input": "I need something to help manage my business operations",
            "description": "Unclear requirements needing clarification"
        }
    ]
    
    console.print(Panel.fit(
        "[bold blue]🤖 AI-Based Recommendation System Demo[/bold blue]\n"
        "[italic]Showcasing intelligent software recommendations[/italic]",
        border_style="blue"
    ))
    
    results = []
    
    for i, example in enumerate(examples, 1):
        console.print(f"\n[bold cyan]Example {i}: {example['title']}[/bold cyan]")
        console.print(f"[italic]{example['description']}[/italic]")
        console.print(f"[yellow]Input:[/yellow] {example['input']}")
        
        # Generate recommendation
        with console.status(f"[bold green]Analyzing example {i}..."):
            recommendation = engine.generate_recommendation(example['input'])
        
        # Show summary
        summary = formatter.format_summary(recommendation)
        console.print(Panel(summary, title="[bold green]Quick Summary[/bold green]"))
        
        # Store results for comparison
        results.append({
            'title': example['title'],
            'input': example['input'],
            'recommendation': recommendation
        })
        
        # Add delay for readability
        time.sleep(1)
    
    # Show comparison table
    console.print("\n[bold cyan]📊 Comparison Table[/bold cyan]")
    table = Table(title="Demo Results Comparison")
    table.add_column("Example", style="cyan")
    table.add_column("Platform", style="green")
    table.add_column("Tech Stack", style="yellow")
    table.add_column("Cost", style="red")
    table.add_column("Timeline", style="blue")
    table.add_column("Confidence", style="magenta")
    
    for result in results:
        rec = result['recommendation']
        platform = rec['platform_recommendation']['platform']
        tech_stack = rec['tech_stack_recommendation']['name']
        cost = rec['cost_estimate']['total_cost']
        timeline = rec['timeline_estimate']['total_timeline']
        confidence = rec['confidence_score']
        
        # Truncate tech stack name for display
        tech_stack_short = tech_stack[:30] + "..." if len(tech_stack) > 30 else tech_stack
        
        table.add_row(
            result['title'],
            platform.upper(),
            tech_stack_short,
            f"${cost:,}",
            f"{timeline} weeks",
            f"{confidence:.2f}"
        )
    
    console.print(table)
    
    # Show statistics
    platforms = [r['recommendation']['platform_recommendation']['platform'] for r in results]
    costs = [r['recommendation']['cost_estimate']['total_cost'] for r in results]
    confidences = [r['recommendation']['confidence_score'] for r in results]
    
    console.print(f"\n[bold]Demo Statistics:[/bold]")
    console.print(f"Total Examples: {len(results)}")
    console.print(f"Average Cost: ${sum(costs)/len(costs):,.2f}")
    console.print(f"Average Confidence: {sum(confidences)/len(confidences):.2f}")
    console.print(f"Platform Distribution: {dict(zip(set(platforms), [platforms.count(p) for p in set(platforms)]))}")
    
    # Show detailed analysis for one example
    console.print(f"\n[bold cyan]🔍 Detailed Analysis Example[/bold cyan]")
    detailed_example = results[0]  # First example
    detailed_report = formatter.format_recommendation(detailed_example['recommendation'])
    console.print(detailed_report)
    
    console.print(f"\n[bold green]✅ Demo completed successfully![/bold green]")
    console.print(f"[italic]Try running 'python main.py' for interactive mode[/italic]")

def run_quick_demo():
    """Run a quick demo with just a few examples"""
    console = Console()
    
    engine = RecommendationEngine()
    formatter = RecommendationFormatter()
    
    quick_examples = [
        "I need an online store to sell my products",
        "I want a mobile app for food delivery",
        "I need a patient management system for my clinic"
    ]
    
    console.print(Panel.fit(
        "[bold blue]🚀 Quick Demo[/bold blue]\n"
        "[italic]Fast demonstration of key features[/italic]",
        border_style="blue"
    ))
    
    for i, example in enumerate(quick_examples, 1):
        console.print(f"\n[bold]Example {i}:[/bold] {example}")
        
        recommendation = engine.generate_recommendation(example)
        summary = formatter.format_summary(recommendation)
        console.print(summary)
    
    console.print(f"\n[bold green]✅ Quick demo completed![/bold green]")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Recommendation System Demo")
    parser.add_argument('--quick', action='store_true', help='Run quick demo')
    
    args = parser.parse_args()
    
    if args.quick:
        run_quick_demo()
    else:
        run_demo() 