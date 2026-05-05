"""
Dataset Generator Module
Generates synthetic employee incentive data for simulation
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class DatasetGenerator:
    """Generates realistic synthetic incentive data"""
    
    def __init__(self, num_records=750, seed=42):
        """
        Initialize dataset generator
        
        Args:
            num_records (int): Number of records to generate
            seed (int): Random seed for reproducibility
        """
        self.num_records = num_records
        np.random.seed(seed)
        random.seed(seed)
    
    def generate(self):
        """Generate complete synthetic dataset"""
        data = {
            'employee_id': self._generate_employee_ids(),
            'employee_name': self._generate_names(),
            'region': self._generate_regions(),
            'role': self._generate_roles(),
            'quarter': self._generate_quarters(),
            'sales_target': self._generate_targets(),
            'sales_amount': self._generate_sales(),
            'previous_quarter_sales': self._generate_previous_sales(),
        }
        
        df = pd.DataFrame(data)
        df = self._add_team_info(df)
        return df
    
    def _generate_employee_ids(self):
        """Generate unique employee IDs"""
        return [f'EMP{str(i).zfill(5)}' for i in range(1, self.num_records + 1)]
    
    def _generate_names(self):
        """Generate employee names"""
        first_names = ['James', 'Sarah', 'Michael', 'Emma', 'David', 'Lisa', 'Robert', 'Jennifer',
                      'William', 'Mary', 'John', 'Patricia', 'Charles', 'Linda', 'Thomas',
                      'Barbara', 'Christopher', 'Elizabeth', 'Daniel', 'Susan', 'Matthew',
                      'Jessica', 'Anthony', 'Karen', 'Mark', 'Nancy', 'Donald', 'Lisa']
        
        last_names = ['Johnson', 'Smith', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller',
                     'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez',
                     'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin',
                     'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark']
        
        return [f"{random.choice(first_names)} {random.choice(last_names)}" 
                for _ in range(self.num_records)]
    
    def _generate_regions(self):
        """Generate geographical regions"""
        regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East Africa']
        return [random.choice(regions) for _ in range(self.num_records)]
    
    def _generate_roles(self):
        """Generate employee roles"""
        roles = []
        for _ in range(self.num_records):
            # 70% Sales, 30% Manager
            role = random.choices(['Sales', 'Manager'], weights=[0.7, 0.3])[0]
            roles.append(role)
        return roles
    
    def _generate_quarters(self):
        """Generate quarter data"""
        quarters = []
        for _ in range(self.num_records):
            year = random.choice([2023, 2024, 2025])
            quarter = random.choice(['Q1', 'Q2', 'Q3', 'Q4'])
            quarters.append(f"{year}-{quarter}")
        return quarters
    
    def _generate_targets(self):
        """Generate sales targets (50k to 500k)"""
        return np.random.exponential(150000, self.num_records)
    
    def _generate_sales(self):
        """Generate sales amounts with realistic distribution"""
        sales = []
        for target in self._generate_targets():
            # 60% meet target, 25% exceed 150%, 15% below
            probability = random.random()
            if probability < 0.60:
                # Hit target range (80-100%)
                sales_val = target * np.random.uniform(0.80, 1.0)
            elif probability < 0.85:
                # Exceed target (150%+)
                sales_val = target * np.random.uniform(1.50, 2.5)
            else:
                # Below target (0-70%)
                sales_val = target * np.random.uniform(0, 0.70)
            
            sales.append(max(0, sales_val))
        return sales
    
    def _generate_previous_sales(self):
        """Generate previous quarter sales"""
        previous = []
        for target in self._generate_targets():
            # Slightly vary from current target
            prev_val = target * np.random.uniform(0.8, 1.2)
            previous.append(max(0, prev_val))
        return previous
    
    def _add_team_info(self, df):
        """Add team information for managers"""
        df['team_size'] = 1
        df['team_performance'] = 1.0
        
        # Add team info for managers
        for idx, row in df.iterrows():
            if row['role'] == 'Manager':
                # Random team size 3-15
                team_size = random.randint(3, 15)
                df.at[idx, 'team_size'] = team_size
                # Random team performance 0.8-1.3
                df.at[idx, 'team_performance'] = np.random.uniform(0.8, 1.3)
        
        return df
    
    @staticmethod
    def add_anomalies(df, anomaly_percentage=2):
        """
        Add intentional anomalies for testing detection
        
        Args:
            df (pd.DataFrame): Original dataset
            anomaly_percentage (float): Percentage of records to make anomalous
        
        Returns:
            pd.DataFrame: Dataset with anomalies
        """
        df = df.copy()
        num_anomalies = max(1, int(len(df) * anomaly_percentage / 100))
        anomaly_indices = np.random.choice(df.index, num_anomalies, replace=False)
        
        for idx in anomaly_indices:
            anomaly_type = random.choice([1, 2, 3])
            
            if anomaly_type == 1:
                # Unrealistic high sales
                df.at[idx, 'sales_amount'] = df.at[idx, 'sales_target'] * 10
            elif anomaly_type == 2:
                # Null values
                df.at[idx, 'sales_amount'] = np.nan
            else:
                # Negative sales (data entry error)
                df.at[idx, 'sales_amount'] = -abs(df.at[idx, 'sales_target'] * 0.5)
        
        return df

if __name__ == "__main__":
    generator = DatasetGenerator(num_records=750)
    df = generator.generate()
    df = DatasetGenerator.add_anomalies(df, anomaly_percentage=2)
    print(f"Generated {len(df)} records")
    print(df.head(10))
    print(f"\nDataset shape: {df.shape}")
    print(f"\nData types:\n{df.dtypes}")
