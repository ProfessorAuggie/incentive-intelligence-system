"""
Main Application
Orchestrates all components of the Enterprise Incentive Intelligence System
"""

import sys
import os
import pandas as pd

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from dataset_generator import DatasetGenerator
from incentive_engine import IncentiveEngine
from validation import DataValidator
from anomaly_detection import AnomalyDetector
from database import DatabaseManager
from analytics import Analytics
from reporting import Reporter


def main():
    """Main execution flow"""
    
    print("\n" + "="*80)
    print(" ENTERPRISE INCENTIVE INTELLIGENCE SYSTEM - BATCH PROCESSING")
    print("="*80 + "\n")
    
    # ========== STEP 1: GENERATE DATASET ==========
    print("Step 1: Generating Synthetic Dataset...")
    print("-" * 80)
    generator = DatasetGenerator(num_records=750, seed=42)
    df = generator.generate()
    df = DatasetGenerator.add_anomalies(df, anomaly_percentage=3)
    print(f"✓ Generated {len(df)} records")
    print(f"  Columns: {list(df.columns)}")
    print(f"  Memory usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
    
    # ========== STEP 2: DATA VALIDATION ==========
    print("\nStep 2: Data Validation...")
    print("-" * 80)
    validator = DataValidator()
    is_valid, validation_report = validator.validate(df)
    validator.print_report()
    
    if not is_valid:
        print("⚠ Data validation failed! Review errors before continuing.")
        # Don't exit - continue for demonstration purposes
    
    # ========== STEP 3: CALCULATE INCENTIVES ==========
    print("Step 3: Calculating Incentives...")
    print("-" * 80)
    incentive_engine = IncentiveEngine(base_salary_reference=100000)
    df = incentive_engine.calculate_incentives(df)
    df = incentive_engine.get_performance_tiers(df)
    summary = incentive_engine.get_incentive_summary(df)
    
    print(f"✓ Incentives calculated for {len(df)} employees")
    print(f"  Total Payout: ${summary['total_incentive_payout']:,.2f}")
    print(f"  Average Payout: ${summary['average_incentive_payout']:,.2f}")
    print(f"  Employees at Target: {summary['employees_at_target']}")
    print(f"  Employees with Growth Bonus: {summary['employees_with_growth_bonus']}")
    
    # ========== STEP 4: ANOMALY DETECTION ==========
    print("\nStep 4: Anomaly Detection...")
    print("-" * 80)
    anomaly_detector = AnomalyDetector(z_threshold=3.0, iqr_multiplier=1.5)
    df = anomaly_detector.detect_all(df)
    anomaly_detector.print_anomaly_report(df)
    
    # ========== STEP 5: DATABASE OPERATIONS ==========
    print("Step 5: Database Operations...")
    print("-" * 80)
    db = DatabaseManager(db_path='data/incentive_system.db', use_sqlite=True)
    db.create_tables()
    db.insert_employees(df)
    db.insert_sales_data(df)
    db.insert_incentives(df)
    db.insert_anomalies(df)
    
    print("\n✓ Database Operations Summary:")
    print("  Top Performers:")
    top_performers = db.query_top_performers(limit=5)
    print(top_performers[['employee_name', 'role', 'incentive_payout', 'performance_tier']].to_string(index=False))
    
    print("\n  Region Summary:")
    region_summary = db.query_region_summary()
    print(region_summary[['region', 'employee_count', 'total_sales', 'total_payout']].to_string(index=False))
    
    print("\n  Role Analysis:")
    role_analysis = db.query_role_analysis()
    print(role_analysis[['role', 'employee_count', 'total_payout', 'avg_payout']].to_string(index=False))
    
    # ========== STEP 6: ANALYTICS & VISUALIZATION ==========
    print("\nStep 6: Generating Analytics & Visualizations...")
    print("-" * 80)
    analytics = Analytics(output_dir='reports')
    analytics.generate_all_charts(df)
    
    # ========== STEP 7: REPORTING ==========
    print("\nStep 7: Generating Reports...")
    print("-" * 80)
    reporter = Reporter(output_dir='reports')
    reporter.generate_all_reports(df, incentive_engine, anomaly_detector)
    
    # ========== FINAL SUMMARY ==========
    print("\n" + "="*80)
    print("PROCESSING COMPLETE - SUMMARY")
    print("="*80)
    
    print(f"\n✓ Data Generation:        750 records created")
    print(f"✓ Data Validation:        {len(validation_report['errors'])} errors, {len(validation_report['warnings'])} warnings")
    print(f"✓ Incentive Calculation:  ${summary['total_incentive_payout']:,.2f} total payout")
    print(f"✓ Anomaly Detection:      {df['is_anomaly'].sum()} anomalies detected ({df['is_anomaly'].sum()/len(df)*100:.1f}%)")
    print(f"✓ Database:               Data persisted to SQLite")
    print(f"✓ Analytics:              6 charts generated")
    print(f"✓ Reports:                4 comprehensive reports generated")
    
    print(f"\n📂 Output Directory: ./reports/")
    print(f"💾 Database File:    ./data/incentive_system.db")
    
    print("\n" + "="*80)
    print("For interactive dashboard, run: streamlit run app.py")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
