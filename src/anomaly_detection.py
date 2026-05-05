"""
Anomaly Detection Module
Identifies unusual patterns in incentive data
"""

import pandas as pd
import numpy as np
from scipy import stats

class AnomalyDetector:
    """Detects anomalies in employee incentive data"""
    
    def __init__(self, z_threshold=3.0, iqr_multiplier=1.5):
        """
        Initialize anomaly detector
        
        Args:
            z_threshold (float): Z-score threshold for outliers
            iqr_multiplier (float): IQR multiplier for outlier detection
        """
        self.z_threshold = z_threshold
        self.iqr_multiplier = iqr_multiplier
        self.anomalies = []
    
    def detect_all(self, df):
        """
        Run all anomaly detection methods
        
        Args:
            df (pd.DataFrame): Data with incentive calculations
        
        Returns:
            pd.DataFrame: Original data with anomaly flags
        """
        self.anomalies = []
        df = df.copy()
        
        df['anomaly_flags'] = ""
        
        # Run all detection methods
        high_incentive_anomalies = self._detect_high_incentive_outliers(df)
        zero_incentive_anomalies = self._detect_zero_incentive_high_sales(df)
        extreme_growth_anomalies = self._detect_extreme_growth(df)
        data_quality_anomalies = self._detect_data_quality_issues(df)
        role_performance_anomalies = self._detect_role_mismatch(df)
        
        # Combine all anomalies
        all_anomalies = (
            high_incentive_anomalies | 
            zero_incentive_anomalies | 
            extreme_growth_anomalies | 
            data_quality_anomalies |
            role_performance_anomalies
        )
        
        # Mark anomalous records
        df.loc[all_anomalies, 'is_anomaly'] = True
        df.loc[~all_anomalies, 'is_anomaly'] = False
        
        # Create summary of anomaly types
        for idx in df[all_anomalies].index:
            flags = []
            if high_incentive_anomalies.loc[idx]:
                flags.append("HIGH_INCENTIVE_OUTLIER")
            if zero_incentive_anomalies.loc[idx]:
                flags.append("ZERO_INCENTIVE_HIGH_SALES")
            if extreme_growth_anomalies.loc[idx]:
                flags.append("EXTREME_GROWTH")
            if data_quality_anomalies.loc[idx]:
                flags.append("DATA_QUALITY_ISSUE")
            if role_performance_anomalies.loc[idx]:
                flags.append("ROLE_PERFORMANCE_MISMATCH")
            
            df.at[idx, 'anomaly_flags'] = "; ".join(flags)
        
        return df
    
    def _detect_high_incentive_outliers(self, df):
        """Detect unusually high incentive payouts"""
        if 'incentive_payout' not in df.columns:
            return pd.Series([False] * len(df), index=df.index)
        
        z_scores = np.abs(stats.zscore(df['incentive_payout'].fillna(0)))
        return z_scores > self.z_threshold
    
    def _detect_zero_incentive_high_sales(self, df):
        """Detect employees with high sales but zero incentive"""
        if 'incentive_payout' not in df.columns or 'sales_target' not in df.columns:
            return pd.Series([False] * len(df), index=df.index)
        
        high_sales = df['sales_amount'] >= df['sales_target'] * 0.9
        zero_incentive = df['incentive_payout'] == 0
        
        return high_sales & zero_incentive
    
    def _detect_extreme_growth(self, df):
        """Detect extreme quarter-over-quarter growth"""
        if 'sales_amount' not in df.columns or 'previous_quarter_sales' not in df.columns:
            return pd.Series([False] * len(df), index=df.index)
        
        df_copy = df.copy()
        df_copy = df_copy[df_copy['previous_quarter_sales'] > 0]
        
        anomalies = pd.Series([False] * len(df), index=df.index)
        
        growth_rates = (df_copy['sales_amount'] - df_copy['previous_quarter_sales']) / df_copy['previous_quarter_sales']
        extreme = growth_rates > 5  # > 500% growth
        
        anomalies.loc[df_copy[extreme].index] = True
        return anomalies
    
    def _detect_data_quality_issues(self, df):
        """Detect data quality issues"""
        issues = pd.Series([False] * len(df), index=df.index)
        
        # Null values in critical fields
        if 'sales_amount' in df.columns:
            issues |= df['sales_amount'].isnull()
        if 'sales_target' in df.columns:
            issues |= df['sales_target'].isnull()
        
        # Negative values
        if 'sales_amount' in df.columns:
            issues |= df['sales_amount'] < 0
        if 'sales_target' in df.columns:
            issues |= df['sales_target'] < 0
        
        return issues
    
    def _detect_role_mismatch(self, df):
        """Detect role-specific anomalies"""
        if 'role' not in df.columns or 'incentive_payout' not in df.columns:
            return pd.Series([False] * len(df), index=df.index)
        
        anomalies = pd.Series([False] * len(df), index=df.index)
        
        # Managers with extremely low incentives despite high sales
        managers = df[df['role'] == 'Manager']
        if len(managers) > 0:
            mgr_incentives = managers['incentive_payout']
            mgr_threshold = mgr_incentives.mean() * 0.1  # Bottom 10%
            
            low_pay_high_sales = (
                (managers['incentive_payout'] < mgr_threshold) & 
                (managers['sales_amount'] > managers['sales_target'])
            )
            anomalies.loc[low_pay_high_sales.index] = True
        
        return anomalies
    
    def get_anomaly_report(self, df):
        """
        Generate anomaly report
        
        Args:
            df (pd.DataFrame): Data with is_anomaly flag
        
        Returns:
            dict: Anomaly statistics
        """
        total_anomalies = df['is_anomaly'].sum() if 'is_anomaly' in df.columns else 0
        
        report = {
            'total_anomalies': total_anomalies,
            'anomaly_percentage': (total_anomalies / len(df) * 100) if len(df) > 0 else 0,
            'anomalous_records': df[df['is_anomaly']] if 'is_anomaly' in df.columns else pd.DataFrame(),
        }
        
        # Count anomaly types
        if 'anomaly_flags' in df.columns:
            anomaly_counts = {}
            for flags in df[df['is_anomaly']]['anomaly_flags']:
                for flag in flags.split("; "):
                    if flag:
                        anomaly_counts[flag] = anomaly_counts.get(flag, 0) + 1
            report['anomaly_types'] = anomaly_counts
        
        return report
    
    def print_anomaly_report(self, df):
        """Print formatted anomaly report"""
        report = self.get_anomaly_report(df)
        
        print("\n" + "="*70)
        print("ANOMALY DETECTION REPORT")
        print("="*70)
        print(f"Total Anomalies: {report['total_anomalies']}")
        print(f"Anomaly Percentage: {report['anomaly_percentage']:.2f}%")
        print("="*70)
        
        if 'anomaly_types' in report and report['anomaly_types']:
            print("\nANOMALY TYPES:")
            for anomaly_type, count in sorted(report['anomaly_types'].items(), 
                                             key=lambda x: x[1], reverse=True):
                print(f"  • {anomaly_type}: {count}")
        
        if len(report['anomalous_records']) > 0:
            print("\nTOP ANOMALOUS RECORDS:")
            display_cols = ['employee_name', 'role', 'sales_target', 
                           'sales_amount', 'incentive_payout', 'anomaly_flags']
            available_cols = [col for col in display_cols if col in report['anomalous_records'].columns]
            
            print(report['anomalous_records'][available_cols].head(10).to_string())
        
        print("="*70 + "\n")

if __name__ == "__main__":
    from dataset_generator import DatasetGenerator
    from incentive_engine import IncentiveEngine
    
    generator = DatasetGenerator(num_records=100)
    df = generator.generate()
    df = DatasetGenerator.add_anomalies(df, anomaly_percentage=5)
    
    engine = IncentiveEngine()
    df = engine.calculate_incentives(df)
    
    detector = AnomalyDetector()
    df = detector.detect_all(df)
    detector.print_anomaly_report(df)
