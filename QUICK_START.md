# Quick Reference Guide

## 🚀 Getting Started (30 seconds)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Choose one:

# Option A: Full batch processing (2-3 minutes)
python main.py

# Option B: Interactive dashboard (real-time)
streamlit run app.py

# Option C: Example scenarios
python example_usage.py
```

---

## 📊 What Gets Generated

### Option A: Batch Processing (`python main.py`)
**Generates in `./reports/` and `./data/`:**
- 4 text reports (Executive Summary, Top Performers, Anomalies, Regional Analysis)
- 1 CSV export (Complete dataset)
- 6 PNG charts (Sales, Distribution, Tiers, Roles, Scatter, Growth)
- 1 SQLite database with 4 tables

**Time:** 2-3 minutes
**Output Size:** ~5-10 MB total

### Option B: Dashboard (`streamlit run app.py`)
**Real-time Interactive:**
- 6 dashboard tabs with live filtering
- Interactive Plotly charts
- CSV export capability
- Employee search functionality
- Anomaly exploration

**Access:** http://localhost:8501
**Time:** Instant loading

### Option C: Examples (`python example_usage.py`)
**Demonstrates:**
1. Basic workflow (100 records)
2. Data validation with anomalies
3. Anomaly detection results
4. Database operations
5. Analytics summary
6. Full pipeline

---

## 📋 Core Components

| Component | File | Purpose |
|---|---|---|
| **Dataset** | `dataset_generator.py` | Generate 750+ synthetic records |
| **Incentives** | `incentive_engine.py` | Calculate multi-tier payouts |
| **Validation** | `validation.py` | Detect data quality issues |
| **Anomalies** | `anomaly_detection.py` | Find outliers & inconsistencies |
| **Database** | `database.py` | SQLite persistence & queries |
| **Analytics** | `analytics.py` | Charts & visualizations |
| **Reports** | `reporting.py` | Generate 4 report types |

---

## 🎯 Key Metrics

| Metric | Calculation | Range |
|---|---|---|
| Achievement Ratio | Sales / Target | 0-∞ |
| Base Incentive | Tier based on ratio | 0-20% |
| Growth Bonus | If growth > 20% | 0-5% |
| Total Payout | Target × Total % | $0-∞ |

---

## 📁 Directory Structure

```
.
├── src/                    # Core modules
├── data/                   # Database storage
├── reports/                # Generated outputs
├── main.py                 # Batch processor
├── app.py                  # Streamlit dashboard
├── example_usage.py        # Examples
└── requirements.txt        # Dependencies
```

---

## 🔍 Common Tasks

### Generate Reports Only
```python
from src.reporting import Reporter
from src.database import DatabaseManager

db = DatabaseManager()
reporter = Reporter()
df = db.query_all_data()
reporter.generate_all_reports(df, engine, detector)
```

### Query Top Performers
```python
from src.database import DatabaseManager

db = DatabaseManager()
top_10 = db.query_top_performers(limit=10)
print(top_10)
```

### Check for Anomalies
```python
from src.anomaly_detection import AnomalyDetector

detector = AnomalyDetector()
df = detector.detect_all(df)
detector.print_anomaly_report(df)
```

### Export to CSV
```python
from src.reporting import Reporter

reporter = Reporter()
reporter.export_to_csv(df, 'my_export.csv')
```

---

## 💾 Database Queries

Access SQLite database at `./data/incentive_system.db`

**Key queries:**
```sql
-- Top 10 performers
SELECT employee_name, incentive_payout 
FROM incentives 
ORDER BY incentive_payout DESC LIMIT 10;

-- Regional summary
SELECT region, COUNT(*), SUM(incentive_payout)
FROM employees e JOIN incentives i
GROUP BY region;

-- Anomalies
SELECT * FROM anomalies 
ORDER BY detected_at DESC;
```

---

## 🎨 Customization

### Change Incentive Rules
Edit `src/incentive_engine.py`:
```python
PAYOUT_AT_TARGET = 0.10        # Change from 10%
PAYOUT_AT_150_PERCENT = 0.20   # Change from 20%
```

### Adjust Anomaly Detection
Edit `src/anomaly_detection.py`:
```python
detector = AnomalyDetector(
    z_threshold=2.5,    # More sensitive (was 3.0)
    iqr_multiplier=1.0  # More sensitive (was 1.5)
)
```

### Change Dataset Size
Edit `main.py` or `example_usage.py`:
```python
generator = DatasetGenerator(num_records=1000)  # was 750
```

---

## 📊 Understanding the Output

### Executive Summary
- Total incentive payout & averages
- Performance achievement rates
- Bonus distribution analysis
- Regional breakdown

### Top Performers Report
- Ranked employee list
- Sales vs target comparison
- Performance tier assignment
- Regional distribution

### Anomaly Report
- Anomaly count & percentage
- Detection method breakdown
- Detailed anomalous records
- Severity indicators

### Regional Analysis
- Per-region metrics
- Achievement rates
- Top regional performers
- Comparative statistics

### Charts
1. **Region Sales** - Horizontal comparison
2. **Incentive Distribution** - Statistical histogram
3. **Performance Tiers** - Employee breakdown
4. **Role Comparison** - Sales vs Incentive by role
5. **Sales vs Target** - Achievement scatter plot
6. **Growth Analysis** - QoQ growth patterns

---

## ⚙️ Configuration Files

### requirements.txt
```
pandas==2.1.4
numpy==1.24.3
matplotlib==3.8.4
seaborn==0.13.0
sqlalchemy==2.0.25
streamlit==1.31.1
plotly==5.18.0
python-dotenv==1.0.0
```

### .gitignore
Configured for:
- Python cache & builds
- Virtual environments
- Database files
- Report outputs
- IDE configurations
- OS files

---

## 🚨 Troubleshooting

**Q: Charts won't display?**
```bash
pip install --upgrade plotly
```

**Q: Streamlit command not found?**
```bash
pip install streamlit
```

**Q: SQLite error?**
```bash
pip install --upgrade sqlalchemy
```

**Q: Import errors?**
```bash
pip install -r requirements.txt --force-reinstall
```

**Q: Permission denied?**
```bash
chmod +x main.py app.py example_usage.py
```

---

## 📞 Support Resources

**See:** [README.md](README.md) for:
- Complete feature documentation
- API reference
- Business use cases
- Detailed customization guide

**Examples:** [example_usage.py](example_usage.py) has 6 runnable scenarios

**Code:** All modules have docstrings and comments

---

## ✨ Key Features at a Glance

- **750+ Records** - Realistic synthetic data
- **Multi-tier Incentives** - 5 calculation tiers
- **Complete Validation** - 5 validation categories
- **5 Anomaly Types** - Sophisticated detection
- **4 Tables** - SQLite database structure
- **6 Charts** - Professional visualizations
- **4 Reports** - Business intelligence
- **6 Dashboard Tabs** - Interactive exploration
- **100% Documented** - Comments on all code
- **6 Examples** - Runnable scenarios

---

## 🎯 Next Steps

1. **Install:** `pip install -r requirements.txt`
2. **Run:** Choose option A, B, or C above
3. **Explore:** Check generated reports in `./reports/`
4. **Customize:** Edit constants in `src/*.py` files
5. **Integrate:** Use classes in your own scripts

---

**Version:** 1.0.0
**Status:** Production Ready
**Last Updated:** 2024-2025
