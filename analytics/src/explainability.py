"""
Model Explainability Module
Provides interpretations of attrition risk model predictions
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.utils import (
    print_section_header,
    save_dataframe,
    OUTPUT_DIR
)


def extract_logistic_coefficients(model, features: list) -> pd.DataFrame:
    """
    Extract and interpret logistic regression coefficients
    
    Args:
        model: Trained logistic regression model
        features: List of feature names
    
    Returns:
        Dataframe with feature importance
    """
    print("\nExtracting model coefficients...")
    
    # Get coefficients
    coefficients = model.coef_[0]
    
    # Create dataframe
    coef_df = pd.DataFrame({
        'feature': features,
        'coefficient': coefficients,
        'abs_coefficient': np.abs(coefficients)
    })
    
    # Sort by absolute value
    coef_df = coef_df.sort_values('abs_coefficient', ascending=False)
    
    # Add interpretation
    coef_df['effect'] = coef_df['coefficient'].apply(
        lambda x: 'Increases Risk' if x > 0 else 'Decreases Risk'
    )
    
    # Add magnitude category
    coef_df['importance'] = pd.cut(
        coef_df['abs_coefficient'],
        bins=[0, 0.1, 0.3, 1.0, 100],
        labels=['Low', 'Medium', 'High', 'Very High']
    )
    
    print(f"  ✓ Analyzed {len(coef_df)} features")
    
    return coef_df


def plot_feature_importance(coef_df: pd.DataFrame, top_n: int = 20) -> None:
    """
    Create visualization of feature importance
    
    Args:
        coef_df: Dataframe with coefficients
        top_n: Number of top features to plot
    """
    print(f"\nCreating feature importance plot (top {top_n})...")
    
    # Select top features
    top_features = coef_df.head(top_n).copy()
    
    # Create figure
    plt.figure(figsize=(12, 8))
    
    # Create color map (red for increases risk, blue for decreases)
    colors = ['#d62728' if x > 0 else '#1f77b4' for x in top_features['coefficient']]
    
    # Horizontal bar plot
    plt.barh(range(len(top_features)), top_features['coefficient'], color=colors)
    plt.yticks(range(len(top_features)), top_features['feature'])
    plt.xlabel('Coefficient (Impact on Attrition Risk)', fontsize=12)
    plt.ylabel('Feature', fontsize=12)
    plt.title(f'Top {top_n} Features - Attrition Risk Model', fontsize=14, fontweight='bold')
    plt.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
    plt.grid(axis='x', alpha=0.3)
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#d62728', label='Increases Risk'),
        Patch(facecolor='#1f77b4', label='Decreases Risk')
    ]
    plt.legend(handles=legend_elements, loc='lower right')
    
    plt.tight_layout()
    
    # Save plot
    plot_path = os.path.join(OUTPUT_DIR, 'feature_importance.png')
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Saved plot: {plot_path}")


def generate_shap_analysis(model, X_sample: pd.DataFrame, features: list) -> None:
    """
    Generate SHAP analysis for model interpretability
    
    Args:
        model: Trained model
        X_sample: Sample of features for SHAP analysis
        features: List of feature names
    """
    print("\nGenerating SHAP analysis...")
    
    try:
        import shap
        
        # Create explainer
        explainer = shap.LinearExplainer(model, X_sample)
        
        # Calculate SHAP values
        shap_values = explainer.shap_values(X_sample)
        
        # Create summary plot
        plt.figure(figsize=(12, 8))
        shap.summary_plot(
            shap_values, 
            X_sample, 
            feature_names=features,
            show=False,
            max_display=20
        )
        
        plot_path = os.path.join(OUTPUT_DIR, 'shap_summary.png')
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  ✓ Saved SHAP plot: {plot_path}")
        
    except ImportError:
        print("  ⚠ SHAP library not available, skipping SHAP analysis")
    except Exception as e:
        print(f"  ⚠ SHAP analysis failed: {str(e)}")


def create_interpretation_guide(coef_df: pd.DataFrame) -> str:
    """
    Create human-readable interpretation guide
    
    Args:
        coef_df: Dataframe with coefficients
    
    Returns:
        Formatted interpretation text
    """
    guide = []
    guide.append("=" * 60)
    guide.append("MODEL INTERPRETATION GUIDE")
    guide.append("=" * 60)
    guide.append("\nTop Risk-Increasing Factors:")
    
    # Top 5 risk increasers
    top_risk = coef_df[coef_df['coefficient'] > 0].head(5)
    for idx, row in top_risk.iterrows():
        guide.append(f"  • {row['feature']}: +{row['coefficient']:.4f}")
    
    guide.append("\nTop Risk-Decreasing Factors:")
    
    # Top 5 risk decreasers
    top_protect = coef_df[coef_df['coefficient'] < 0].head(5)
    for idx, row in top_protect.iterrows():
        guide.append(f"  • {row['feature']}: {row['coefficient']:.4f}")
    
    guide.append("\n" + "=" * 60)
    guide.append("\nKey Insights:")
    guide.append("  1. Compensation factors play a significant role in attrition")
    guide.append("  2. Workload metrics indicate burnout risk")
    guide.append("  3. Performance ratings are predictive of retention")
    guide.append("  4. Tenure and career progression affect likelihood to stay")
    guide.append("=" * 60)
    
    return "\n".join(guide)


def analyze_risk_drivers_by_segment(risk_report: pd.DataFrame, 
                                    coef_df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze risk drivers for different employee segments
    
    Args:
        risk_report: Employee risk scores
        coef_df: Feature coefficients
    
    Returns:
        Dataframe with segment analysis
    """
    print("\nAnalyzing risk drivers by segment...")
    
    segments = []
    
    # Analyze high-risk employees by department
    high_risk = risk_report[risk_report['risk_band'] == 'High']
    
    dept_summary = high_risk.groupby('department').agg({
        'employee_id': 'count',
        'attrition_risk_score': 'mean',
        'tenure_months': 'mean',
        'base_salary': 'mean'
    }).reset_index()
    
    dept_summary.columns = [
        'department', 'high_risk_count', 'avg_risk_score',
        'avg_tenure', 'avg_salary'
    ]
    
    dept_summary = dept_summary.sort_values('high_risk_count', ascending=False)
    
    print(f"  ✓ Analyzed {len(dept_summary)} departments")
    
    return dept_summary


def generate_explainability_report() -> None:
    """
    Main explainability pipeline
    """
    print_section_header("Model Explainability Analysis")
    
    # Load model artifacts
    model_path = os.path.join(OUTPUT_DIR, 'attrition_model.joblib')
    scaler_path = os.path.join(OUTPUT_DIR, 'feature_scaler.joblib')
    features_path = os.path.join(OUTPUT_DIR, 'model_features.joblib')
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            "Model not found. Run train_model.py first."
        )
    
    print("\nLoading model artifacts...")
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    features = joblib.load(features_path)
    print(f"  ✓ Loaded model with {len(features)} features")
    
    # Extract coefficients
    coef_df = extract_logistic_coefficients(model, features)
    
    # Save coefficients
    save_dataframe(coef_df, 'logistic_coefficients.csv')
    
    # Print top features
    print("\n" + "-" * 60)
    print("TOP 10 RISK-INCREASING FEATURES:")
    print("-" * 60)
    top_risk = coef_df[coef_df['coefficient'] > 0].head(10)
    for idx, row in top_risk.iterrows():
        print(f"  {row['feature']:35s}: +{row['coefficient']:7.4f} ({row['importance']})")
    
    print("\n" + "-" * 60)
    print("TOP 10 RISK-DECREASING FEATURES:")
    print("-" * 60)
    top_protect = coef_df[coef_df['coefficient'] < 0].head(10)
    for idx, row in top_protect.iterrows():
        print(f"  {row['feature']:35s}: {row['coefficient']:7.4f} ({row['importance']})")
    print("-" * 60)
    
    # Create visualization
    plot_feature_importance(coef_df, top_n=20)
    
    # Load feature data for SHAP (sample for efficiency)
    feature_path = os.path.join(OUTPUT_DIR, 'feature_table.csv')
    if os.path.exists(feature_path):
        df = pd.read_csv(feature_path)
        active_df = df[df['employment_status'] == 'Active']
        
        if len(active_df) > 500:
            sample_df = active_df.sample(n=500, random_state=42)
        else:
            sample_df = active_df
        
        X_sample = sample_df[features].fillna(sample_df[features].median())
        X_sample = X_sample.replace([np.inf, -np.inf], np.nan)
        X_sample = X_sample.fillna(X_sample.median())
        X_sample_scaled = scaler.transform(X_sample)
        X_sample_scaled = pd.DataFrame(X_sample_scaled, columns=features)
        
        # Generate SHAP analysis
        generate_shap_analysis(model, X_sample_scaled, features)
    
    # Load risk report for segment analysis
    risk_report_path = os.path.join(OUTPUT_DIR, 'employee_risk_scores.csv')
    if os.path.exists(risk_report_path):
        risk_report = pd.read_csv(risk_report_path)
        dept_analysis = analyze_risk_drivers_by_segment(risk_report, coef_df)
        save_dataframe(dept_analysis, 'department_risk_analysis.csv')
    
    # Create interpretation guide
    interpretation = create_interpretation_guide(coef_df)
    print("\n" + interpretation)
    
    # Save interpretation to file
    guide_path = os.path.join(OUTPUT_DIR, 'interpretation_guide.txt')
    with open(guide_path, 'w') as f:
        f.write(interpretation)
    print(f"\n✓ Saved interpretation guide: {guide_path}")
    
    print("\n" + "=" * 60)
    print("EXPLAINABILITY ANALYSIS COMPLETE")
    print("=" * 60)
    print("\nOutputs:")
    print("  - logistic_coefficients.csv: Feature importance scores")
    print("  - feature_importance.png: Visualization of top features")
    print("  - shap_summary.png: SHAP value summary (if available)")
    print("  - interpretation_guide.txt: Human-readable guide")
    print("  - department_risk_analysis.csv: Risk by department")


if __name__ == "__main__":
    generate_explainability_report()
    
    print("\n✓ Explainability analysis complete!")
