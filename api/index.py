"""
Vercel Serverless Function Handler
Route all API requests through this handler
"""

import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from http.server import BaseHTTPRequestHandler
from dataset_generator import DatasetGenerator
from incentive_engine import IncentiveEngine
from validation import DataValidator
from anomaly_detection import AnomalyDetector
import traceback

class handler(BaseHTTPRequestHandler):
    """Vercel Serverless Function Handler"""
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'status': 'healthy',
                'service': 'Enterprise Incentive Intelligence System',
                'version': '1.0.0'
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """Handle POST requests"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body) if body else {}
            
            response = None
            
            if self.path == '/api/dataset/generate':
                response = self.generate_dataset(data)
            elif self.path == '/api/incentives/calculate':
                response = self.calculate_incentives(data)
            elif self.path == '/api/validation/check':
                response = self.validate_data(data)
            elif self.path == '/api/anomalies/detect':
                response = self.detect_anomalies(data)
            elif self.path == '/api/analytics/summary':
                response = self.analytics_summary(data)
            else:
                response = {'error': 'Endpoint not found'}, 404
            
            status_code = response[1] if len(response) > 1 else 200
            response_data = response[0]
            
            self.send_response(status_code)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(response_data).encode())
        
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {
                'status': 'error',
                'message': str(e),
                'traceback': traceback.format_exc()
            }
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def generate_dataset(self, data):
        """Generate synthetic dataset"""
        try:
            num_records = data.get('num_records', 750)
            gen = DatasetGenerator(num_records=num_records, seed=42)
            df = gen.generate()
            
            return {
                'status': 'success',
                'records_generated': len(df),
                'columns': list(df.columns)
            }, 200
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 400
    
    def calculate_incentives(self, data):
        """Calculate incentives"""
        try:
            num_records = data.get('num_records', 100)
            gen = DatasetGenerator(num_records=num_records, seed=42)
            df = gen.generate()
            
            engine = IncentiveEngine()
            df = engine.calculate_incentives(df)
            df = engine.get_performance_tiers(df)
            
            summary = engine.get_incentive_summary(df)
            
            return {
                'status': 'success',
                'summary': {k: float(v) if isinstance(v, (int, float)) else int(v) 
                           for k, v in summary.items()},
                'total_records': len(df)
            }, 200
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 400
    
    def validate_data(self, data):
        """Validate data"""
        try:
            num_records = data.get('num_records', 100)
            gen = DatasetGenerator(num_records=num_records, seed=42)
            df = gen.generate()
            
            if data.get('add_anomalies'):
                df = DatasetGenerator.add_anomalies(df, anomaly_percentage=3)
            
            validator = DataValidator()
            is_valid, report = validator.validate(df)
            
            return {
                'status': 'success',
                'is_valid': is_valid,
                'errors': report['errors'],
                'warnings': report['warnings']
            }, 200
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 400
    
    def detect_anomalies(self, data):
        """Detect anomalies"""
        try:
            num_records = data.get('num_records', 100)
            gen = DatasetGenerator(num_records=num_records, seed=42)
            df = gen.generate()
            df = DatasetGenerator.add_anomalies(df, anomaly_percentage=3)
            
            engine = IncentiveEngine()
            df = engine.calculate_incentives(df)
            
            detector = AnomalyDetector()
            df = detector.detect_all(df)
            report = detector.get_anomaly_report(df)
            
            return {
                'status': 'success',
                'total_anomalies': int(report['total_anomalies']),
                'anomaly_percentage': float(report['anomaly_percentage']),
                'anomaly_types': report.get('anomaly_types', {})
            }, 200
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 400
    
    def analytics_summary(self, data):
        """Analytics summary"""
        try:
            gen = DatasetGenerator(num_records=100, seed=42)
            df = gen.generate()
            
            engine = IncentiveEngine()
            df = engine.calculate_incentives(df)
            
            return {
                'status': 'success',
                'total_records': len(df),
                'total_sales': float(df['sales_amount'].sum()),
                'total_incentive': float(df['incentive_payout'].sum())
            }, 200
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 400
