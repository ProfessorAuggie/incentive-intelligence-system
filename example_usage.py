"""
Example Usage - Enterprise Incentive Intelligence System

This script demonstrates how to use each component of the system.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from dataset_generator import DatasetGenerator
from incentive_engine import IncentiveEngine
from validation import DataValidator
from anomaly_detection import AnomalyDetector
from database import DatabaseManager
from analytics import Analytics
from reporting import Reporter


def example_1_basic_workflow():
    """Example 1: Basic workflow with small dataset"""
    print("\n" + "="*70)
    print("EXAMPLE 1: BASIC WORKFLOW")
    print("="*70)
    
    # Generate data
    print("\n1. Generating dataset with 100 records...")
    generator = DatasetGenerator(num_records=100, seed=42)
    df = generator.generate()
    print(f"   ✓ Generated {len(df)} records")
    
    # Calculate incentives
    print("\n2. Calculating incentives...")
    engine = IncentiveEngine()
    df = engine.calculate_incentives(df)
    df = engine.get_performance_tiers(df)
    summary = engine.get_incentive_summary(df)
    print(f"   ✓ Total payout: ${summary['total_incentive_payout']:,.2f}")
    print(f"   ✓ Avg incentive: ${summary['average_incentive_payout']:,.2f}")
    
    # Display top earners
    print("\n3. Top 5 Earners:")
    top_5 = df.nlargest(5, 'incentive_payout')[
        ['employee_name', 'role', 'sales_amount', 'incentive_payout']
    ]
    for idx, (_, row) in enumerate(top_5.iterrows(), 1):
        print(f"   {idx}. {row['employee_name']:20} | Role: {row['role']:7} | "
              f"Payout: ${row['incentive_payout']:>10,.0f}")


def example_2_data_validation():
    """Example 2: Data validation with anomalies"""
    print("\n" + "="*70)
    print("EXAMPLE 2: DATA VALIDATION WITH ANOMALIES")
    print("="*70)
    
    # Generate data with anomalies
    print("\n1. Generating dataset with intentional anomalies...")
    generator = DatasetGenerator(num_records=100, seed=42)
    df = generator.generate()
    df = DatasetGenerator.add_anomalies(df, anomaly_percentage=5)
    print(f"   ✓ Generated {len(df)} records with 5% anomalies")
    
    # Validate data
    print("\n2. Running validation...")
    validator = DataValidator()
    is_valid, report = validator.validate(df)
    
    if report['errors']:
        print(f"   ⚠ Found {len(report['errors'])} critical errors:")
        for error in report['errors'][:3]:
            print(f"      • {error}")
    
    if report['warnings']:
        print(f"   ⚠ Found {len(report['warnings'])} warnings:")
        for warning in report['warnings'][:3]:
            print(f"      • {warning}")


def example_3_anomaly_detection():
    """Example 3: Anomaly detection"""
    print("\n" + "="*70)
    print("EXAMPLE 3: ANOMALY DETECTION")
    print("="*70)
    
    # Setup
    generator = DatasetGenerator(num_records=150, seed=42)
    df = generator.generate()
    df = DatasetGenerator.add_anomalies(df, anomaly_percentage=4)
    
    engine = IncentiveEngine()
    df = engine.calculate_incentives(df)
    
    # Detect anomalies
    print("\n1. Detecting anomalies...")
    detector = AnomalyDetector()
    df = detector.detect_all(df)
    report = detector.get_anomaly_report(df)
    
    print(f"   ✓ Total anomalies: {report['total_anomalies']} ({report['anomaly_percentage']:.1f}%)")
    
    if 'anomaly_types' in report and report['anomaly_types']:
        print("\n2. Anomaly Types Found:")
        for atype, count in sorted(report['anomaly_types'].items(), 
                                  key=lambda x: x[1], reverse=True):
            print(f"   • {atype:40} {count:3} cases")


def example_4_database_operations():
    """Example 4: Database operations"""
    print("\n" + "="*70)
    print("EXAMPLE 4: DATABASE OPERATIONS")
    print("="*70)
    
    # Setup
    generator = DatasetGenerator(num_records=200, seed=42)
    df = generator.generate()
    
    engine = IncentiveEngine()
    df = engine.calculate_incentives(df)
    df = engine.get_performance_tiers(df)
    
    detector = AnomalyDetector()
    df = detector.detect_all(df)
    
    # Database operations
    print("\n1. Creating and populating database...")
    db = DatabaseManager(db_path='data/example.db')
    db.create_tables()
    db.insert_employees(df)
    db.insert_sales_data(df)
    db.insert_incentives(df)
    db.insert_anomalies(df)
    print("   ✓ Database operations complete")
    
    # Query examples
    print("\n2. Top 5 Performers (from database):")
    top = db.query_top_performers(limit=5)
    for idx, (_, row) in enumerate(top.iterrows(), 1):
        print(f"   {idx}. {row['employee_name']:20} | "
              f"Region: {row['region']:15} | Payout: ${row['incentive_payout']:>10,.0f}")
    
    print("\n3. Regional Summary:")
    regions = db.query_region_summary()
    for _, row in regions.iterrows():
        print(f"   {row['region']:20} | Employees: {row['employee_count']:3} | "
              f"Total: ${row['total_payout']:>15,.0f}")


def example_5_analytics():
    """Example 5: Analytics without full visualization"""
    print("\n" + "="*70)
    print("EXAMPLE 5: ANALYTICS SUMMARY")
    print("="*70)
    
    # Setup
    generator = DatasetGenerator(num_records=200, seed=42)
    df = generator.generate()
    
    engine = IncentiveEngine()
    df = engine.calculate_incentives(df)
    df = engine.get_performance_tiers(df)
    
    # Analytics
    analytics = Analytics()
    
    print("\n1. Regional Performance Analysis:")
    region_stats = analytics.analyze_region_performance(df)
    print(region_stats.to_string())
    
    print("\n2. Key Statistics:")
    print(f"   Total Sales: ${df['sales_amount'].sum():,.0f}")
    print(f"   Total Incentive: ${df['incentive_payout'].sum():,.0f}")
    print(f"   Avg Achievement: {(df['achievement_ratio'].mean()*100):.1f}%")


def example_6_full_pipeline():
    """Example 6: Full pipeline with reports"""
    print("\n" + "="*70)
    print("EXAMPLE 6: FULL PIPELINE (MINIMAL)")
    print("="*70 + "\n")
    
    # Generate
    print("Step 1: Generating 300 records...")
    generator = DatasetGenerator(num_records=300, seed=42)
    df = generator.generate()
    df = DatasetGenerator.add_anomalies(df, anomaly_percentage=3)
    
    # Validate
    print("Step 2: Validating data...")
    validator = DataValidator()
    is_valid, _ = validator.validate(df)
    print(f"   Status: {'✓ VALID' if is_valid else '✗ INVALID'}")
    
    # Calculate incentives
    print("Step 3: Calculating incentives...")
    engine = IncentiveEngine()
    df = engine.calculate_incentives(df)
    df = engine.get_performance_tiers(df)
    
    # Detect anomalies
    print("Step 4: Detecting anomalies...")
    detector = AnomalyDetector()
    df = detector.detect_all(df)
    
    # Generate reports (text only)
    print("Step 5: Generating reports...")
    reporter = Reporter(output_dir='reports')
    
    exec_summary = reporter.generate_executive_summary(df, engine)
    reporter.save_report(exec_summary, 'example_executive_summary.txt')
    
    top_report = reporter.generate_top_performers_report(df, limit=10)
    reporter.save_report(top_report, 'example_top_performers.txt')
    
    anomaly_report = reporter.generate_anomaly_report(df, detector)
    reporter.save_report(anomaly_report, 'example_anomaly_report.txt')
    
    print(f"\n✓ Pipeline complete!")
    print(f"  Total Payout: ${df['incentive_payout'].sum():,.0f}")
    print(f"  Anomalies: {df['is_anomaly'].sum()}")
    print(f"  Reports saved to ./reports/")


if __name__ == "__main__":
    # Run examples
    example_1_basic_workflow()
    example_2_data_validation()
    example_3_anomaly_detection()
    example_4_database_operations()
    example_5_analytics()
    example_6_full_pipeline()
    
    print("\n" + "="*70)
    print("ALL EXAMPLES COMPLETED")
    print("="*70)
    print("\nFor full system execution, run: python main.py")
    print("For interactive dashboard, run: streamlit run app.py")
