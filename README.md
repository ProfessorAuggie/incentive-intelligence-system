# Enterprise Incentive Intelligence System

A comprehensive, production-grade platform for managing, calculating, validating, and analyzing employee incentive payouts in enterprise environments.

## 🎯 Overview

The **Enterprise Incentive Intelligence System** is a sophisticated enterprise-grade application designed to simulate real-world incentive management with:

- **Incentive Calculation Engine**: Complex multi-tier compensation formulas
- **Data Validation**: Comprehensive data quality checks
- **Anomaly Detection**: ML-based outlier and inconsistency detection
- **SQL Database Layer**: Persistent data storage and querying
- **Advanced Analytics**: Business intelligence and visualization
- **Comprehensive Reporting**: Executive summaries and detailed reports
- **Interactive Dashboard**: Web-based exploration via Streamlit

## 📊 Project Architecture

```
Enterprise Incentive Intelligence System/
├── src/
│   ├── dataset_generator.py      # Synthetic data generation (750+ records)
│   ├── incentive_engine.py       # Multi-tier payout calculations
│   ├── validation.py             # Data quality validation
│   ├── anomaly_detection.py      # Pattern detection & outliers
│   ├── database.py               # SQLite/PostgreSQL layer
│   ├── analytics.py              # Analytics & visualizations
│   └── reporting.py              # Report generation & export
├── data/                         # Database storage
├── reports/                      # Generated reports & charts
├── main.py                       # Batch processing orchestrator
├── app.py                        # Streamlit interactive dashboard
├── requirements.txt              # Dependencies
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone repository
cd Sales-Incentive-Management-System

# Install dependencies
pip install -r requirements.txt
```

### Usage

#### Option 1: Batch Processing (Full Analysis)
```bash
python main.py
```
This will:
1. Generate 750 synthetic employee records
2. Validate data quality
3. Calculate multi-tier incentives
4. Detect anomalies
5. Store data in SQLite
6. Generate analytics charts (6 visualizations)
7. Create comprehensive reports

**Output:**
- Generated reports in `./reports/`
- Database at `./data/incentive_system.db`
- 6 PNG charts (sales, incentives, performance tiers, etc.)

#### Option 2: Interactive Dashboard
```bash
streamlit run app.py
```
Then navigate to `http://localhost:8501` in your browser.

## 📋 Feature Details

### 1️⃣ Incentive Calculation Engine

**Multi-Tier Compensation Model:**

| Achievement Level | Payout |
|---|---|
| 0-80% of target | 0% |
| 80-100% of target | 5% |
| 100%+ of target | 10% |
| 150%+ of target | 20% |
| +20% YoY growth | +5% bonus |
| Manager bonus (base) | 3-15% (team-dependent) |

**Example Calculation:**
```
Employee Sales: $150,000 | Target: $100,000
Achievement Ratio: 1.5 (150%)
Base Incentive: 20% (exceeds 150%)
Growth Bonus: +5% (20% YoY growth)
Role Bonus: 0% (Sales rep)
Total Incentive: 25% → $25,000 payout
```

### 2️⃣ Data Validation

Comprehensive validation checks:

- **Structure**: Required columns, data types
- **Null Detection**: Missing values in critical fields
- **Range Validation**: Negative values, unrealistic ranges
- **Consistency**: Duplicate IDs, invalid roles/regions
- **Business Logic**: Reasonable growth rates, target constraints

**Validation Report includes:**
- Error severity classification
- Warning alerts
- Record-level issues
- Timestamp and status

### 3️⃣ Anomaly Detection

Detects 5 categories of anomalies:

1. **High Incentive Outliers** (Z-score > 3.0)
   - Identifies unusually high payouts
   - Flags potential data errors or exceptional performance

2. **Zero Incentive with High Sales**
   - Employees meeting targets but receiving no payout
   - Indicates possible system errors

3. **Extreme Growth** (>500% QoQ)
   - Validates extreme growth claims
   - Identifies possible data entry errors

4. **Data Quality Issues**
   - Null values in critical fields
   - Negative or zero values where not expected

5. **Role Performance Mismatch**
   - Managers with unusually low payouts despite high sales
   - Role-specific anomalies

**Output:** Each anomaly flagged with type and severity

### 4️⃣ SQL Database Layer

**SQLite Database** with tables:

```sql
-- Employee Master Data
CREATE TABLE employees (
    employee_id TEXT PRIMARY KEY,
    employee_name TEXT NOT NULL,
    region TEXT,
    role TEXT,
    team_size INTEGER,
    team_performance FLOAT
);

-- Sales Transactions
CREATE TABLE sales_data (
    id INTEGER PRIMARY KEY,
    employee_id TEXT NOT NULL,
    quarter TEXT NOT NULL,
    sales_target FLOAT,
    sales_amount FLOAT,
    previous_quarter_sales FLOAT,
    achievement_ratio FLOAT
);

-- Calculated Incentives
CREATE TABLE incentives (
    id INTEGER PRIMARY KEY,
    employee_id TEXT NOT NULL,
    quarter TEXT NOT NULL,
    base_incentive FLOAT,
    growth_bonus FLOAT,
    role_bonus FLOAT,
    total_incentive FLOAT,
    incentive_payout FLOAT,
    performance_tier TEXT
);

-- Detected Anomalies
CREATE TABLE anomalies (
    id INTEGER PRIMARY KEY,
    employee_id TEXT NOT NULL,
    quarter TEXT,
    anomaly_type TEXT,
    severity TEXT,
    description TEXT,
    detected_at TIMESTAMP
);
```

**Key Queries:**

```python
# Top 10 performers by payout
db.query_top_performers(limit=10)

# Regional summary with totals
db.query_region_summary()

# Role-based analysis
db.query_role_analysis()

# Anomaly summary
db.query_anomalies_summary()

# Complete dataset join
db.query_all_data()
```

### 5️⃣ Analytics & Visualization

**Generated Charts (PNG format):**

1. **Region Sales Analysis**
   - Total sales by geographical region
   - Regional performance comparison

2. **Incentive Distribution**
   - Histogram with mean/median overlays
   - Payout range visualization

3. **Performance Tiers Pie Chart**
   - Employee distribution across tiers
   - Performance category breakdown

4. **Role Comparison (2-panel)**
   - Average sales by role
   - Average incentive payout by role

5. **Sales vs Target Scatter Plot**
   - Achievement visualization
   - Role-based color coding

6. **Growth Analysis (2-panel)**
   - QoQ growth rate distribution
   - Growth bonus distribution by role

### 6️⃣ Comprehensive Reporting

**4 Report Types Generated:**

#### Executive Summary Report
- Financial overview (total, average, max, min payouts)
- Performance metrics (achievement rate, etc.)
- Bonus analysis breakdown
- Regional breakdown with top performers

#### Top Performers Report
- Ranked list (top 20) with detailed metrics
- Sales targets vs achievements
- Role and region information
- Performance tier classification

#### Anomaly Report
- Total anomalies and percentage
- Anomaly type distribution
- Detailed anomalous records (top 20)
- Issue descriptions and severity

#### Regional Analysis Report
- Per-region metrics:
  - Employee count
  - Total sales and incentives
  - Achievement rates
  - Top regional performer

All reports include timestamps and are exported as text files for easy integration.

### 7️⃣ Interactive Dashboard (Streamlit)

**6 Dashboard Tabs:**

1. **📊 Dashboard**: KPI metrics and overview charts
   - Total payouts and averages
   - Achievement rates
   - Interactive visualizations

2. **👥 Employees**: Employee lookup and rankings
   - Top 10 performers list
   - Employee search functionality
   - Detailed performance metrics

3. **🔍 Anomalies**: Anomaly exploration
   - Anomaly statistics and types
   - Detailed anomalous record list
   - Severity indicators

4. **📈 Analytics**: Detailed analytics view
   - Sales and incentive by role
   - Growth metrics and distribution
   - Statistical analysis

5. **🏪 Regional**: Regional performance analysis
   - Regional summary table
   - Distribution charts
   - Comparative metrics

6. **⚙️ Admin**: Administration panel
   - Dataset summary
   - Data quality metrics
   - Export functionality

**Features:**
- Real-time filtering by region, role, incentive level
- Interactive Plotly charts
- CSV export capability
- Responsive design

## 📊 Dataset Specification

**Generated Dataset (750 records):**

| Field | Type | Range | Description |
|---|---|---|---|
| employee_id | String | EMP00001-EMP00750 | Unique identifier |
| employee_name | String | - | Employee full name |
| region | String | 5 regions | NA, Europe, APAC, LATAM, MEA |
| role | String | Sales/Manager | Employee role (70/30 split) |
| quarter | String | Q1-Q4 2023-2025 | Quarter identifier |
| sales_target | Float | $50K-$500K | Sales quota |
| sales_amount | Float | $0-$1.25M | Actual sales |
| previous_quarter_sales | Float | $40K-$600K | Prior period sales |
| team_size | Integer | 1-15 | Manager team size |
| team_performance | Float | 0.8-1.3 | Manager team multiplier |

**Synthetic Data Characteristics:**
- 60% of employees meet targets
- 25% exceed 150% targets
- 15% fall below targets
- ~3% intentional anomalies for testing
- Realistic growth distributions

## 🔧 Configuration & Customization

### Modify Incentive Rules

Edit `src/incentive_engine.py`:

```python
class IncentiveEngine:
    # Adjust these constants
    BASE_SALARY_PERCENTAGE = 0.60
    PAYOUT_AT_TARGET = 0.10
    PAYOUT_AT_150_PERCENT = 0.20
    GROWTH_BONUS = 0.05
    GROWTH_THRESHOLD = 0.20
```

### Adjust Anomaly Sensitivity

Edit `src/anomaly_detection.py`:

```python
detector = AnomalyDetector(
    z_threshold=3.0,      # Lower = more sensitive
    iqr_multiplier=1.5    # Lower = more sensitive
)
```

### Generate Different Dataset Size

```python
generator = DatasetGenerator(num_records=1000, seed=42)
```

### PostgreSQL Configuration

In `src/database.py`:

```python
db = DatabaseManager(use_sqlite=False)
# Configure PostgreSQL connection string in __init__
```

## 📈 Business Insights & Use Cases

### 1. Compliance Monitoring
- Validate all payouts against policy
- Detect unauthorized adjustments
- Audit trail via database

### 2. Performance Analysis
- Identify top performers by region/role
- Spot underperforming regions
- Track growth trends

### 3. Anomaly Investigation
- Flag unusual payouts for review
- Identify data quality issues
- Detect potential fraud patterns

### 4. Compensation Planning
- Project incentive costs by region
- Analyze role-based compensation
- Validate fairness across teams

### 5. Executive Reporting
- Generate C-suite dashboards
- Track KPIs and trends
- Export for Board presentations

## 🛠 Technical Stack

| Component | Technology | Purpose |
|---|---|---|
| **Data Processing** | Pandas, NumPy | Data manipulation, calculations |
| **Database** | SQLite (PostgreSQL-ready) | Persistent storage, querying |
| **Analytics** | Matplotlib, Seaborn, Plotly | Visualization & charts |
| **Web Dashboard** | Streamlit | Interactive web interface |
| **ORM** | SQLAlchemy | Database abstraction |
| **Environment** | Python 3.8+ | Runtime |

## 📁 Output Files

### Reports Directory (`./reports/`)
```
reports/
├── executive_summary_YYYYMMDD_HHMMSS.txt
├── top_performers_YYYYMMDD_HHMMSS.txt
├── anomaly_report_YYYYMMDD_HHMMSS.txt
├── regional_analysis_YYYYMMDD_HHMMSS.txt
├── complete_dataset_YYYYMMDD_HHMMSS.csv
├── region_sales.png
├── incentive_distribution.png
├── performance_tiers.png
├── role_comparison.png
├── sales_vs_target.png
└── growth_analysis.png
```

### Database (`./data/`)
```
data/
└── incentive_system.db  # SQLite database file
```

## 🧪 Testing & Validation

The system includes comprehensive testing via anomaly injection:

```python
# Add 3% intentional anomalies for testing
df = DatasetGenerator.add_anomalies(df, anomaly_percentage=3)
```

This creates:
- Unrealistic high sales (10x target)
- Null value entries
- Negative sales values

Then verifies detection accuracy.

## 🔒 Data Quality Guarantees

- ✅ All nulls detected and reported
- ✅ Range validation on all numeric fields
- ✅ Consistency checks on categorical fields
- ✅ Business logic validation
- ✅ Anomaly flagging with severity levels
- ✅ Database referential integrity
- ✅ Audit trail via timestamp tracking

## 📚 API Reference

### DatasetGenerator
```python
generator = DatasetGenerator(num_records=750, seed=42)
df = generator.generate()
df = DatasetGenerator.add_anomalies(df, anomaly_percentage=2)
```

### IncentiveEngine
```python
engine = IncentiveEngine(base_salary_reference=100000)
df = engine.calculate_incentives(df)
df = engine.get_performance_tiers(df)
summary = engine.get_incentive_summary(df)
```

### DataValidator
```python
validator = DataValidator()
is_valid, report = validator.validate(df)
validator.print_report()
```

### AnomalyDetector
```python
detector = AnomalyDetector(z_threshold=3.0, iqr_multiplier=1.5)
df = detector.detect_all(df)
report = detector.get_anomaly_report(df)
detector.print_anomaly_report(df)
```

### DatabaseManager
```python
db = DatabaseManager(db_path='data/incentive_system.db')
db.create_tables()
db.insert_employees(df)
db.insert_sales_data(df)
db.insert_incentives(df)
db.insert_anomalies(df)

# Queries
top_performers = db.query_top_performers(limit=10)
region_summary = db.query_region_summary()
role_analysis = db.query_role_analysis()
anomalies = db.query_anomalies_summary()
```

### Analytics
```python
analytics = Analytics(output_dir='reports')
analytics.analyze_region_performance(df)
analytics.generate_all_charts(df)
```

### Reporter
```python
reporter = Reporter(output_dir='reports')
reporter.generate_executive_summary(df, engine)
reporter.generate_top_performers_report(df, limit=20)
reporter.generate_anomaly_report(df, detector)
reporter.generate_region_report(df)
reporter.generate_all_reports(df, engine, detector)
```

## 🎓 Key Metrics Definitions

| Metric | Definition | Calculation |
|---|---|---|
| **Achievement Ratio** | Sales as % of target | Sales / Target |
| **Performance Tier** | Categorical achievement level | Based on achievement ratio ranges |
| **Base Incentive** | Main compensation tier | Based on achievement ratio |
| **Growth Bonus** | QoQ growth reward | +5% if growth > 20% |
| **Role Bonus** | Role-specific compensation | Varies by role (Mgr: 3-15%, Sales: 0%) |
| **Total Incentive %** | Sum of all bonuses | Base + Growth + Role |
| **Incentive Payout** | Actual dollar amount | Sales Target × Total Incentive % |

## 📞 Support & Documentation

### Common Issues

**Q: Dashboard won't load?**
A: Ensure Streamlit is installed: `pip install streamlit`

**Q: Database file not found?**
A: Run `python main.py` first to generate database

**Q: Charts not displaying?**
A: Check Plotly is installed: `pip install plotly`

### Performance Optimization

For large datasets (>5000 records):
- Consider PostgreSQL instead of SQLite
- Add database indexes on frequently queried columns
- Use SQLAlchemy connection pooling

## 📄 License & Credits

Created as an enterprise-grade demonstration of:
- Data engineering best practices
- Business logic implementation
- SQL database design
- Analytics and visualization
- Web application development
- Python software architecture

## 🚀 Future Enhancements

Potential extensions:
- [ ] Real-time data streaming
- [ ] Machine learning for prediction
- [ ] Advanced forecasting
- [ ] Mobile app support
- [ ] API endpoints (FastAPI)
- [ ] CI/CD integration
- [ ] Cloud deployment templates
- [ ] Advanced BI integration (Power BI, Tableau)

---

**Version:** 1.0.0  
**Last Updated:** 2024-2025  
**Status:** Production Ready