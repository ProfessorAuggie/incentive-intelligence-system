import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import axios from 'axios';

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState('overview');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3000/api';

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_URL}/analytics/summary`);
      setData(response.data);
      setError(null);
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  };

  const handleCalculateIncentives = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/incentives/calculate`, {
        num_records: 500
      });
      setData(response.data);
      setError(null);
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  };

  const handleDetectAnomalies = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/anomalies/detect`, {
        num_records: 300
      });
      setData(response.data);
      setError(null);
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="min-h-screen bg-gray-50"
    >
      <nav className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-indigo-600">💰 Incentive Intelligence</h1>
          <div className="space-x-4">
            <button
              onClick={() => setActiveTab('overview')}
              className={`px-4 py-2 rounded ${
                activeTab === 'overview'
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-200 text-gray-800'
              }`}
            >
              Overview
            </button>
            <button
              onClick={() => setActiveTab('analytics')}
              className={`px-4 py-2 rounded ${
                activeTab === 'analytics'
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-200 text-gray-800'
              }`}
            >
              Analytics
            </button>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            Error: {error}
          </div>
        )}

        {activeTab === 'overview' && (
          <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }}>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="bg-white rounded-lg shadow p-6">
                <div className="text-gray-500 text-sm font-semibold">Total Records</div>
                <div className="text-3xl font-bold text-indigo-600 mt-2">
                  {data?.total_records || '—'}
                </div>
              </div>
              <div className="bg-white rounded-lg shadow p-6">
                <div className="text-gray-500 text-sm font-semibold">Total Sales</div>
                <div className="text-3xl font-bold text-green-600 mt-2">
                  ${data?.total_sales?.toLocaleString('en-US', {
                    maximumFractionDigits: 0
                  }) || '—'}
                </div>
              </div>
              <div className="bg-white rounded-lg shadow p-6">
                <div className="text-gray-500 text-sm font-semibold">Total Incentive</div>
                <div className="text-3xl font-bold text-blue-600 mt-2">
                  ${data?.total_incentive?.toLocaleString('en-US', {
                    maximumFractionDigits: 0
                  }) || '—'}
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <motion.button
                whileHover={{ scale: 1.05 }}
                onClick={handleCalculateIncentives}
                disabled={loading}
                className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-4 px-6 rounded-lg disabled:opacity-50"
              >
                {loading ? 'Processing...' : '📊 Calculate Incentives'}
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                onClick={handleDetectAnomalies}
                disabled={loading}
                className="bg-red-600 hover:bg-red-700 text-white font-bold py-4 px-6 rounded-lg disabled:opacity-50"
              >
                {loading ? 'Processing...' : '🔍 Detect Anomalies'}
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                onClick={fetchData}
                disabled={loading}
                className="bg-green-600 hover:bg-green-700 text-white font-bold py-4 px-6 rounded-lg disabled:opacity-50"
              >
                {loading ? 'Refreshing...' : '🔄 Refresh Data'}
              </motion.button>
            </div>
          </motion.div>
        )}

        {activeTab === 'analytics' && (
          <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }}>
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Analytics Data</h2>
              <pre className="bg-gray-100 p-4 rounded overflow-auto text-sm">
                {JSON.stringify(data, null, 2)}
              </pre>
            </div>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
}
