# Data Dictionary

## Overview
This document provides detailed definitions for all datasets, tables, and fields used in the Workforce Intelligence & Attrition Risk Platform.

---

## Raw Data Tables

### employees.csv
Core employee demographic and employment information.

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| employee_id | String | Unique employee identifier | EMP00001 |
| first_name | String | Employee first name | John |
| last_name | String | Employee last name | Smith |
| email | String | Employee email address | john.smith@company.com |
| department | String | Department name | Engineering |
| job_title | String | Current job title | Senior Software Engineer |
| job_level | String | Organizational level | Senior |
| location | String | Primary work location | San Francisco |
| hire_date | Date | Date employee was hired | 2022-03-15 |
| termination_date | Date | Date employment ended (NULL if active) | 2024-06-30 |
| employment_status | String | Current status: Active or Terminated | Active |

**Key Constraints:**
- `employee_id` is unique primary key
- `termination_date` must be >= `hire_date`
- `employment_status` must be 'Active' or 'Terminated'

---

### compensation.csv
Employee compensation details including salary, bonus, and equity.

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| employee_id | String | Links to employees table | EMP00001 |
| base_salary | Decimal | Annual base salary in USD | 125000.00 |
| annual_bonus | Decimal | Annual bonus amount | 15000.00 |
| stock_options | Integer | Number of stock options granted | 5000 |
| currency | String | Currency code | USD |
| last_raise_date | Date | Date of most recent salary increase | 2023-12-01 |
| market_adjustment_pct | Decimal | % above/below market rate | -3.5 |

**Key Metrics:**
- **Total Compensation**: base_salary + annual_bonus
- **Compa-Ratio**: base_salary / department_median_salary
- **Below Market**: market_adjustment_pct < -5%

---

### performance.csv
Employee performance review history and ratings.

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| employee_id | String | Links to employees table | EMP00001 |
| review_date | Date | Date of performance review | 2024-06-15 |
| performance_rating | Integer | Rating on 1-5 scale | 4 |
| reviewer_id | String | ID of reviewing manager | EMP00500 |
| review_type | String | Type of review | Annual |
| goals_met_pct | Decimal | Percentage of goals achieved | 85.5 |

**Rating Scale:**
- 1: Below Expectations
- 2: Needs Improvement
- 3: Meets Expectations
- 4: Exceeds Expectations
- 5: Outstanding

---

### attendance.csv
Employee attendance, PTO, and overtime tracking.

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| employee_id | String | Links to employees table | EMP00001 |
| record_date | Date | Month/year of record | 2024-01-01 |
| days_present | Integer | Days present in month | 20 |
| days_absent | Integer | Unplanned absence days | 1 |
| days_pto | Integer | Planned time off days | 2 |
| overtime_hours | Decimal | Overtime hours worked | 15.5 |
| remote_days | Integer | Days worked remotely | 10 |

**Key Metrics:**
- **Attendance Rate**: days_present / total_work_days
- **Overtime Rate**: overtime_hours / months_employed
- **Remote Work %**: remote_days / days_present

---

### attrition_labels.csv
Attrition labels and reasons for terminated employees only.

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| employee_id | String | Links to employees table | EMP00001 |
| attrition_flag | Integer | 1 if left, 0 if stayed | 1 |
| attrition_date | Date | Date of separation | 2024-06-30 |
| attrition_reason | String | Reason for leaving | Resignation - Better Offer |
| voluntary | Integer | 1 if voluntary, 0 if involuntary | 1 |
| regrettable | Integer | 1 if regrettable loss, 0 otherwise | 1 |
| attrition_risk_score | Decimal | Historical risk score (0-1) | 0.742 |

**Attrition Reasons:**
- Resignation - Better Offer
- Resignation - Work-Life Balance
- Resignation - Career Growth
- Performance
- Layoff
- Relocation

**Regrettable Attrition Criteria:**
- Voluntary resignation AND
- Performance rating >= 3.5

---

## Analytical Tables

### feature_table.csv
Engineered features for model training and scoring.

**Compensation Features:**
- `salary_dept_percentile`: Salary percentile within department (0-100)
- `salary_level_percentile`: Salary percentile within job level (0-100)
- `compa_ratio`: Actual salary / department median
- `below_market`: 1 if market_adjustment_pct < -5%, 0 otherwise
- `bonus_ratio`: annual_bonus / base_salary * 100
- `has_stock_options`: 1 if stock_options > 0, 0 otherwise
- `months_since_raise`: Months since last salary increase

**Performance Features:**
- `avg_performance_rating`: Average of all performance ratings
- `performance_volatility`: max_rating - min_rating
- `low_performer`: 1 if avg_rating < 3, 0 otherwise
- `high_performer`: 1 if avg_rating >= 4, 0 otherwise
- `goals_achiever`: 1 if avg_goals_met_pct >= 80%, 0 otherwise
- `months_since_review`: Months since last performance review

**Workload Features:**
- `avg_monthly_overtime`: Average overtime hours per month
- `high_overtime`: 1 if avg_monthly_overtime > 40, 0 otherwise
- `very_high_overtime`: 1 if avg_monthly_overtime > 60, 0 otherwise
- `attendance_issues`: 1 if annual absence rate > 5 days, 0 otherwise
- `low_pto_usage`: 1 if annual PTO < 5 days, 0 otherwise
- `remote_work_pct`: Percentage of days worked remotely

**Tenure Features:**
- `tenure_months`: Months of employment
- `early_tenure`: 1 if tenure < 12 months, 0 otherwise
- `months_since_promotion`: Estimated months since last promotion
- `overdue_promotion`: 1 if months_since_promotion > 24, 0 otherwise
- `tenure_level_mismatch`: 1 if long tenure but junior level, 0 otherwise

**Department Features:**
- `dept_size`: Number of employees in department
- `dept_attrition_rate`: Historical attrition rate for department
- `high_attrition_dept`: 1 if dept_attrition_rate > 20%, 0 otherwise
- `salary_vs_dept_avg`: base_salary / dept_avg_salary

**Interaction Features:**
- `workload_compensation_imbalance`: High overtime + below market pay
- `high_performer_at_risk`: High performance + below market pay
- `burnout_risk`: Very high overtime + attendance issues
- `flight_risk_composite`: Weighted composite of risk factors (0-1)

---

### employee_risk_scores.csv
Attrition risk predictions for active employees.

| Field | Type | Description | Range |
|-------|------|-------------|-------|
| employee_id | String | Unique employee identifier | - |
| attrition_risk_score | Decimal | Predicted probability of attrition | 0.0 - 1.0 |
| risk_band | String | Risk category | Low/Medium/High |
| risk_rank | Integer | Rank by risk (1 = highest) | 1 - N |
| risk_percentile | Decimal | Percentile rank of risk | 0 - 100 |

**Risk Band Definitions:**
- **Low**: risk_score < 0.3 (Stay probability > 70%)
- **Medium**: risk_score 0.3 - 0.6 (Stay probability 40-70%)
- **High**: risk_score > 0.6 (Stay probability < 40%)

---

## Model Output Files

### model_metrics.json
Performance metrics for trained attrition model.

```json
{
  "auc_roc": 0.8234,
  "precision": 0.7156,
  "recall": 0.6847,
  "f1_score": 0.6998,
  "accuracy": 0.8512,
  "test_set_size": 500
}
```

### logistic_coefficients.csv
Feature importance from logistic regression model.

| Field | Description |
|-------|-------------|
| feature | Feature name |
| coefficient | Logistic regression coefficient |
| abs_coefficient | Absolute value of coefficient |
| effect | "Increases Risk" or "Decreases Risk" |
| importance | Categorical importance: Low/Medium/High/Very High |

---

## Data Quality Rules

### Validation Checks
1. **Referential Integrity**: All employee_ids in dependent tables exist in employees table
2. **Date Logic**: termination_date >= hire_date
3. **Value Ranges**: 
   - performance_rating: 1-5
   - attrition_flag: 0 or 1
   - base_salary > 0
4. **Consistency**: Attrition labels only for terminated employees

### Data Freshness
- **Raw Data**: Updated monthly from HR systems
- **Features**: Regenerated after each data update
- **Model Scores**: Refreshed weekly or on-demand
- **Reports**: Generated daily for high-priority employees

---

## Change Log

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-08 | Initial data dictionary |

---

## Contact
For questions about data definitions or access:
- Data Team: data@company.com
- HR Analytics: hr-analytics@company.com
