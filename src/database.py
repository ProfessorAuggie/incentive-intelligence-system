"""
Database Module
Handles all database operations using SQLite/PostgreSQL
"""

import sqlite3
import pandas as pd
from sqlalchemy import create_engine, Column, String, Float, Integer, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

class DatabaseManager:
    """Manages database operations for incentive data"""
    
    def __init__(self, db_path='data/incentive_system.db', use_sqlite=True):
        """
        Initialize database manager
        
        Args:
            db_path (str): Path to SQLite database file
            use_sqlite (bool): Use SQLite if True, PostgreSQL otherwise
        """
        self.db_path = db_path
        self.use_sqlite = use_sqlite
        
        if use_sqlite:
            os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else '.', exist_ok=True)
            self.engine = create_engine(f'sqlite:///{db_path}')
        else:
            # PostgreSQL connection (configure as needed)
            # self.engine = create_engine('postgresql://user:password@localhost/dbname')
            raise NotImplementedError("PostgreSQL support not yet configured")
        
        self.Session = sessionmaker(bind=self.engine)
    
    def create_tables(self):
        """Create required database tables"""
        Base.metadata.create_all(self.engine)
        
        # Create tables using SQL if not exist
        with self.engine.connect() as conn:
            # Employees table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    employee_id TEXT PRIMARY KEY,
                    employee_name TEXT NOT NULL,
                    region TEXT,
                    role TEXT,
                    team_size INTEGER DEFAULT 1,
                    team_performance FLOAT DEFAULT 1.0
                )
            """)
            
            # Sales data table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sales_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id TEXT NOT NULL,
                    quarter TEXT NOT NULL,
                    sales_target FLOAT NOT NULL,
                    sales_amount FLOAT NOT NULL,
                    previous_quarter_sales FLOAT,
                    achievement_ratio FLOAT,
                    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
                )
            """)
            
            # Incentives table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS incentives (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id TEXT NOT NULL,
                    quarter TEXT NOT NULL,
                    base_incentive FLOAT,
                    growth_bonus FLOAT,
                    role_bonus FLOAT,
                    total_incentive FLOAT,
                    incentive_payout FLOAT,
                    performance_tier TEXT,
                    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
                )
            """)
            
            # Anomalies table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS anomalies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id TEXT NOT NULL,
                    quarter TEXT,
                    anomaly_type TEXT,
                    severity TEXT,
                    description TEXT,
                    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
                )
            """)
            
            conn.commit()
    
    def insert_data(self, df, table_name='employees'):
        """
        Insert data into table
        
        Args:
            df (pd.DataFrame): Data to insert
            table_name (str): Target table name
        """
        try:
            df.to_sql(table_name, self.engine, if_exists='replace', index=False)
            print(f"✓ Inserted {len(df)} records into {table_name} table")
            return True
        except Exception as e:
            print(f"✗ Error inserting into {table_name}: {e}")
            return False
    
    def insert_employees(self, df):
        """Insert employee data"""
        employees = df[['employee_id', 'employee_name', 'region', 'role', 
                       'team_size', 'team_performance']].drop_duplicates(subset=['employee_id'])
        self.insert_data(employees, 'employees')
    
    def insert_sales_data(self, df):
        """Insert sales data"""
        sales = df[['employee_id', 'quarter', 'sales_target', 'sales_amount', 
                   'previous_quarter_sales', 'achievement_ratio']]
        self.insert_data(sales, 'sales_data')
    
    def insert_incentives(self, df):
        """Insert incentive calculations"""
        incentives = df[['employee_id', 'quarter', 'base_incentive', 'growth_bonus',
                        'role_bonus', 'total_incentive', 'incentive_payout', 'performance_tier']]
        self.insert_data(incentives, 'incentives')
    
    def insert_anomalies(self, df):
        """Insert detected anomalies"""
        anomalous = df[df['is_anomaly']].copy()
        anomalies = anomalous[['employee_id', 'quarter', 'anomaly_flags']].copy()
        anomalies.rename(columns={'anomaly_flags': 'anomaly_type'}, inplace=True)
        anomalies['severity'] = 'high'
        anomalies['description'] = anomalies['anomaly_type']
        
        if len(anomalies) > 0:
            self.insert_data(anomalies[['employee_id', 'quarter', 'anomaly_type', 
                                        'severity', 'description']], 'anomalies')
    
    def query_top_performers(self, limit=10, quarter=None):
        """
        Query top performers by incentive payout
        
        Args:
            limit (int): Number of top performers to return
            quarter (str): Filter by quarter (optional)
        
        Returns:
            pd.DataFrame: Top performers
        """
        query = """
            SELECT e.employee_id, e.employee_name, e.region, e.role,
                   i.quarter, i.incentive_payout, i.performance_tier,
                   s.sales_amount, s.sales_target
            FROM incentives i
            JOIN employees e ON i.employee_id = e.employee_id
            JOIN sales_data s ON i.employee_id = s.employee_id AND i.quarter = s.quarter
        """
        
        if quarter:
            query += f" WHERE i.quarter = '{quarter}'"
        
        query += f" ORDER BY i.incentive_payout DESC LIMIT {limit}"
        
        return pd.read_sql_query(query, self.engine)
    
    def query_region_summary(self, quarter=None):
        """
        Get region-wise summary
        
        Args:
            quarter (str): Filter by quarter (optional)
        
        Returns:
            pd.DataFrame: Region summary
        """
        query = """
            SELECT e.region,
                   COUNT(DISTINCT e.employee_id) as employee_count,
                   SUM(s.sales_amount) as total_sales,
                   SUM(s.sales_target) as total_target,
                   AVG(i.incentive_payout) as avg_incentive,
                   SUM(i.incentive_payout) as total_payout
            FROM employees e
            JOIN sales_data s ON e.employee_id = s.employee_id
            JOIN incentives i ON e.employee_id = i.employee_id AND s.quarter = i.quarter
        """
        
        if quarter:
            query += f" WHERE s.quarter = '{quarter}'"
        
        query += " GROUP BY e.region ORDER BY total_payout DESC"
        
        return pd.read_sql_query(query, self.engine)
    
    def query_role_analysis(self, quarter=None):
        """
        Analyze performance by role
        
        Args:
            quarter (str): Filter by quarter (optional)
        
        Returns:
            pd.DataFrame: Role analysis
        """
        query = """
            SELECT e.role,
                   COUNT(DISTINCT e.employee_id) as employee_count,
                   AVG(s.sales_amount) as avg_sales,
                   SUM(i.incentive_payout) as total_payout,
                   AVG(i.incentive_payout) as avg_payout
            FROM employees e
            JOIN sales_data s ON e.employee_id = s.employee_id
            JOIN incentives i ON e.employee_id = i.employee_id AND s.quarter = i.quarter
        """
        
        if quarter:
            query += f" WHERE s.quarter = '{quarter}'"
        
        query += " GROUP BY e.role"
        
        return pd.read_sql_query(query, self.engine)
    
    def query_anomalies_summary(self):
        """Get summary of detected anomalies"""
        query = """
            SELECT anomaly_type, COUNT(*) as count, severity
            FROM anomalies
            GROUP BY anomaly_type, severity
            ORDER BY count DESC
        """
        
        try:
            return pd.read_sql_query(query, self.engine)
        except Exception as e:
            print(f"Error querying anomalies: {e}")
            return pd.DataFrame()
    
    def query_all_data(self):
        """Get complete dataset with all tables joined"""
        query = """
            SELECT e.employee_id, e.employee_name, e.region, e.role,
                   s.quarter, s.sales_target, s.sales_amount, s.previous_quarter_sales,
                   i.base_incentive, i.growth_bonus, i.role_bonus, i.total_incentive,
                   i.incentive_payout, i.performance_tier
            FROM employees e
            LEFT JOIN sales_data s ON e.employee_id = s.employee_id
            LEFT JOIN incentives i ON e.employee_id = i.employee_id AND s.quarter = i.quarter
        """
        
        return pd.read_sql_query(query, self.engine)
    
    def export_to_csv(self, query_result, filename):
        """
        Export query result to CSV
        
        Args:
            query_result (pd.DataFrame): Data to export
            filename (str): Output filename
        """
        os.makedirs('reports', exist_ok=True)
        filepath = f'reports/{filename}'
        query_result.to_csv(filepath, index=False)
        print(f"✓ Exported to {filepath}")
        return filepath

if __name__ == "__main__":
    from dataset_generator import DatasetGenerator
    from incentive_engine import IncentiveEngine
    from anomaly_detection import AnomalyDetector
    
    # Setup
    generator = DatasetGenerator(num_records=100)
    df = generator.generate()
    
    engine = IncentiveEngine()
    df = engine.calculate_incentives(df)
    df = engine.get_performance_tiers(df)
    
    detector = AnomalyDetector()
    df = detector.detect_all(df)
    
    # Database operations
    db = DatabaseManager()
    db.create_tables()
    db.insert_employees(df)
    db.insert_sales_data(df)
    db.insert_incentives(df)
    db.insert_anomalies(df)
    
    print("\n" + "="*70)
    print("TOP PERFORMERS")
    print("="*70)
    print(db.query_top_performers(limit=5))
    
    print("\n" + "="*70)
    print("REGION SUMMARY")
    print("="*70)
    print(db.query_region_summary())
    
    print("\n" + "="*70)
    print("ROLE ANALYSIS")
    print("="*70)
    print(db.query_role_analysis())
