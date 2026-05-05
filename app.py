"""
Streamlit Dashboard
Interactive web-based dashboard for the Enterprise Incentive Intelligence System
"""

import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from dataset_generator import DatasetGenerator
from incentive_engine import IncentiveEngine
from validation import DataValidator
from anomaly_detection import AnomalyDetector
from database import DatabaseManager
from analytics import Analytics

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="Incentive Intelligence System",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== STYLING ==========
st.markdown("""
<style>
    .main-header {
        font-size: 2.5em;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 10px;
    }
    .metric-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# ========== SIDEBAR CONFIGURATION ==========
st.sidebar.markdown("# ⚙️ Configuration")

with st.sidebar.expander("Dataset Generation", expanded=False):
    num_records = st.slider("Number of Records", 100, 2000, 750, step=50)
    generate_data = st.button("🔄 Generate New Dataset", key="gen_data")

with st.sidebar.expander("Filters", expanded=True):
    st.write("**Filter Options**")
    selected_region = st.selectbox("Region", ["All", "North America", "Europe", "Asia Pacific", "Latin America", "Middle East Africa"])
    selected_role = st.selectbox("Role", ["All", "Sales", "Manager"])
    min_incentive = st.slider("Minimum Incentive ($)", 0, 100000, 0, step=10000)

# ========== LOAD/GENERATE DATA ==========
@st.cache_resource
def load_data(num_records=750):
    """Load or generate dataset"""
    try:
        # Try to load from database
        db = DatabaseManager()
        df = db.query_all_data()
        if len(df) > 0:
            return df
    except:
        pass
    
    # Generate new data if not in database
    generator = DatasetGenerator(num_records=num_records, seed=42)
    df = generator.generate()
    df = DatasetGenerator.add_anomalies(df, anomaly_percentage=3)
    
    engine = IncentiveEngine()
    df = engine.calculate_incentives(df)
    df = engine.get_performance_tiers(df)
    
    detector = AnomalyDetector()
    df = detector.detect_all(df)
    
    return df

# Load data
if generate_data:
    st.cache_resource.clear()

df = load_data(num_records)

# Apply filters
df_filtered = df.copy()

if selected_region != "All":
    df_filtered = df_filtered[df_filtered['region'] == selected_region]

if selected_role != "All":
    df_filtered = df_filtered[df_filtered['role'] == selected_role]

if min_incentive > 0:
    df_filtered = df_filtered[df_filtered['incentive_payout'] >= min_incentive]

# ========== MAIN PAGE ==========
st.markdown('<div class="main-header">💰 Enterprise Incentive Intelligence System</div>', unsafe_allow_html=True)

# Tabs for different sections
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Dashboard", "👥 Employees", "🔍 Anomalies", "📈 Analytics", "🏪 Regional", "⚙️ Admin"
])

# ========== TAB 1: DASHBOARD ==========
with tab1:
    st.subheader("Executive Dashboard")
    
    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Payout",
            f"${df_filtered['incentive_payout'].sum():,.0f}",
            f"{df_filtered['incentive_payout'].mean():.0f} avg"
        )
    
    with col2:
        at_target = (df_filtered['achievement_ratio'] >= 1.0).sum()
        st.metric(
            "At Target",
            f"{at_target}",
            f"{at_target/len(df_filtered)*100:.1f}% achievement"
        )
    
    with col3:
        anomalies = df_filtered['is_anomaly'].sum() if 'is_anomaly' in df_filtered.columns else 0
        st.metric(
            "Anomalies",
            f"{anomalies}",
            f"{anomalies/len(df_filtered)*100:.1f}% of records"
        )
    
    with col4:
        st.metric(
            "Employees",
            f"{len(df_filtered)}",
            f"{df_filtered['role'].value_counts().get('Manager', 0)} Managers"
        )
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Incentive Distribution")
        fig = px.histogram(df_filtered, x='incentive_payout', nbins=50, title="",
                          labels={'incentive_payout': 'Incentive Payout ($)'})
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Sales by Region")
        region_sales = df_filtered.groupby('region')['sales_amount'].sum().reset_index()
        fig = px.bar(region_sales, x='region', y='sales_amount', title="",
                    labels={'sales_amount': 'Total Sales ($)', 'region': 'Region'})
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Performance Tiers
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Performance Tiers")
        if 'performance_tier' in df_filtered.columns:
            tier_counts = df_filtered['performance_tier'].value_counts()
            fig = px.pie(values=tier_counts.values, names=tier_counts.index, title="")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Sales vs Target")
        fig = px.scatter(df_filtered, x='sales_target', y='sales_amount', 
                        color='role', title="",
                        labels={'sales_target': 'Sales Target ($)', 'sales_amount': 'Sales Amount ($)'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

# ========== TAB 2: EMPLOYEES ==========
with tab2:
    st.subheader("Employee Performance Details")
    
    # Top Performers
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("**Top 10 Performers by Incentive Payout**")
        top_performers = df_filtered.nlargest(10, 'incentive_payout')[
            ['employee_name', 'role', 'region', 'sales_amount', 'incentive_payout', 'performance_tier']
        ].reset_index(drop=True)
        top_performers.index = top_performers.index + 1
        st.dataframe(top_performers, use_container_width=True)
    
    with col2:
        st.metric("Top Earner", f"${df_filtered['incentive_payout'].max():,.0f}")
    
    # Employee Search
    st.write("---")
    st.write("**Search Employee**")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        search_name = st.text_input("Enter employee name or ID")
    
    if search_name:
        search_results = df_filtered[
            (df_filtered['employee_name'].str.contains(search_name, case=False, na=False)) |
            (df_filtered['employee_id'].str.contains(search_name, case=False, na=False))
        ]
        
        if len(search_results) > 0:
            st.dataframe(search_results[[
                'employee_name', 'employee_id', 'role', 'region', 'sales_target', 
                'sales_amount', 'achievement_ratio', 'incentive_payout'
            ]], use_container_width=True)
        else:
            st.info("No matching employees found")

# ========== TAB 3: ANOMALIES ==========
with tab3:
    st.subheader("Anomaly Detection Results")
    
    # Anomaly Statistics
    if 'is_anomaly' in df_filtered.columns:
        anomaly_count = df_filtered['is_anomaly'].sum()
        anomaly_pct = anomaly_count / len(df_filtered) * 100
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Anomalies", anomaly_count)
        with col2:
            st.metric("Anomaly Rate", f"{anomaly_pct:.2f}%")
        with col3:
            st.metric("Normal Records", len(df_filtered) - anomaly_count)
        
        # Anomaly Types
        if 'anomaly_flags' in df_filtered.columns and anomaly_count > 0:
            st.write("---")
            st.write("**Anomaly Type Distribution**")
            
            anomaly_types = {}
            for flags in df_filtered[df_filtered['is_anomaly']]['anomaly_flags']:
                for flag in str(flags).split("; "):
                    if flag:
                        anomaly_types[flag] = anomaly_types.get(flag, 0) + 1
            
            if anomaly_types:
                anomaly_df = pd.DataFrame(
                    list(anomaly_types.items()),
                    columns=['Anomaly Type', 'Count']
                ).sort_values('Count', ascending=False)
                
                fig = px.bar(anomaly_df, x='Anomaly Type', y='Count', title="")
                st.plotly_chart(fig, use_container_width=True)
        
        # Anomalous Records
        st.write("---")
        st.write("**Anomalous Records**")
        
        anomalous_records = df_filtered[df_filtered['is_anomaly']]
        if len(anomalous_records) > 0:
            display_cols = ['employee_name', 'role', 'region', 'sales_amount', 
                          'incentive_payout', 'anomaly_flags']
            st.dataframe(anomalous_records[display_cols], use_container_width=True)
        else:
            st.info("No anomalies detected in current filter")
    else:
        st.warning("Anomaly detection not yet performed")

# ========== TAB 4: ANALYTICS ==========
with tab4:
    st.subheader("Detailed Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Sales by Role**")
        role_sales = df_filtered.groupby('role')['sales_amount'].agg(['sum', 'mean']).reset_index()
        fig = px.bar(role_sales, x='role', y='sum', title="Total Sales",
                    labels={'sum': 'Total Sales ($)', 'role': 'Role'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.write("**Incentive by Role**")
        role_incentive = df_filtered.groupby('role')['incentive_payout'].agg(['sum', 'mean']).reset_index()
        fig = px.bar(role_incentive, x='role', y='sum', title="Total Incentive",
                    labels={'sum': 'Total Incentive ($)', 'role': 'Role'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Growth Analysis
    st.write("---")
    st.write("**Growth Metrics**")
    
    df_with_growth = df_filtered[df_filtered['previous_quarter_sales'] > 0].copy()
    df_with_growth['growth_rate'] = (
        (df_with_growth['sales_amount'] - df_with_growth['previous_quarter_sales']) / 
        df_with_growth['previous_quarter_sales']
    )
    
    col1, col2 = st.columns([2, 1])
    with col1:
        fig = px.histogram(df_with_growth, x='growth_rate', nbins=50, title="Growth Rate Distribution",
                          labels={'growth_rate': 'Growth Rate'})
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        growth_bonus_count = (df_filtered['growth_bonus'] > 0).sum()
        st.metric("Employees with Growth Bonus", growth_bonus_count)
        st.metric("Total Growth Bonus", f"${df_filtered['growth_bonus'].sum():,.0f}")

# ========== TAB 5: REGIONAL ==========
with tab5:
    st.subheader("Regional Performance Analysis")
    
    # Regional Summary
    regional_summary = df_filtered.groupby('region').agg({
        'employee_id': 'count',
        'sales_amount': ['sum', 'mean'],
        'incentive_payout': ['sum', 'mean']
    }).round(2)
    
    regional_summary.columns = ['Employees', 'Total Sales', 'Avg Sales', 'Total Incentive', 'Avg Incentive']
    
    st.dataframe(regional_summary, use_container_width=True)
    
    # Regional Charts
    col1, col2 = st.columns(2)
    
    with col1:
        regional_sales = df_filtered.groupby('region')['sales_amount'].sum().reset_index()
        fig = px.pie(regional_sales, values='sales_amount', names='region', title="Sales Distribution by Region")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        regional_incentive = df_filtered.groupby('region')['incentive_payout'].sum().reset_index()
        fig = px.pie(regional_incentive, values='incentive_payout', names='region', 
                    title="Incentive Distribution by Region")
        st.plotly_chart(fig, use_container_width=True)

# ========== TAB 6: ADMIN ==========
with tab6:
    st.subheader("Administration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Dataset Summary**")
        st.write(f"Total Records: {len(df)}")
        st.write(f"Filtered Records: {len(df_filtered)}")
        st.write(f"Columns: {len(df.columns)}")
        
        if st.button("Generate Dataset Report"):
            summary = {
                'Total Employees': len(df),
                'Total Sales': df['sales_amount'].sum(),
                'Total Payout': df['incentive_payout'].sum(),
                'Average Incentive': df['incentive_payout'].mean(),
                'Anomalies': df['is_anomaly'].sum() if 'is_anomaly' in df.columns else 0
            }
            st.json(summary)
    
    with col2:
        st.write("**Data Quality**")
        null_counts = df.isnull().sum()
        if null_counts.sum() > 0:
            st.write(null_counts[null_counts > 0])
        else:
            st.success("✓ No null values detected")
    
    # Export Options
    st.write("---")
    st.write("**Export Data**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv = df_filtered.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv,
            file_name=f"incentive_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # Excel export would need openpyxl
        st.info("💡 Excel export available via main.py batch processing")

# Footer
st.write("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 0.8em;'>
    Enterprise Incentive Intelligence System | Last Updated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """
    </div>
    """,
    unsafe_allow_html=True
)
