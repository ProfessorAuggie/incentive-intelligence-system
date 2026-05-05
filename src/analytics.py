"""
Analytics Module
Generates analytics and visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

class Analytics:
    """Provides analytics and visualization for incentive data"""
    
    def __init__(self, output_dir='reports'):
        """
        Initialize analytics module
        
        Args:
            output_dir (str): Directory for saving charts
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (14, 8)
    
    def analyze_region_performance(self, df):
        """Analyze sales and incentives by region"""
        region_stats = df.groupby('region').agg({
            'sales_amount': ['sum', 'mean'],
            'sales_target': ['sum', 'mean'],
            'incentive_payout': ['sum', 'mean'],
            'employee_id': 'count'
        }).round(2)
        
        region_stats.columns = ['Total Sales', 'Avg Sales', 'Total Target', 'Avg Target',
                               'Total Incentive', 'Avg Incentive', 'Employee Count']
        return region_stats
    
    def visualize_region_sales(self, df, save=True):
        """Create bar chart of sales by region"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        region_sales = df.groupby('region')['sales_amount'].sum().sort_values(ascending=False)
        colors = sns.color_palette("husl", len(region_sales))
        
        bars = ax.bar(region_sales.index, region_sales.values, color=colors, alpha=0.7, edgecolor='black')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'${height:,.0f}',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax.set_xlabel('Region', fontsize=12, fontweight='bold')
        ax.set_ylabel('Total Sales ($)', fontsize=12, fontweight='bold')
        ax.set_title('Total Sales by Region', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        if save:
            filepath = f'{self.output_dir}/region_sales.png'
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"✓ Saved chart: {filepath}")
        
        return fig
    
    def visualize_incentive_distribution(self, df, save=True):
        """Create histogram of incentive distribution"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        incentives = df['incentive_payout'].dropna()
        
        ax.hist(incentives, bins=50, color='steelblue', alpha=0.7, edgecolor='black')
        
        # Add mean and median lines
        mean_val = incentives.mean()
        median_val = incentives.median()
        
        ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: ${mean_val:,.0f}')
        ax.axvline(median_val, color='green', linestyle='--', linewidth=2, label=f'Median: ${median_val:,.0f}')
        
        ax.set_xlabel('Incentive Payout ($)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
        ax.set_title('Distribution of Incentive Payouts', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        plt.tight_layout()
        
        if save:
            filepath = f'{self.output_dir}/incentive_distribution.png'
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"✓ Saved chart: {filepath}")
        
        return fig
    
    def visualize_performance_tiers(self, df, save=True):
        """Create pie chart of performance tiers"""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        if 'performance_tier' not in df.columns:
            print("Warning: performance_tier column not found")
            return fig
        
        tier_counts = df['performance_tier'].value_counts()
        colors = sns.color_palette("Set2", len(tier_counts))
        
        wedges, texts, autotexts = ax.pie(tier_counts.values, labels=tier_counts.index,
                                           autopct='%1.1f%%', colors=colors, startangle=90,
                                           textprops={'fontsize': 11, 'fontweight': 'bold'})
        
        ax.set_title('Employee Distribution by Performance Tier', fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        if save:
            filepath = f'{self.output_dir}/performance_tiers.png'
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"✓ Saved chart: {filepath}")
        
        return fig
    
    def visualize_role_comparison(self, df, save=True):
        """Compare sales and incentives by role"""
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Sales by role
        role_sales = df.groupby('role')['sales_amount'].mean().sort_values(ascending=False)
        axes[0].bar(role_sales.index, role_sales.values, color=['#1f77b4', '#ff7f0e'], alpha=0.7, edgecolor='black')
        axes[0].set_ylabel('Average Sales ($)', fontsize=11, fontweight='bold')
        axes[0].set_title('Average Sales by Role', fontsize=12, fontweight='bold')
        for i, v in enumerate(role_sales.values):
            axes[0].text(i, v, f'${v:,.0f}', ha='center', va='bottom', fontweight='bold')
        
        # Incentives by role
        role_incentives = df.groupby('role')['incentive_payout'].mean().sort_values(ascending=False)
        axes[1].bar(role_incentives.index, role_incentives.values, color=['#1f77b4', '#ff7f0e'], alpha=0.7, edgecolor='black')
        axes[1].set_ylabel('Average Incentive ($)', fontsize=11, fontweight='bold')
        axes[1].set_title('Average Incentive Payout by Role', fontsize=12, fontweight='bold')
        for i, v in enumerate(role_incentives.values):
            axes[1].text(i, v, f'${v:,.0f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        if save:
            filepath = f'{self.output_dir}/role_comparison.png'
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"✓ Saved chart: {filepath}")
        
        return fig
    
    def visualize_sales_vs_target(self, df, save=True):
        """Scatter plot of sales vs target"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Create color map for roles
        colors = {'Sales': '#1f77b4', 'Manager': '#ff7f0e'}
        role_colors = df['role'].map(colors)
        
        ax.scatter(df['sales_target'], df['sales_amount'], c=role_colors, alpha=0.6, s=100, edgecolor='black')
        
        # Add diagonal line (target = sales)
        max_val = max(df['sales_target'].max(), df['sales_amount'].max())
        ax.plot([0, max_val], [0, max_val], 'r--', linewidth=2, alpha=0.7, label='Target = Sales')
        
        ax.set_xlabel('Sales Target ($)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Sales Amount ($)', fontsize=12, fontweight='bold')
        ax.set_title('Sales Amount vs Target', fontsize=14, fontweight='bold')
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor='#1f77b4', label='Sales'),
                          Patch(facecolor='#ff7f0e', label='Manager'),
                          plt.Line2D([0], [0], color='r', linestyle='--', linewidth=2, label='Target = Sales')]
        ax.legend(handles=legend_elements, fontsize=10)
        
        plt.tight_layout()
        
        if save:
            filepath = f'{self.output_dir}/sales_vs_target.png'
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"✓ Saved chart: {filepath}")
        
        return fig
    
    def visualize_growth_analysis(self, df, save=True):
        """Analyze and visualize growth trends"""
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Growth rate distribution
        df_copy = df[df['previous_quarter_sales'] > 0].copy()
        df_copy['growth_rate'] = (df_copy['sales_amount'] - df_copy['previous_quarter_sales']) / df_copy['previous_quarter_sales']
        
        axes[0].hist(df_copy['growth_rate'], bins=50, color='seagreen', alpha=0.7, edgecolor='black')
        axes[0].axvline(0, color='red', linestyle='--', linewidth=2, label='Zero Growth')
        axes[0].set_xlabel('Growth Rate', fontsize=11, fontweight='bold')
        axes[0].set_ylabel('Frequency', fontsize=11, fontweight='bold')
        axes[0].set_title('Quarter-over-Quarter Growth Distribution', fontsize=12, fontweight='bold')
        axes[0].legend()
        
        # Growth bonus recipients
        growth_bonus_by_role = df.groupby('role')['growth_bonus'].sum()
        axes[1].bar(growth_bonus_by_role.index, growth_bonus_by_role.values, color=['#2ca02c', '#d62728'], alpha=0.7, edgecolor='black')
        axes[1].set_ylabel('Total Growth Bonus ($)', fontsize=11, fontweight='bold')
        axes[1].set_title('Total Growth Bonus by Role', fontsize=12, fontweight='bold')
        for i, v in enumerate(growth_bonus_by_role.values):
            axes[1].text(i, v, f'${v:,.0f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        if save:
            filepath = f'{self.output_dir}/growth_analysis.png'
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"✓ Saved chart: {filepath}")
        
        return fig
    
    def generate_all_charts(self, df):
        """Generate all available charts"""
        print("\n" + "="*70)
        print("GENERATING ANALYTICS CHARTS")
        print("="*70)
        
        self.visualize_region_sales(df)
        self.visualize_incentive_distribution(df)
        self.visualize_performance_tiers(df)
        self.visualize_role_comparison(df)
        self.visualize_sales_vs_target(df)
        self.visualize_growth_analysis(df)
        
        print("="*70 + "\n")

if __name__ == "__main__":
    from dataset_generator import DatasetGenerator
    from incentive_engine import IncentiveEngine
    
    generator = DatasetGenerator(num_records=100)
    df = generator.generate()
    
    engine = IncentiveEngine()
    df = engine.calculate_incentives(df)
    df = engine.get_performance_tiers(df)
    
    analytics = Analytics()
    
    print("\nREGION PERFORMANCE ANALYSIS:")
    print(analytics.analyze_region_performance(df))
    
    analytics.generate_all_charts(df)
