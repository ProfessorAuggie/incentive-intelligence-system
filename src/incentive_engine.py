"""
Incentive Engine Module
Calculates employee incentive payouts based on sales performance
"""

import pandas as pd
import numpy as np

class IncentiveEngine:
    """Calculates incentive payouts based on business rules"""
    
    # Incentive rules constants
    BASE_SALARY_PERCENTAGE = 0.60  # 60% of target as reference
    PAYOUT_AT_TARGET = 0.10  # 10% at 100% target
    PAYOUT_AT_150_PERCENT = 0.20  # 20% at 150% target
    GROWTH_BONUS = 0.05  # 5% bonus for 20%+ growth
    GROWTH_THRESHOLD = 0.20  # 20% growth threshold
    
    def __init__(self, base_salary_reference=100000):
        """
        Initialize incentive engine
        
        Args:
            base_salary_reference (float): Reference salary for calculations
        """
        self.base_salary_reference = base_salary_reference
    
    def calculate_incentives(self, df):
        """
        Calculate incentives for all employees
        
        Args:
            df (pd.DataFrame): Employee data with sales information
        
        Returns:
            pd.DataFrame: Original data with incentive columns added
        """
        df = df.copy()
        
        # Calculate base incentives
        df['achievement_ratio'] = df['sales_amount'] / df['sales_target']
        df['base_incentive'] = df.apply(self._calculate_base_incentive, axis=1)
        
        # Calculate growth bonus
        df['growth_rate'] = (df['sales_amount'] - df['previous_quarter_sales']) / df['previous_quarter_sales']
        df['growth_bonus'] = df.apply(self._calculate_growth_bonus, axis=1)
        
        # Calculate role-specific bonuses
        df['role_bonus'] = df.apply(self._calculate_role_bonus, axis=1)
        
        # Calculate total incentive
        df['total_incentive'] = df['base_incentive'] + df['growth_bonus'] + df['role_bonus']
        
        # Calculate payout amount
        df['incentive_payout'] = (df['sales_target'] * df['total_incentive']).round(2)
        
        return df
    
    def _calculate_base_incentive(self, row):
        """Calculate base incentive percentage"""
        try:
            achievement = row['sales_amount'] / row['sales_target']
            
            if achievement >= 1.5:
                # 20% at 150%+ achievement
                return self.PAYOUT_AT_150_PERCENT
            elif achievement >= 1.0:
                # 10% at 100%+ achievement
                return self.PAYOUT_AT_TARGET
            elif achievement >= 0.8:
                # 5% at 80%+ achievement (partial credit)
                return 0.05
            else:
                # No payout below 80%
                return 0.0
        except (ZeroDivisionError, TypeError):
            return 0.0
    
    def _calculate_growth_bonus(self, row):
        """Calculate bonus for growth over previous quarter"""
        try:
            if row['previous_quarter_sales'] == 0:
                growth_rate = 0
            else:
                growth_rate = row['growth_rate']
            
            if growth_rate >= self.GROWTH_THRESHOLD:
                # 5% additional bonus for 20%+ growth
                return self.GROWTH_BONUS
            else:
                return 0.0
        except (ZeroDivisionError, TypeError):
            return 0.0
    
    def _calculate_role_bonus(self, row):
        """Calculate role-specific bonuses"""
        if pd.isna(row['role']):
            return 0.0
        
        if row['role'] == 'Manager':
            return self._calculate_manager_bonus(row)
        else:
            # Sales reps - no additional role bonus
            return 0.0
    
    def _calculate_manager_bonus(self, row):
        """
        Calculate manager bonus based on team performance
        Base: 3% + team performance multiplier
        """
        try:
            team_size = row.get('team_size', 1)
            team_perf = row.get('team_performance', 1.0)
            
            if team_size < 3:
                base_manager_bonus = 0.03
            else:
                # Scale with team size
                base_manager_bonus = 0.03 + (min(team_size - 3, 12) * 0.005)
            
            # Apply team performance multiplier
            total_manager_bonus = base_manager_bonus * team_perf
            
            # Cap at 15%
            return min(total_manager_bonus, 0.15)
        except (TypeError, AttributeError):
            return 0.03  # Minimum manager bonus
    
    def get_incentive_summary(self, df):
        """
        Generate summary statistics for incentives
        
        Args:
            df (pd.DataFrame): Dataframe with incentive calculations
        
        Returns:
            dict: Summary statistics
        """
        return {
            'total_incentive_payout': df['incentive_payout'].sum(),
            'average_incentive_payout': df['incentive_payout'].mean(),
            'median_incentive_payout': df['incentive_payout'].median(),
            'max_incentive_payout': df['incentive_payout'].max(),
            'min_incentive_payout': df['incentive_payout'].min(),
            'std_dev_incentive': df['incentive_payout'].std(),
            'employees_at_target': (df['achievement_ratio'] >= 1.0).sum(),
            'employees_below_target': (df['achievement_ratio'] < 1.0).sum(),
            'employees_with_growth_bonus': (df['growth_bonus'] > 0).sum(),
            'total_growth_bonuses': df['growth_bonus'].sum(),
            'total_manager_bonuses': df[df['role'] == 'Manager']['role_bonus'].sum(),
        }
    
    def get_performance_tiers(self, df):
        """
        Categorize employees into performance tiers
        
        Args:
            df (pd.DataFrame): Dataframe with incentive calculations
        
        Returns:
            pd.DataFrame: Data with performance tier column
        """
        df = df.copy()
        
        def assign_tier(ratio):
            if ratio >= 1.5:
                return 'Exceeds Expectations'
            elif ratio >= 1.0:
                return 'Meets Target'
            elif ratio >= 0.8:
                return 'Partially Meets'
            else:
                return 'Below Target'
        
        df['performance_tier'] = df['achievement_ratio'].apply(assign_tier)
        return df

if __name__ == "__main__":
    from dataset_generator import DatasetGenerator
    
    generator = DatasetGenerator(num_records=100)
    df = generator.generate()
    
    engine = IncentiveEngine()
    df = engine.calculate_incentives(df)
    df = engine.get_performance_tiers(df)
    
    print("Sample Incentive Calculations:")
    print(df[['employee_name', 'role', 'sales_target', 'sales_amount', 
              'achievement_ratio', 'base_incentive', 'growth_bonus', 
              'role_bonus', 'incentive_payout']].head(10))
    
    print("\n" + "="*60)
    print("Incentive Summary:")
    summary = engine.get_incentive_summary(df)
    for key, value in summary.items():
        print(f"{key}: ${value:,.2f}" if 'payout' in key else f"{key}: {value:,.2f}")
