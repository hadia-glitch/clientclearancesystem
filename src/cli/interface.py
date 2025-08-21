"""
Command Line Interface for AI Recommendation System
Provides an interactive interface for users to get recommendations
"""

import click
import json
import sys
from typing import Dict, Any, List
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.text import Text
from rich import print as rprint

from ..engine.recommendation_engine import RecommendationEngine
from ..utils.formatter import RecommendationFormatter
from ..data.dataset_generator import DatasetLoader

class CLIInterface:
    def __init__(self):
        """Initialize the CLI interface"""
        self.console = Console()
        self.engine = RecommendationEngine()
        self.formatter = RecommendationFormatter()
        self.dataset_loader = DatasetLoader()

    def run(self):
        """Run the main CLI interface"""
        self.console.print(Panel.fit(
            "[bold blue]🤖 AI-Based Recommendation System[/bold blue]\n"
            "[italic]Get intelligent software recommendations for your business[/italic]",
            border_style="blue"
        ))
        
        while True:
            try:
                self._show_main_menu()
                choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4"])
                
                if choice == "1":
                    self._get_recommendation()
                elif choice == "2":
                    self._show_dataset_info()
                elif choice == "3":
                    self._show_examples()
                elif choice == "4":
                    self.console.print("[green]Thank you for using the AI Recommendation System![/green]")
                    break
                    
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Exiting...[/yellow]")
                break
            except Exception as e:
                self.console.print(f"[red]Error: {str(e)}[/red]")

    def _show_main_menu(self):
        """Display the main menu"""
        menu = """
[bold]Main Menu:[/bold]
1. Get Recommendation
2. Show Dataset Info
3. Show Examples
4. Exit
        """
        self.console.print(menu)

    def _get_additional_info(self, client_input=None) -> Dict[str, Any]:
        """Get additional information from user, only asking for missing info"""
        additional_info = {}
        # Use text analyzer to check for info in input
        from src.models.text_analyzer import TextAnalyzer
        analyzer = TextAnalyzer()
        analysis = analyzer.analyze_text(client_input) if client_input else {}
        # Portability
        portability = analysis.get('portability') if analysis else None
        if not portability or portability not in ['high', 'medium', 'low']:
            portability = Prompt.ask(
                "What is the portability requirement for your application?",
                choices=["high", "medium", "low"],
                default="medium"
            )
        additional_info['portability_requirement'] = portability
        #Type
        business_type = analysis['business_type'][0] if analysis else None
        if business_type == 'unknown' :
            business_type = Prompt.ask(
                "What is your business type?"
               
            )
        additional_info['business_type'] = business_type
        # Budget
        budget = None
        if analysis and analysis.get('budget_indicators'):
            budget = analysis['budget_indicators'].get('amount')
        if not budget:
            if Confirm.ask("Do you have a budget constraint?"):
                try:
                    budget = float(Prompt.ask("Budget (USD)"))
                except ValueError:
                    self.console.print("[red]Invalid budget amount.[/red]")
        if budget:
            additional_info['budget_constraint'] = budget
        # Timeline
        timeline = None
        if analysis and analysis.get('timeline_indicators'):
            timeline = analysis['timeline_indicators'].get('weeks')
        if not timeline:
            if Confirm.ask("Do you have a timeline constraint?"):
                try:
                    timeline = float(Prompt.ask("Timeline (weeks)"))
                except ValueError:
                    self.console.print("[red]Invalid timeline.[/red]")
        if timeline:
            additional_info['timeline_constraint'] = timeline
        access = Prompt.ask(
                "Do you want it to be accessible online or offline?",
                choices=["online","offline"],
               )
        additional_info['access_requirement'] = access
        return additional_info

    def _get_recommendation(self):
      """Get a single recommendation with interactive follow-up"""
      self.console.print("\n[bold cyan]📝 Enter your business requirements:[/bold cyan]")
      self.console.print("[italic]Describe what you need for your business...[/italic]")
      client_input = Prompt.ask("Your requirements")
      if not client_input.strip():
        self.console.print("[red]Please provide some requirements.[/red]")
        return

      additional_info = self._get_additional_info(client_input)
      recommendation = self.engine.generate_recommendation(client_input, additional_info)
      self._display_recommendation(recommendation)

      prev_recommendation = recommendation
      prev_input = client_input

      while True:
        followup = Prompt.ask(
            "[bold]Is there anything else you'd like me to take into consideration?[/bold] "
            "([italic]Type your clarification, or 'done' if satisfied[/italic])"
        )

        if followup.strip().lower() == 'done':
            self.console.print(
                "[bold green]Thank you for using the recommendation assistant! "
                "If you need a file, you can save this recommendation now.[/bold green]"
            )
            if Confirm.ask("Save this recommendation to a file?"):
                self._save_recommendation(prev_recommendation)
            break

        # Append new requirement
        client_input = prev_input + " " + followup
        

        with self.console.status("[bold green]Re-analyzing your updated requirements..."):
            new_recommendation = self.engine.generate_recommendation(client_input, additional_info)

        prev_platform = prev_recommendation['platform_recommendation']['platform']
        curr_platform = new_recommendation['platform_recommendation']['platform']

        if prev_platform == curr_platform:
            self.console.print(
                f"[yellow]Your new requirement had been incorporated into the "
                f"previous recommendation i.e  {curr_platform.upper()}.[/yellow]"
            )
        else:
            self.console.print(
                f"[green]Your new requirement has changed the recommendation:[/green]\n"
                f"[cyan]• Platform changed from {prev_platform.upper()} to "
                f"{curr_platform.upper()}[/cyan]\n"
                f"[italic]{new_recommendation['platform_recommendation']['reasoning']}[/italic]"
            )
            self._display_recommendation(new_recommendation)

        # Update previous references for next loop
        prev_recommendation = new_recommendation
        prev_input = client_input


    def _display_recommendation(self, recommendation: Dict[str, Any]):
        """Display the recommendation in a formatted way"""
        # Show summary first
        summary = self.formatter.format_summary(recommendation)
        self.console.print(Panel(summary, title="[bold green]Quick Summary[/bold green]"))
    
        # Show full report
        full_report = self.formatter.format_recommendation(recommendation)
        self.console.print(full_report)

    def _save_recommendation(self, recommendation: Dict[str, Any]):
        """Save recommendation to a file"""
        try:
            filename = Prompt.ask("Enter filename", default="recommendation.json")
            if not filename.endswith('.json'):
                filename += '.json'
            
            with open(filename, 'w') as f:
                json.dump(recommendation, f, indent=2)
            
            self.console.print(f"[green]Recommendation saved to {filename}[/green]")
        except Exception as e:
            self.console.print(f"[red]Error saving file: {str(e)}[/red]")

    def _show_dataset_info(self):
        """Show dataset information from CSV file"""
        self.console.print("\n[bold cyan]📊 Dataset Information[/bold cyan]")
        
        try:
            # Load and show dataset statistics
            stats = self.dataset_loader.get_dataset_stats()
            
            self.console.print(f"[green]Dataset loaded successfully![/green]")
            self.console.print(f"Total entries: {stats['total_entries']}")
            
            # Show platform distribution
            platform_table = Table(title="Platform Distribution")
            platform_table.add_column("Platform", style="cyan")
            platform_table.add_column("Count", style="green")
            platform_table.add_column("Percentage", style="yellow")
            
            total = stats['total_entries']
            for platform, count in stats['platform_distribution'].items():
                percentage = (count / total) * 100
                platform_table.add_row(platform.upper(), str(count), f"{percentage:.1f}%")
            
            self.console.print(platform_table)
            
            # Show portability and notification statistics
            self.console.print(f"\n[bold]Portability Requirements:[/bold]")
            for level, count in stats['portability_distribution'].items():
                percentage = (count / total) * 100
                self.console.print(f"  {level.title()}: {count} ({percentage:.1f}%)")
            
            self.console.print(f"\n[bold]Notification Requirements:[/bold]")
            for level, count in stats['notification_distribution'].items():
                percentage = (count / total) * 100
                self.console.print(f"  {level.title()}: {count} ({percentage:.1f}%)")
                
        except Exception as e:
            self.console.print(f"[red]Error loading dataset: {str(e)}[/red]")
            self.console.print("[yellow]The CSV dataset file may not exist or be accessible.[/yellow]")

    def _show_examples(self):
        """Show example inputs and their recommendations"""
        examples = [
            "I need an online store to sell my products",
            "I want a mobile app for food delivery",
            "I need a patient management system for my clinic",
            "I want an e-learning platform for my courses",
            "I need a logistics tracking system"
        ]
        
        self.console.print("\n[bold cyan]📝 Example Inputs:[/bold cyan]")
        for i, example in enumerate(examples, 1):
            self.console.print(f"{i}. {example}")
        
        self.console.print("\n[italic]Try these examples to see how the system works![/italic]")

@click.command()
@click.option('--dataset-info', is_flag=True, help='Show dataset information')
@click.option('--examples', is_flag=True, help='Show examples')
def main(dataset_info, examples):
    """AI-Based Recommendation System CLI"""
    cli = CLIInterface()
    
    if dataset_info:
        cli._show_dataset_info()
    elif examples:
        cli._show_examples()
    else:
        cli.run()

if __name__ == "__main__":
    main()
