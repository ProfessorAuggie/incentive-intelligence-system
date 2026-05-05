"""
Reporting Module
Generates comprehensive reports and exports
"""

import pandas as pd
import os
from datetime import datetime

class Reporter:
    """Generates reports and exports data"""
    
    def __init__(self, output_dir='reports'):
        """
        Initialize reporter
        
        Args:
            output_dir (str): Directory for saving reports
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_executive_summary(self, df, incentive_engine):
        """
        Generate executive summary report
        
        Args:
            df (pd.DataFrame): Complete dataset
            incentive_engine (IncentiveEngine): Engine with summary methods
        
        Returns:
            str: Report text
        """
        summary = incentive_engine.get_incentive_summary(df)
        
        report = []
        report.append("="*80)
        report.append("EXECUTIVE SUMMARY REPORT")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("="*80)
        
        report.append("\n1. FINANCIAL OVERVIEW")
        report.append("-" * 80)
        report.append(f"Total Incentive Payout:        ${summary['total_incentive_payout']:>20,.2f}")
        report.append(f"Average Incentive Payout:      ${summary['average_incentive_payout']:>20,.2f}")
        report.append(f"Median Incentive Payout:       ${summary['median_incentive_payout']:>20,.2f}")
        report.append(f"Maximum Payout:                ${summary['max_incentive_payout']:>20,.2f}")
        report.append(f"Minimum Payout:                ${summary['min_incentive_payout']:>20,.2f}")
        report.append(f"Standard Deviation:            ${summary['std_dev_incentive']:>20,.2f}")
        
        report.append("\n2. PERFORMANCE METRICS")
        report.append("-" * 80)
        report.append(f"Total Employees:               {len(df):>20,}")
        report.append(f"Employees at Target:           {summary['employees_at_target']:>20,}")
        report.append(f"Employees Below Target:        {summary['employees_below_target']:>20,}")
        report.append(f"Achievement Rate:              {(summary['employees_at_target']/len(df)*100):>19.1f}%")
        
        report.append("\n3. BONUS ANALYSIS")
        report.append("-" * 80)
        report.append(f"Employees with Growth Bonus:   {summary['employees_with_growth_bonus']:>20,}")
        report.append(f"Total Growth Bonuses:          ${summary['total_growth_bonuses']:>20,.2f}")
        report.append(f"Total Manager Bonuses:         ${summary['total_manager_bonuses']:>20,.2f}")
        
        report.append("\n4. REGIONAL BREAKDOWN")
        report.append("-" * 80)
        region_summary = df.groupby('region').agg({
            'employee_id': 'count',
            'sales_amount': 'sum',
            'incentive_payout': 'sum'
        }).round(2)
        region_summary.columns = ['Employees', 'Total Sales', 'Total Incentive']
        
        for region, row in region_summary.iterrows():
            report.append(f"{region:<30} | Emps: {row['Employees']:>4.0f} | "
                         f"Sales: ${row['Total Sales']:>15,.0f} | "
                         f"Incentive: ${row['Total Incentive']:>15,.0f}")
        
        report.append("\n" + "="*80)
        
        return "\n".join(report)
    
    def generate_top_performers_report(self, df, limit=20):
        """
        Generate top performers report
        
        Args:
            df (pd.DataFrame): Complete dataset
            limit (int): Number of top performers
        
        Returns:
            str: Report text
        """
        report = []
        report.append("="*120)
        report.append(f"TOP {limit} PERFORMERS")
        report.append("="*120)
        
        top_performers = df.nlargest(limit, 'incentive_payout')[
            ['employee_id', 'employee_name', 'role', 'region', 'sales_target', 
             'sales_amount', 'achievement_ratio', 'incentive_payout', 'performance_tier']
        ]
        
        # Format and print
        for idx, (_, row) in enumerate(top_performers.iterrows(), 1):
            report.append(f"\n{idx}. {row['employee_name']} ({row['employee_id']})")
            report.append(f"   Role: {row['role']:12} | Region: {row['region']:20} | Tier: {row['performance_tier']}")
            report.append(f"   Sales Target: ${row['sales_target']:>15,.0f} | Sales: ${row['sales_amount']:>15,.0f}")
            report.append(f"   Achievement: {row['achievement_ratio']*100:>5.1f}% | Payout: ${row['incentive_payout']:>15,.2f}")
        
        report.append("\n" + "="*120)
        
        return "\n".join(report)
    
    def generate_anomaly_report(self, df, anomaly_detector):
        """
        Generate anomaly report
        
        Args:
            df (pd.DataFrame): Dataset with anomaly flags
            anomaly_detector (AnomalyDetector): Detector with report methods
        
        Returns:
            str: Report text
        """
        anomaly_report = anomaly_detector.get_anomaly_report(df)
        
        report = []
        report.append("="*100)
        report.append("ANOMALY DETECTION REPORT")
        report.append("="*100)
        
        report.append(f"\nTotal Anomalies Found: {anomaly_report['total_anomalies']}")
        report.append(f"Anomaly Percentage: {anomaly_report['anomaly_percentage']:.2f}%")
        
        if 'anomaly_types' in anomaly_report and anomaly_report['anomaly_types']:
            report.append("\nANOMALY BREAKDOWN:")
            report.append("-" * 100)
            for anomaly_type, count in sorted(anomaly_report['anomaly_types'].items(), 
                                             key=lambda x: x[1], reverse=True):
                percentage = (count / anomaly_report['total_anomalies'] * 100) if anomaly_report['total_anomalies'] > 0 else 0
                report.append(f"  • {anomaly_type:<40} {count:>5} cases ({percentage:>5.1f}%)")
        
        if len(anomaly_report['anomalous_records']) > 0:
            report.append("\nDETAILED ANOMALOUS RECORDS:")
            report.append("-" * 100)
            
            anomalies = anomaly_report['anomalous_records'].copy()
            for _, row in anomalies.head(20).iterrows():
                report.append(f"\n• {row['employee_name']} ({row['employee_id']})")
                report.append(f"  Region: {row['region']:20} | Role: {row['role']}")
                report.append(f"  Sales: ${row['sales_amount']:>15,.0f} | Target: ${row['sales_target']:>15,.0f}")
                report.append(f"  Incentive: ${row['incentive_payout']:>15,.2f}")
                if 'anomaly_flags' in row:
                    report.append(f"  Issues: {row['anomaly_flags']}")
        
        report.append("\n" + "="*100)
        
        return "\n".join(report)
    
    def generate_region_report(self, df):
        """
        Generate detailed regional analysis
        
        Args:
            df (pd.DataFrame): Complete dataset
        
        Returns:
            str: Report text
        """
        report = []
        report.append("="*100)
        report.append("REGIONAL PERFORMANCE ANALYSIS")
        report.append("="*100)
        
        regions = df['region'].unique()
        
        for region in sorted(regions):
            region_data = df[df['region'] == region]
            
            report.append(f"\n{region}")
            report.append("-" * 100)
            report.append(f"  Employees:              {len(region_data):>10,}")
            report.append(f"  Total Sales:            ${region_data['sales_amount'].sum():>15,.0f}")
            report.append(f"  Average Sales:          ${region_data['sales_amount'].mean():>15,.0f}")
            report.append(f"  Total Incentive Payout: ${region_data['incentive_payout'].sum():>15,.0f}")
            report.append(f"  Average Incentive:      ${region_data['incentive_payout'].mean():>15,.0f}")
            
            # Achievement stats
            at_target = (region_data['achievement_ratio'] >= 1.0).sum()
            report.append(f"  Achievement Rate:       {(at_target/len(region_data)*100):>14.1f}%")
            
            # Top performer
            top = region_data.nlargest(1, 'incentive_payout')
            if len(top) > 0:
                report.append(f"  Top Performer:          {top.iloc[0]['employee_name']}")
        
        report.append("\n" + "="*100)
        
        return "\n".join(report)
    
    def export_to_csv(self, df, filename):
        """
        Export dataframe to CSV
        
        Args:
            df (pd.DataFrame): Data to export
            filename (str): Output filename
        
        Returns:
            str: File path
        """
        filepath = f'{self.output_dir}/{filename}'
        df.to_csv(filepath, index=False)
        print(f"✓ Exported to {filepath}")
        return filepath
    
    def export_to_excel(self, dfs_dict, filename):
        """
        Export multiple dataframes to Excel sheets
        
        Args:
            dfs_dict (dict): Dictionary of dataframe_name: dataframe
            filename (str): Output filename
        
        Returns:
            str: File path
        """
        try:
            filepath = f'{self.output_dir}/{filename}'
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                for sheet_name, df in dfs_dict.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"✓ Exported to {filepath}")
            return filepath
        except Exception as e:
            print(f"✗ Error exporting to Excel: {e}")
            return None
    
    def save_report(self, report_text, filename):
        """
        Save report to text file
        
        Args:
            report_text (str): Report content
            filename (str): Output filename
        
        Returns:
            str: File path
        """
        filepath = f'{self.output_dir}/{filename}'
        with open(filepath, 'w') as f:
            f.write(report_text)
        print(f"✓ Saved report: {filepath}")
        return filepath
    
    def generate_all_reports(self, df, incentive_engine, anomaly_detector):
        """
        Generate all reports
        
        Args:
            df (pd.DataFrame): Complete dataset
            incentive_engine (IncentiveEngine): Engine with calculations
            anomaly_detector (AnomalyDetector): Detector for anomalies
        """
        print("\n" + "="*70)
        print("GENERATING REPORTS")
        print("="*70)
        
        # Executive summary
        exec_summary = self.generate_executive_summary(df, incentive_engine)
        self.save_report(exec_summary, f'executive_summary_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
        
        # Top performers
        top_report = self.generate_top_performers_report(df)
        self.save_report(top_report, f'top_performers_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
        
        # Anomalies
        anomaly_report = self.generate_anomaly_report(df, anomaly_detector)
        self.save_report(anomaly_report, f'anomaly_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
        
        # Regional analysis
        region_report = self.generate_region_report(df)
        self.save_report(region_report, f'regional_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
        
        # Data exports
        self.export_to_csv(df, f'complete_dataset_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
        
        print("="*70 + "\n")

if __name__ == "__main__":
    from dataset_generator import DatasetGenerator
    from incentive_engine import IncentiveEngine
    from anomaly_detection import AnomalyDetector
    
    generator = DatasetGenerator(num_records=100)
    df = generator.generate()
    df = DatasetGenerator.add_anomalies(df, anomaly_percentage=5)
    
    engine = IncentiveEngine()
    df = engine.calculate_incentives(df)
    df = engine.get_performance_tiers(df)
    
    detector = AnomalyDetector()
    df = detector.detect_all(df)
    
    reporter = Reporter()
    reporter.generate_all_reports(df, engine, detector)
