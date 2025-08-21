"""
Dataset Loader for AI Recommendation System
Loads client requirements data from CSV file
"""

import pandas as pd
import json
from typing import List, Dict, Any
import os

class DatasetLoader:
    """Loads client requirements from CSV file."""
    
    def __init__(self, csv_file: str = 'src/data/client_requirements.csv'):
        self.csv_file = csv_file
        self.data = None
        
    def load_dataset(self) -> List[Dict[str, Any]]:
        """Load client requirements from CSV file."""
        if not os.path.exists(self.csv_file):
            raise FileNotFoundError(f"CSV file not found: {self.csv_file}")
            
        df = pd.read_csv(self.csv_file)
        return df.to_dict(orient='records')
    
    def get_dataset_stats(self) -> Dict[str, Any]:
        """Get statistics about the loaded dataset."""
        if self.data is None:
            self.data = self.load_dataset()
            
        df = pd.DataFrame(self.data)
        
        stats = {
            'total_entries': len(df),
            'platform_distribution': df['platform'].value_counts().to_dict(),
            'business_type_distribution': df['business_type'].value_counts().to_dict(),
            'portability_distribution': df['portability'].value_counts().to_dict(),
            'notification_distribution': df['notification_requirement'].value_counts().to_dict(),
            'budget_ranges': {
                'low': len(df[df['budget'] < 20000]),
                'medium': len(df[(df['budget'] >= 20000) & (df['budget'] < 40000)]),
                'high': len(df[df['budget'] >= 40000])
            },
            'timeline_ranges': {
                'short': len(df[df['timeline_weeks'] < 10]),
                'medium': len(df[(df['timeline_weeks'] >= 10) & (df['timeline_weeks'] < 20)]),
                'long': len(df[df['timeline_weeks'] >= 20])
            }
        }
        
        return stats
    
    def get_sample_requirements(self, n: int = 5) -> List[Dict[str, Any]]:
        """Get a sample of requirements for testing."""
        if self.data is None:
            self.data = self.load_dataset()
            
        import random
        return random.sample(self.data, min(n, len(self.data)))
    
    def get_requirements_by_platform(self, platform: str) -> List[Dict[str, Any]]:
        """Get all requirements for a specific platform."""
        if self.data is None:
            self.data = self.load_dataset()
            
        return [req for req in self.data if req['platform'] == platform]
    
    def get_requirements_by_business_type(self, business_type: str) -> List[Dict[str, Any]]:
        """Get all requirements for a specific business type."""
        if self.data is None:
            self.data = self.load_dataset()
            
        return [req for req in self.data if req['business_type'] == business_type]
    
    def get_mobile_requirements(self) -> List[Dict[str, Any]]:
        """Get all mobile app requirements."""
        return self.get_requirements_by_platform('mobile')
    
    def get_web_requirements(self) -> List[Dict[str, Any]]:
        """Get all web app requirements."""
        return self.get_requirements_by_platform('web')
    
    def get_desktop_requirements(self) -> List[Dict[str, Any]]:
        """Get all desktop app requirements."""
        return self.get_requirements_by_platform('desktop')
    
    def get_high_portability_requirements(self) -> List[Dict[str, Any]]:
        """Get requirements with high portability needs."""
        if self.data is None:
            self.data = self.load_dataset()
            
        return [req for req in self.data if req['portability'] == 'high']
    
    def get_major_notification_requirements(self) -> List[Dict[str, Any]]:
        """Get requirements with major notification needs."""
        if self.data is None:
            self.data = self.load_dataset()
            
        return [req for req in self.data if req['notification_requirement'] == 'major']

# Keep the old class name for backward compatibility
DatasetGenerator = DatasetLoader 