"""
Data Validation Module
Validates data quality and identifies issues
"""

import pandas as pd
import numpy as np
from datetime import datetime

class DataValidator:
    """Validates employee incentive data"""
    
    def __init__(self):
        self.validation_errors = []
        self.validation_warnings = []
    
    def validate(self, df):
        """
        Perform comprehensive validation on dataset
        
        Args:
            df (pd.DataFrame): Data to validate
        
        Returns:
            tuple: (is_valid, validation_report)
        """
        self.validation_errors = []
        self.validation_warnings = []
        
        # Run all validations
        self._validate_structure(df)
        self._validate_nulls(df)
        self._validate_ranges(df)
        self._validate_consistency(df)
        self._validate_business_logic(df)
        
        is_valid = len(self.validation_errors) == 0
        report = self.get_report()
        
        return is_valid, report
    
    def _validate_structure(self, df):
        """Validate dataset structure"""
        required_columns = [
            'employee_id', 'employee_name', 'region', 'role',
            'sales_amount', 'sales_target', 'quarter', 'previous_quarter_sales'
        ]
        
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            self.validation_errors.append(f"Missing required columns: {missing_cols}")
        
        if df.empty:
            self.validation_errors.append("Dataset is empty")
        
        if len(df) < 10:
            self.validation_warnings.append(f"Dataset has only {len(df)} records (< 10)")
    
    def _validate_nulls(self, df):
        """Detect null values"""
        null_counts = df.isnull().sum()
        
        for col in null_counts[null_counts > 0].index:
            count = null_counts[col]
            percentage = (count / len(df)) * 100
            
            if col in ['employee_id', 'sales_amount', 'sales_target']:
                self.validation_errors.append(
                    f"Critical field '{col}' has {count} nulls ({percentage:.1f}%)"
                )
            else:
                self.validation_warnings.append(
                    f"Field '{col}' has {count} nulls ({percentage:.1f}%)"
                )
    
    def _validate_ranges(self, df):
        """Validate value ranges"""
        
        # Sales amount validation
        if 'sales_amount' in df.columns:
            negative_sales = (df['sales_amount'] < 0).sum()
            if negative_sales > 0:
                self.validation_errors.append(
                    f"{negative_sales} records have negative sales amounts"
                )
            
            # Check for unrealistic values (> 10x target)
            if 'sales_target' in df.columns:
                unrealistic = (df['sales_amount'] > df['sales_target'] * 10).sum()
                if unrealistic > 0:
                    self.validation_warnings.append(
                        f"{unrealistic} records have sales > 10x target (possible data entry errors)"
                    )
        
        # Sales target validation
        if 'sales_target' in df.columns:
            negative_targets = (df['sales_target'] < 0).sum()
            if negative_targets > 0:
                self.validation_errors.append(
                    f"{negative_targets} records have negative sales targets"
                )
            
            zero_targets = (df['sales_target'] == 0).sum()
            if zero_targets > 0:
                self.validation_errors.append(
                    f"{zero_targets} records have zero sales targets"
                )
        
        # Previous quarter sales validation
        if 'previous_quarter_sales' in df.columns:
            negative_prev = (df['previous_quarter_sales'] < 0).sum()
            if negative_prev > 0:
                self.validation_errors.append(
                    f"{negative_prev} records have negative previous quarter sales"
                )
    
    def _validate_consistency(self, df):
        """Validate data consistency"""
        
        # Employee ID should be unique
        if 'employee_id' in df.columns:
            duplicates = df['employee_id'].duplicated().sum()
            if duplicates > 0:
                self.validation_warnings.append(
                    f"{duplicates} duplicate employee IDs detected"
                )
        
        # Role validation
        if 'role' in df.columns:
            valid_roles = ['Sales', 'Manager']
            invalid_roles = df[~df['role'].isin(valid_roles)]['role'].unique()
            if len(invalid_roles) > 0:
                self.validation_warnings.append(
                    f"Invalid roles found: {list(invalid_roles)}"
                )
        
        # Region validation
        if 'region' in df.columns:
            valid_regions = [
                'North America', 'Europe', 'Asia Pacific', 
                'Latin America', 'Middle East Africa'
            ]
            invalid_regions = df[~df['region'].isin(valid_regions)]['region'].unique()
            if len(invalid_regions) > 0:
                self.validation_warnings.append(
                    f"Unexpected regions: {list(invalid_regions)}"
                )
    
    def _validate_business_logic(self, df):
        """Validate business logic constraints"""
        
        # Growth rate should be reasonable
        if 'previous_quarter_sales' in df.columns and 'sales_amount' in df.columns:
            df_copy = df.copy()
            df_copy = df_copy[df_copy['previous_quarter_sales'] > 0]
            
            if len(df_copy) > 0:
                growth_rates = (df_copy['sales_amount'] - df_copy['previous_quarter_sales']) / df_copy['previous_quarter_sales']
                extreme_growth = (growth_rates > 5).sum()  # 500%+ growth
                
                if extreme_growth > 0:
                    self.validation_warnings.append(
                        f"{extreme_growth} records show > 500% quarter growth (verify data)"
                    )
    
    def get_report(self):
        """Get detailed validation report"""
        report = {
            'valid': len(self.validation_errors) == 0,
            'error_count': len(self.validation_errors),
            'warning_count': len(self.validation_warnings),
            'errors': self.validation_errors,
            'warnings': self.validation_warnings,
            'timestamp': datetime.now().isoformat()
        }
        return report
    
    def print_report(self):
        """Print formatted validation report"""
        report = self.get_report()
        
        print("\n" + "="*70)
        print("DATA VALIDATION REPORT")
        print("="*70)
        print(f"Status: {'✓ VALID' if report['valid'] else '✗ INVALID'}")
        print(f"Errors: {report['error_count']}")
        print(f"Warnings: {report['warning_count']}")
        print(f"Timestamp: {report['timestamp']}")
        print("="*70)
        
        if report['errors']:
            print("\nCRITICAL ERRORS:")
            for i, error in enumerate(report['errors'], 1):
                print(f"  {i}. {error}")
        
        if report['warnings']:
            print("\nWARNINGS:")
            for i, warning in enumerate(report['warnings'], 1):
                print(f"  {i}. {warning}")
        
        if not report['errors'] and not report['warnings']:
            print("\n✓ All validations passed!")
        
        print("="*70 + "\n")

if __name__ == "__main__":
    from dataset_generator import DatasetGenerator
    
    generator = DatasetGenerator(num_records=100)
    df = generator.generate()
    df = DatasetGenerator.add_anomalies(df, anomaly_percentage=5)
    
    validator = DataValidator()
    is_valid, report = validator.validate(df)
    validator.print_report()
