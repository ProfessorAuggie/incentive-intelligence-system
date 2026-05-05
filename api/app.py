"""
Vercel Python Serverless Functions
API endpoints for the Enterprise Incentive Intelligence System
"""

import sys
import os
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from flask import Flask, request, jsonify
from flask_cors import CORS
from dataset_generator import DatasetGenerator
from incentive_engine import IncentiveEngine
from validation import DataValidator
from anomaly_detection import AnomalyDetector
from analytics import Analytics
import pandas as pd
import traceback

app = Flask(__name__)
CORS(app)

# Initialize components
generator = DatasetGenerator(num_records=750, seed=42)
engine = IncentiveEngine()
validator = DataValidator()
detector = AnomalyDetector()

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Enterprise Incentive Intelligence System API',
        'version': '1.0.0'
    }), 200

@app.route('/api/dataset/generate', methods=['POST'])
def generate_dataset():
    """Generate synthetic dataset"""
    try:
        data = request.json
        num_records = data.get('num_records', 750)
        
        gen = DatasetGenerator(num_records=num_records, seed=42)
        df = gen.generate()
        
        return jsonify({
            'status': 'success',
            'records_generated': len(df),
            'columns': list(df.columns)
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'traceback': traceback.format_exc()
        }), 400

@app.route('/api/incentives/calculate', methods=['POST'])
def calculate_incentives():
    """Calculate incentives for dataset"""
    try:
        data = request.json
        
        # Generate dataset
        gen = DatasetGenerator(num_records=data.get('num_records', 100), seed=42)
        df = gen.generate()
        
        # Calculate incentives
        engine_instance = IncentiveEngine()
        df = engine_instance.calculate_incentives(df)
        df = engine_instance.get_performance_tiers(df)
        
        summary = engine_instance.get_incentive_summary(df)
        
        # Convert to JSON-serializable format
        result = {
            'status': 'success',
            'summary': {k: float(v) if isinstance(v, (int, float)) else int(v) 
                       for k, v in summary.items()},
            'total_records': len(df),
            'top_earners': df.nlargest(5, 'incentive_payout')[[
                'employee_name', 'role', 'incentive_payout', 'performance_tier'
            ]].to_dict('records')
        }
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'traceback': traceback.format_exc()
        }), 400

@app.route('/api/validation/check', methods=['POST'])
def validate_data():
    """Validate dataset"""
    try:
        data = request.json
        
        # Generate dataset
        gen = DatasetGenerator(num_records=data.get('num_records', 100), seed=42)
        df = gen.generate()
        
        if data.get('add_anomalies'):
            df = DatasetGenerator.add_anomalies(df, anomaly_percentage=3)
        
        # Validate
        validator_instance = DataValidator()
        is_valid, report = validator_instance.validate(df)
        
        return jsonify({
            'status': 'success',
            'is_valid': is_valid,
            'errors': report['errors'],
            'warnings': report['warnings'],
            'error_count': report['error_count'],
            'warning_count': report['warning_count']
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'traceback': traceback.format_exc()
        }), 400

@app.route('/api/anomalies/detect', methods=['POST'])
def detect_anomalies():
    """Detect anomalies in dataset"""
    try:
        data = request.json
        
        # Generate dataset
        gen = DatasetGenerator(num_records=data.get('num_records', 100), seed=42)
        df = gen.generate()
        df = DatasetGenerator.add_anomalies(df, anomaly_percentage=3)
        
        # Calculate incentives
        engine_instance = IncentiveEngine()
        df = engine_instance.calculate_incentives(df)
        
        # Detect anomalies
        detector_instance = AnomalyDetector()
        df = detector_instance.detect_all(df)
        report = detector_instance.get_anomaly_report(df)
        
        anomalies_data = report['anomalous_records'][[
            'employee_name', 'role', 'sales_amount', 'incentive_payout', 'anomaly_flags'
        ]].head(20).to_dict('records')
        
        return jsonify({
            'status': 'success',
            'total_anomalies': int(report['total_anomalies']),
            'anomaly_percentage': float(report['anomaly_percentage']),
            'anomaly_types': report.get('anomaly_types', {}),
            'anomalous_records': anomalies_data
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'traceback': traceback.format_exc()
        }), 400

@app.route('/api/analytics/summary', methods=['GET'])
def analytics_summary():
    """Get analytics summary"""
    try:
        # Generate dataset
        gen = DatasetGenerator(num_records=100, seed=42)
        df = gen.generate()
        
        # Calculate incentives
        engine_instance = IncentiveEngine()
        df = engine_instance.calculate_incentives(df)
        
        # Regional analysis
        analytics_instance = Analytics()
        region_stats = analytics_instance.analyze_region_performance(df)
        
        return jsonify({
            'status': 'success',
            'region_summary': region_stats.to_dict(),
            'total_records': len(df),
            'total_sales': float(df['sales_amount'].sum()),
            'total_incentive': float(df['incentive_payout'].sum())
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'traceback': traceback.format_exc()
        }), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
