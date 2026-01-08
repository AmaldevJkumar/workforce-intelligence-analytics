-- ============================================================================
-- Workforce Intelligence Platform - Data Loading
-- ============================================================================
-- Description: Loads CSV data into raw schema tables
-- Author: Data Engineering Team
-- Date: January 2026
-- ============================================================================
-- IMPORTANT: Update the file paths below to match your local system
-- Windows example: 'C:/Users/YourName/workforce-intelligence-platform/data_generation/output/employees.csv'
-- ============================================================================

-- Set search path
SET search_path TO raw, public;

-- ============================================================================
-- INSTRUCTIONS FOR UPDATING FILE PATHS
-- ============================================================================
-- Replace 'YOUR_PROJECT_PATH' with the actual path to your project directory
-- Example for Windows:
--   C:/Users/johndoe/Documents/workforce-intelligence-platform/data_generation/output/
--
-- Make sure to:
-- 1. Use forward slashes (/) even on Windows
-- 2. Include the full absolute path
-- 3. Ensure PostgreSQL has read permissions on these files
-- ============================================================================

-- ============================================================================
-- 1. LOAD EMPLOYEES
-- ============================================================================
\echo 'Loading employees data...'

COPY raw.employees (
    employee_id,
    first_name,
    last_name,
    email,
    department,
    job_title,
    job_level,
    location,
    hire_date,
    termination_date,
    employment_status
)
FROM 'YOUR_PROJECT_PATH/data_generation/output/employees.csv'
WITH (
    FORMAT CSV,
    HEADER TRUE,
    DELIMITER ',',
    NULL ''
);

-- Verify load
SELECT COUNT(*) as employees_loaded FROM raw.employees;

-- ============================================================================
-- 2. LOAD COMPENSATION
-- ============================================================================
\echo 'Loading compensation data...'

COPY raw.compensation (
    employee_id,
    base_salary,
    annual_bonus,
    stock_options,
    currency,
    last_raise_date,
    market_adjustment_pct
)
FROM 'YOUR_PROJECT_PATH/data_generation/output/compensation.csv'
WITH (
    FORMAT CSV,
    HEADER TRUE,
    DELIMITER ',',
    NULL ''
);

-- Verify load
SELECT COUNT(*) as compensation_records_loaded FROM raw.compensation;

-- ============================================================================
-- 3. LOAD PERFORMANCE
-- ============================================================================
\echo 'Loading performance data...'

COPY raw.performance (
    employee_id,
    review_date,
    performance_rating,
    reviewer_id,
    review_type,
    goals_met_pct
)
FROM 'YOUR_PROJECT_PATH/data_generation/output/performance.csv'
WITH (
    FORMAT CSV,
    HEADER TRUE,
    DELIMITER ',',
    NULL ''
);

-- Verify load
SELECT COUNT(*) as performance_records_loaded FROM raw.performance;

-- ============================================================================
-- 4. LOAD ATTENDANCE
-- ============================================================================
\echo 'Loading attendance data...'

COPY raw.attendance (
    employee_id,
    record_date,
    days_present,
    days_absent,
    days_pto,
    overtime_hours,
    remote_days
)
FROM 'YOUR_PROJECT_PATH/data_generation/output/attendance.csv'
WITH (
    FORMAT CSV,
    HEADER TRUE,
    DELIMITER ',',
    NULL ''
);

-- Verify load
SELECT COUNT(*) as attendance_records_loaded FROM raw.attendance;

-- ============================================================================
-- 5. LOAD ATTRITION LABELS
-- ============================================================================
\echo 'Loading attrition labels data...'

COPY raw.attrition_labels (
    employee_id,
    attrition_flag,
    attrition_date,
    attrition_reason,
    voluntary,
    regrettable,
    attrition_risk_score
)
FROM 'YOUR_PROJECT_PATH/data_generation/output/attrition_labels.csv'
WITH (
    FORMAT CSV,
    HEADER TRUE,
    DELIMITER ',',
    NULL ''
);

-- Verify load
SELECT COUNT(*) as attrition_records_loaded FROM raw.attrition_labels;

-- ============================================================================
-- VALIDATION QUERIES
-- ============================================================================
\echo 'Running validation queries...'

-- Summary of loaded data
SELECT 
    'employees' as table_name,
    COUNT(*) as record_count,
    COUNT(DISTINCT employee_id) as unique_employees
FROM raw.employees

UNION ALL

SELECT 
    'compensation' as table_name,
    COUNT(*) as record_count,
    COUNT(DISTINCT employee_id) as unique_employees
FROM raw.compensation

UNION ALL

SELECT 
    'performance' as table_name,
    COUNT(*) as record_count,
    COUNT(DISTINCT employee_id) as unique_employees
FROM raw.performance

UNION ALL

SELECT 
    'attendance' as table_name,
    COUNT(*) as record_count,
    COUNT(DISTINCT employee_id) as unique_employees
FROM raw.attendance

UNION ALL

SELECT 
    'attrition_labels' as table_name,
    COUNT(*) as record_count,
    COUNT(DISTINCT employee_id) as unique_employees
FROM raw.attrition_labels
ORDER BY table_name;

-- Check for referential integrity
\echo 'Checking referential integrity...'

SELECT 
    'Orphaned compensation records' as check_name,
    COUNT(*) as issue_count
FROM raw.compensation c
WHERE NOT EXISTS (
    SELECT 1 FROM raw.employees e WHERE e.employee_id = c.employee_id
)

UNION ALL

SELECT 
    'Orphaned performance records' as check_name,
    COUNT(*) as issue_count
FROM raw.performance p
WHERE NOT EXISTS (
    SELECT 1 FROM raw.employees e WHERE e.employee_id = p.employee_id
)

UNION ALL

SELECT 
    'Orphaned attendance records' as check_name,
    COUNT(*) as issue_count
FROM raw.attendance a
WHERE NOT EXISTS (
    SELECT 1 FROM raw.employees e WHERE e.employee_id = a.employee_id
)

UNION ALL

SELECT 
    'Orphaned attrition records' as check_name,
    COUNT(*) as issue_count
FROM raw.attrition_labels al
WHERE NOT EXISTS (
    SELECT 1 FROM raw.employees e WHERE e.employee_id = al.employee_id
);

-- Data quality checks
\echo 'Running data quality checks...'

SELECT 
    'Employees with future hire dates' as quality_check,
    COUNT(*) as issue_count
FROM raw.employees
WHERE hire_date > CURRENT_DATE

UNION ALL

SELECT 
    'Invalid termination dates' as quality_check,
    COUNT(*) as issue_count
FROM raw.employees
WHERE termination_date IS NOT NULL 
  AND termination_date < hire_date

UNION ALL

SELECT 
    'Negative salaries' as quality_check,
    COUNT(*) as issue_count
FROM raw.compensation
WHERE base_salary <= 0

UNION ALL

SELECT 
    'Invalid performance ratings' as quality_check,
    COUNT(*) as issue_count
FROM raw.performance
WHERE performance_rating NOT BETWEEN 1 AND 5;

-- Success message
DO $$
BEGIN
    RAISE NOTICE '============================================================';
    RAISE NOTICE 'DATA LOADING COMPLETE';
    RAISE NOTICE '============================================================';
    RAISE NOTICE 'All CSV files loaded successfully into raw schema';
    RAISE NOTICE 'Review validation results above for data quality issues';
END $$;
