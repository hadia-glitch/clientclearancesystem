# AI-Based Recommendation System Documentation

## Overview

The AI-Based Recommendation System for Client Clearance is an intelligent system that analyzes client requirements and provides comprehensive software development recommendations. It uses Natural Language Processing (NLP) to understand client input and generates platform, feature, and technology stack recommendations.

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Installation](#installation)
3. [Usage](#usage)
4. [API Reference](#api-reference)
5. [Testing](#testing)
6. [Dataset](#dataset)
7. [Contributing](#contributing)

## System Architecture

### Components

1. **Text Analyzer** (`src/models/text_analyzer.py`)
   - Analyzes client input using NLP
   - Extracts business type, platform preferences, and features
   - Calculates clarity scores and generates clarification questions

2. **Recommendation Engine** (`src/engine/recommendation_engine.py`)
   - Generates platform recommendations (Mobile/Web/Desktop)
   - Suggests relevant features based on business type
   - Recommends technology stacks
   - Estimates costs and timelines

3. **Dataset Generator** (`src/data/dataset_generator.py`)
   - Creates dummy client requirements data
   - Supports multiple business types
   - Generates both clear and vague inputs for training

4. **CLI Interface** (`src/cli/interface.py`)
   - Interactive command-line interface
   - Batch analysis capabilities
   - Rich formatting and display

5. **Formatter** (`src/utils/formatter.py`)
   - Formats recommendations for display
   - Supports multiple output formats
   - Generates comparison reports

### Data Flow

```
Client Input → Text Analyzer → Recommendation Engine → Formatter → Output
     ↓              ↓                ↓              ↓
Clarification → Business Type → Platform/Features → Formatted Report
   Questions     Detection        Recommendations
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation Steps

1. Clone the repository:
```bash
git clone <repository-url>
cd rayonix
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download spaCy model:
```bash
python -m spacy download en_core_web_sm
```

4. Download NLTK data:
```python
import nltk
nltk.download('punkt')
```

### Verification

Run the test suite to verify installation:
```bash
python -m pytest tests/
```

## Usage

### Interactive Mode

Start the interactive CLI:
```bash
python main.py
```

### Command Line Options

```bash
# Generate dataset
python main.py --generate-data

# Run batch analysis
python main.py --batch

# Run test scenarios
python main.py --test

# Analyze specific input
python main.py --input "I need an online store" --output recommendation.json
```

### Programmatic Usage

```python
from src.engine.recommendation_engine import RecommendationEngine

# Initialize engine
engine = RecommendationEngine()

# Generate recommendation
recommendation = engine.generate_recommendation(
    "I need an online store to sell my products"
)

# Access results
platform = recommendation['platform_recommendation']['platform']
features = recommendation['feature_recommendations']
cost = recommendation['cost_estimate']['total_cost']
timeline = recommendation['timeline_estimate']['total_timeline']
```

## API Reference

### RecommendationEngine

#### `generate_recommendation(client_input: str, additional_info: Dict = None) -> Dict`

Generates a comprehensive recommendation based on client input.

**Parameters:**
- `client_input` (str): Client's business requirements
- `additional_info` (Dict, optional): Additional constraints (budget, timeline, etc.)

**Returns:**
- `Dict`: Complete recommendation with platform, features, tech stack, costs, and timeline

### TextAnalyzer

#### `analyze_text(text: str) -> Dict`

Analyzes input text and extracts key information.

**Parameters:**
- `text` (str): Input text to analyze

**Returns:**
- `Dict`: Analysis results including business type, clarity score, platform preference, etc.

#### `needs_clarification(analysis: Dict) -> bool`

Determines if input needs clarification.

**Parameters:**
- `analysis` (Dict): Text analysis results

**Returns:**
- `bool`: True if clarification is needed

#### `generate_clarification_questions(analysis: Dict) -> List[str]`

Generates follow-up questions for vague inputs.

**Parameters:**
- `analysis` (Dict): Text analysis results

**Returns:**
- `List[str]`: List of clarification questions

### DatasetGenerator

#### `generate_client_requirements(num_samples: int = 150) -> List[Dict]`

Generates dummy client requirements dataset.

**Parameters:**
- `num_samples` (int): Number of samples to generate

**Returns:**
- `List[Dict]`: List of client requirement dictionaries

#### `save_dataset(requirements: List[Dict], filename: str = 'client_requirements.json')`

Saves dataset to JSON and CSV files.

**Parameters:**
- `requirements` (List[Dict]): Dataset to save
- `filename` (str): Base filename

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_recommendation_engine.py

# Run with verbose output
python -m pytest -v tests/
```

### Test Coverage

The test suite covers:
- Text analysis functionality
- Recommendation generation
- Platform and feature detection
- Cost and timeline estimation
- Formatter utilities
- CLI interface

### Example Test Scenarios

1. **Clear Input Test**: "I need an online store to sell my products"
   - Expected: High clarity score, retail business type, web platform

2. **Vague Input Test**: "I need something to help manage my business"
   - Expected: Low clarity score, clarification questions generated

3. **Mobile App Test**: "I want a food delivery app"
   - Expected: Restaurant business type, mobile platform, delivery features

## Dataset

### Business Types Supported

1. **Retail**: Online stores, marketplaces, e-commerce
2. **Restaurant**: Food delivery, menu management, reservations
3. **Healthcare**: Patient management, appointments, medical records
4. **Education**: Learning platforms, course management, student portals
5. **Logistics**: Delivery tracking, route optimization, warehouse management
6. **Finance**: Banking apps, financial management, investment tracking
7. **Real Estate**: Property listings, virtual tours, lead management
8. **Consulting**: Project management, time tracking, client billing

### Dataset Statistics

- **Total Samples**: 150+ (configurable)
- **Business Types**: 8 different categories
- **Platforms**: Mobile, Web, Desktop
- **Features**: 40+ different feature types
- **Tech Stacks**: 10+ technology combinations

### Dataset Generation

```python
from src.data.dataset_generator import DatasetGenerator

generator = DatasetGenerator()
requirements = generator.generate_client_requirements(200)
generator.save_dataset(requirements)
stats = generator.get_dataset_stats(requirements)
```

## Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Install development dependencies
4. Run tests before making changes
5. Submit a pull request

### Code Style

- Follow PEP 8 guidelines
- Use type hints for function parameters
- Add docstrings to all functions and classes
- Write unit tests for new features

### Adding New Business Types

1. Update `business_keywords` in `TextAnalyzer`
2. Add business features in `RecommendationEngine`
3. Update platform mapping logic
4. Add test cases
5. Update documentation

### Adding New Features

1. Define feature keywords in `TextAnalyzer`
2. Add feature descriptions in `RecommendationEngine`
3. Update cost and timeline estimation
4. Add test cases
5. Update documentation

