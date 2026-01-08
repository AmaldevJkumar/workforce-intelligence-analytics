# 🎯 Workforce Intelligence & Attrition Risk Platform

A complete, production-ready analytics platform for predicting employee attrition risk using machine learning. Built for HR teams and data analysts to proactively manage retention and reduce workforce costs.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-production--ready-brightgreen.svg)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Documentation](#documentation)
- [Model Performance](#model-performance)
- [Contributing](#contributing)
- [License](#license)

---

## 🔍 Overview

The Workforce Intelligence & Attrition Risk Platform is an end-to-end solution for:

1. **Generating synthetic HR data** for development and testing
2. **Building a data warehouse** with raw and analytics schemas
3. **Engineering predictive features** from employee, compensation, performance, and attendance data
4. **Training interpretable ML models** to predict attrition risk
5. **Scoring active employees** and identifying high-risk individuals
6. **Explaining model predictions** with feature importance and SHAP values
7. **Generating actionable insights** for HR leadership

### Why This Matters

- **18% annual attrition** costs mid-size companies **$10M-15M** per year
- **Early identification** of at-risk employees enables proactive retention
- **Data-driven insights** help HR prioritize high-value interventions
- **Interpretable models** build trust with stakeholders

---

## ✨ Features

### Data Generation
- Synthetic dataset generator creates **realistic, internally consistent** HR data
- 5 datasets: employees, compensation, performance, attendance, attrition labels
- Configurable parameters (employee count, departments, date ranges)
- Realistic attrition patterns based on multiple risk factors

### Data Warehouse
- PostgreSQL schemas (raw, analytics) with proper constraints
- SQL scripts for table creation and data loading
- Referential integrity and data quality checks
- Ready for production HRIS integration

### Analytics Pipeline
- **Data Preparation**: Joins, cleaning, validation
- **Feature Engineering**: 40+ predictive features across 6 categories
- **Model Training**: Logistic regression with class balancing
- **Employee Scoring**: Risk predictions for all active employees
- **Explainability**: Coefficient analysis and SHAP visualizations

### Insights & Reporting
- Pre-built HR weekly report template
- Comprehensive retention recommendations
- Data dictionary and metric definitions
- Risk distribution analysis by department

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Data Generation Layer                     │
│  Python script generates 5 synthetic CSV datasets           │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                   Data Warehouse Layer                       │
│  PostgreSQL with raw and analytics schemas                  │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                    Analytics Layer                           │
│                                                              │
│  1. Data Prep     → Joins, cleaning, validation            │
│  2. Feature Eng   → 40+ predictive features                │
│  3. Model Train   → Logistic regression (AUC: 0.78-0.85)   │
│  4. Score         → Risk predictions for active employees   │
│  5. Explain       → Feature importance + SHAP              │
│                                                              │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                    Insights Layer                            │
│  Risk reports, department analysis, retention plans         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **PostgreSQL 12+** (optional, for warehouse)
- **Git**

### 5-Minute Setup

```bash
# 1. Clone repository
git clone https://github.com/yourusername/workforce-intelligence-platform.git
cd workforce-intelligence-platform

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate synthetic data
python data_generation/generate_synthetic_data.py

# 5. Run analytics pipeline
cd analytics
python src/data_prep.py
python src/feature_engineering.py
python src/train_model.py
python src/score_employees.py
python src/explainability.py
```

**Result**: You now have:
- ✅ 5 CSV datasets with 2,000 synthetic employees
- ✅ Trained attrition prediction model (AUC ~0.80)
- ✅ Risk scores for all active employees
- ✅ Feature importance visualizations
- ✅ Actionable insights reports

---

## 📦 Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/workforce-intelligence-platform.git
cd workforce-intelligence-platform
```

### Step 2: Set Up Python Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: (Optional) Set Up PostgreSQL Warehouse

```bash
# Start PostgreSQL service
# Then connect via psql or pgAdmin

# Run setup scripts
psql -U postgres -f warehouse/01_create_schemas.sql
psql -U postgres -f warehouse/02_create_tables.sql

# Update file paths in 03_load_data.sql, then:
psql -U postgres -f warehouse/03_load_data.sql
```

---

## 💻 Usage

### Generate Synthetic Data

```bash
python data_generation/generate_synthetic_data.py
```

**Output**: `data_generation/output/`
- `employees.csv` (2,000 records)
- `compensation.csv`
- `performance.csv`
- `attendance.csv`
- `attrition_labels.csv`

### Run Analytics Pipeline

**Full Pipeline:**
```bash
cd analytics

# 1. Data preparation
python src/data_prep.py

# 2. Feature engineering
python src/feature_engineering.py

# 3. Model training
python src/train_model.py

# 4. Score employees
python src/score_employees.py

# 5. Generate explanations
python src/explainability.py
```

**Individual Steps:**

```python
# Python API usage
from analytics.src import data_prep, feature_engineering, train_model

# Prepare data
df = data_prep.create_analytical_dataset()

# Engineer features
features_df = feature_engineering.engineer_features()

# Train model
train_model.train_attrition_model()
```

### Outputs

All outputs saved to `analytics/outputs/`:

| File | Description |
|------|-------------|
| `prepared_data.csv` | Cleaned and joined dataset |
| `feature_table.csv` | Engineered features (40+ columns) |
| `employee_risk_scores.csv` | Risk predictions for active employees |
| `high_risk_priority_list.csv` | Top 50 at-risk employees |
| `model_metrics.json` | Model performance metrics |
| `logistic_coefficients.csv` | Feature importance |
| `feature_importance.png` | Visualization of top features |
| `shap_summary.png` | SHAP value explanation plot |
| `risk_summary.json` | Risk distribution statistics |

---

## 📁 Project Structure

```
workforce-intelligence-platform/
│
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── .gitignore                    # Git ignore rules
│
├── data_generation/              # Synthetic data generation
│   ├── generate_synthetic_data.py
│   └── output/                   # Generated CSV files
│       ├── employees.csv
│       ├── compensation.csv
│       ├── performance.csv
│       ├── attendance.csv
│       └── attrition_labels.csv
│
├── warehouse/                    # PostgreSQL data warehouse
│   ├── 01_create_schemas.sql    # Create raw and analytics schemas
│   ├── 02_create_tables.sql     # Create tables with constraints
│   └── 03_load_data.sql         # Load CSV data (update paths)
│
├── analytics/                    # Analytics pipeline
│   ├── outputs/                  # Pipeline outputs
│   └── src/                      # Source code
│       ├── utils.py              # Shared utilities
│       ├── data_prep.py          # Data preparation
│       ├── feature_engineering.py # Feature engineering
│       ├── train_model.py        # Model training
│       ├── score_employees.py    # Employee scoring
│       └── explainability.py     # Model interpretation
│
├── docs/                         # Documentation
│   ├── data_dictionary.md        # Field definitions
│   └── metric_definitions.md     # Metric calculations
│
└── insights/                     # Sample reports and insights
    ├── HR_weekly_report.md       # Weekly HR report template
    └── retention_recommendations.md # Retention strategies
```

---

## 📚 Documentation

### Core Documentation

- **[Data Dictionary](docs/data_dictionary.md)**: Comprehensive field definitions for all datasets
- **[Metric Definitions](docs/metric_definitions.md)**: Calculation methods for HR metrics
- **[HR Weekly Report](insights/HR_weekly_report.md)**: Sample executive report
- **[Retention Recommendations](insights/retention_recommendations.md)**: Evidence-based retention strategies

### Key Concepts

#### Risk Bands
- **Low (0.0 - 0.29)**: Stable, engaged employees (~65%)
- **Medium (0.30 - 0.59)**: Moderate flight risk (~25%)
- **High (0.60 - 1.00)**: Significant attrition risk (~10%)

#### Feature Categories
1. **Compensation**: salary percentile, compa-ratio, market position
2. **Performance**: ratings, goals achievement, review frequency
3. **Workload**: overtime hours, attendance issues, PTO usage
4. **Tenure**: months employed, promotion timing, career stage
5. **Department**: team size, attrition rate, salary vs. peers
6. **Interactions**: burnout risk, workload-pay imbalance

---

## 📊 Model Performance

### Expected Performance Metrics

| Metric | Target | Typical Range |
|--------|--------|---------------|
| **AUC-ROC** | > 0.75 | 0.78 - 0.85 |
| **Precision** | > 0.60 | 0.65 - 0.75 |
| **Recall** | > 0.60 | 0.60 - 0.70 |
| **F1 Score** | > 0.60 | 0.62 - 0.72 |

### Top Predictive Features

Based on logistic regression coefficients:

**Risk Increasing (+)**:
1. Below market compensation
2. High overtime (> 40 hrs/month)
3. Low performance ratings
4. Overdue for promotion
5. Department attrition rate

**Risk Decreasing (-)**:
1. Recent promotion or raise
2. High performance ratings
3. Stock options/equity
4. Low overtime
5. Long tenure (> 5 years)

### Model Interpretability

- **Logistic Regression**: Fully interpretable coefficients
- **SHAP Values**: Individual prediction explanations
- **Feature Importance**: Ranked by absolute impact

---

## 🛠️ Customization

### Adjust Synthetic Data

Edit `data_generation/generate_synthetic_data.py`:

```python
# Change number of employees
NUM_EMPLOYEES = 5000  # Default: 2000

# Change date ranges
start_date = datetime(2018, 1, 1)  # Earlier hire dates
end_date = datetime(2024, 12, 31)

# Adjust attrition rate
has_left = np.random.random() < 0.25  # Increase from 18% to 25%
```

### Add Custom Features

Edit `analytics/src/feature_engineering.py`:

```python
def calculate_custom_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    # Example: Add education level feature
    df['has_advanced_degree'] = df['education_level'].isin(['Masters', 'PhD'])
    
    # Example: Add commute distance risk
    df['long_commute_risk'] = (df['commute_miles'] > 30).astype(int)
    
    return df
```

### Tune Model Hyperparameters

Edit `analytics/src/train_model.py`:

```python
model = LogisticRegression(
    penalty='l2',
    C=0.5,  # Increase regularization
    class_weight='balanced',
    max_iter=2000  # More iterations
)
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Commit your changes**: `git commit -m 'Add some feature'`
4. **Push to the branch**: `git push origin feature/your-feature-name`
5. **Open a Pull Request**

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
pytest tests/

# Format code
black analytics/src/

# Lint code
flake8 analytics/src/
```

---

## 📈 Roadmap

### v1.0 (Current)
- ✅ Synthetic data generation
- ✅ PostgreSQL warehouse setup
- ✅ Feature engineering pipeline
- ✅ Logistic regression baseline model
- ✅ Risk scoring and explainability

### v1.1 (Planned)
- [ ] Real-time risk score updates
- [ ] Automated weekly reporting
- [ ] Integration with HRIS APIs (Workday, BambooHR)
- [ ] Web dashboard for HR teams

### v2.0 (Future)
- [ ] Advanced ML models (XGBoost, LightGBM)
- [ ] Survival analysis (time-to-attrition)
- [ ] Intervention effectiveness tracking
- [ ] A/B testing framework for retention programs

---

## ❓ FAQ

**Q: Can I use this with real employee data?**  
A: Yes, but ensure compliance with data privacy laws (GDPR, CCPA). Anonymize PII and secure database access.

**Q: How accurate are the predictions?**  
A: With synthetic data, expect AUC 0.78-0.85. Real data performance depends on data quality and feature relevance.

**Q: What if I don't have PostgreSQL?**  
A: The analytics pipeline works with CSV files only. PostgreSQL is optional for production deployments.

**Q: How often should I retrain the model?**  
A: Quarterly or when significant workforce changes occur (restructuring, policy changes).

**Q: Can I integrate this with my HRIS?**  
A: Yes, modify data loading scripts to connect to your HRIS API. Most systems provide REST APIs or data exports.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with scikit-learn, pandas, and matplotlib
- Inspired by real-world HR analytics challenges
- Thanks to the open-source data science community

---

## 📧 Contact

**Project Maintainer**: Your Name  
**Email**: your.email@example.com  
**LinkedIn**: [Your LinkedIn](https://linkedin.com/in/yourprofile)

For questions, issues, or feature requests:
- **GitHub Issues**: [Report a bug](https://github.com/yourusername/workforce-intelligence-platform/issues)
- **Discussions**: [Ask a question](https://github.com/yourusername/workforce-intelligence-platform/discussions)

---

## ⭐ Star This Repository

If you find this project useful, please consider giving it a star on GitHub! It helps others discover the project and motivates continued development.

---

**Made with ❤️ for HR teams and data analysts worldwide**
