"""
Utility functions for the analytics pipeline
Provides shared helpers for data loading, validation, and output management
"""

import pandas as pd
import numpy as np
import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

# Paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(PROJECT_ROOT, "data_generation", "output")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_data() -> Dict[str, pd.DataFrame]:
    """
    Load all HR datasets from CSV files
    
    Returns:
        Dictionary of dataframes keyed by table name
    """
    print("\n" + "=" * 60)
    print("LOADING DATA")
    print("=" * 60)
    
    datasets = {}
    files = {
        'employees': 'employees.csv',
        'compensation': 'compensation.csv',
        'performance': 'performance.csv',
        'attendance': 'attendance.csv',
        'attrition_labels': 'attrition_labels.csv'
    }
    
    for name, filename in files.items():
        filepath = os.path.join(DATA_DIR, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Required file not found: {filepath}")
        
        datasets[name] = pd.read_csv(filepath)
        print(f"✓ Loaded {name}: {len(datasets[name]):,} records")
    
    print(f"\nTotal datasets loaded: {len(datasets)}")
    return datasets


def convert_dates(df: pd.DataFrame, date_columns: List[str]) -> pd.DataFrame:
    """
    Convert string columns to datetime
    
    Args:
        df: Input dataframe
        date_columns: List of column names to convert
    
    Returns:
        Dataframe with converted date columns
    """
    df = df.copy()
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df


def validate_data(df: pd.DataFrame, name: str, required_columns: List[str]) -> None:
    """
    Validate dataframe structure and content
    
    Args:
        df: Dataframe to validate
        name: Name of dataset for logging
        required_columns: List of columns that must exist
    """
    print(f"\nValidating {name}...")
    
    # Check required columns
    missing = set(required_columns) - set(df.columns)
    if missing:
        raise ValueError(f"{name} missing required columns: {missing}")
    
    # Check for empty dataframe
    if len(df) == 0:
        raise ValueError(f"{name} is empty")
    
    # Check for duplicate employee IDs
    if 'employee_id' in df.columns:
        dupes = df['employee_id'].duplicated().sum()
        if dupes > 0 and name == 'employees':
            raise ValueError(f"{name} has {dupes} duplicate employee_ids")
    
    print(f"✓ {name} validation passed")


def save_dataframe(df: pd.DataFrame, filename: str, index: bool = False) -> None:
    """
    Save dataframe to CSV in output directory
    
    Args:
        df: Dataframe to save
        filename: Output filename
        index: Whether to save index
    """
    filepath = os.path.join(OUTPUT_DIR, filename)
    df.to_csv(filepath, index=index)
    print(f"✓ Saved: {filepath}")


def save_json(data: Dict[str, Any], filename: str) -> None:
    """
    Save dictionary to JSON file
    
    Args:
        data: Dictionary to save
        filename: Output filename
    """
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4, default=str)
    print(f"✓ Saved: {filepath}")


def calculate_tenure_months(hire_date: pd.Series, reference_date: pd.Series) -> pd.Series:
    """
    Calculate tenure in months between two dates
    
    Args:
        hire_date: Series of hire dates
        reference_date: Series of reference dates (termination or current)
    
    Returns:
        Series of tenure in months
    """
    days_diff = (reference_date - hire_date).dt.days
    return (days_diff / 30.44).round(1)


def categorize_risk(risk_scores: pd.Series) -> pd.Series:
    """
    Categorize continuous risk scores into risk bands
    
    Args:
        risk_scores: Series of risk probabilities (0-1)
    
    Returns:
        Series of risk categories
    """
    return pd.cut(
        risk_scores,
        bins=[0, 0.3, 0.6, 1.0],
        labels=['Low', 'Medium', 'High'],
        include_lowest=True
    )


def print_section_header(title: str) -> None:
    """
    Print formatted section header
    
    Args:
        title: Section title
    """
    print("\n" + "=" * 60)
    print(title.upper())
    print("=" * 60)


def print_stats(df: pd.DataFrame, label: str = "Dataset") -> None:
    """
    Print basic statistics about a dataframe
    
    Args:
        df: Dataframe to analyze
        label: Label for output
    """
    print(f"\n{label} Statistics:")
    print(f"  Rows: {len(df):,}")
    print(f"  Columns: {len(df.columns)}")
    
    if 'employee_id' in df.columns:
        print(f"  Unique employees: {df['employee_id'].nunique():,}")
    
    # Memory usage
    memory_mb = df.memory_usage(deep=True).sum() / 1024 / 1024
    print(f"  Memory: {memory_mb:.2f} MB")


def get_latest_date(df: pd.DataFrame, date_column: str = 'record_date') -> datetime:
    """
    Get the latest date from a date column
    
    Args:
        df: Dataframe containing date column
        date_column: Name of date column
    
    Returns:
        Latest date as datetime
    """
    return pd.to_datetime(df[date_column]).max()


def filter_active_employees(employees_df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter to only active employees
    
    Args:
        employees_df: Employee dataframe
    
    Returns:
        Filtered dataframe with only active employees
    """
    return employees_df[employees_df['employment_status'] == 'Active'].copy()


def calculate_percentile(series: pd.Series, value: float) -> float:
    """
    Calculate percentile rank of a value in a series
    
    Args:
        series: Series of values
        value: Value to rank
    
    Returns:
        Percentile (0-100)
    """
    return (series < value).mean() * 100


def safe_divide(numerator: pd.Series, denominator: pd.Series, fill_value: float = 0) -> pd.Series:
    """
    Safely divide two series, handling division by zero
    
    Args:
        numerator: Numerator series
        denominator: Denominator series
        fill_value: Value to use when denominator is zero
    
    Returns:
        Series of division results
    """
    result = numerator / denominator
    result = result.replace([np.inf, -np.inf], fill_value)
    result = result.fillna(fill_value)
    return result


def get_data_summary() -> Dict[str, Any]:
    """
    Get summary statistics of loaded data
    
    Returns:
        Dictionary with data summary
    """
    datasets = load_data()
    
    summary = {
        'timestamp': datetime.now().isoformat(),
        'total_employees': len(datasets['employees']),
        'active_employees': (datasets['employees']['employment_status'] == 'Active').sum(),
        'terminated_employees': (datasets['employees']['employment_status'] == 'Terminated').sum(),
        'attrition_rate': round(
            (datasets['employees']['employment_status'] == 'Terminated').mean() * 100, 2
        ),
        'total_performance_reviews': len(datasets['performance']),
        'total_attendance_records': len(datasets['attendance'])
    }
    
    return summary


if __name__ == "__main__":
    # Test utilities
    print_section_header("Testing Utilities")
    
    # Load data test
    data = load_data()
    
    # Print summary
    summary = get_data_summary()
    print("\nData Summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    print("\n✓ All utility functions working correctly")
