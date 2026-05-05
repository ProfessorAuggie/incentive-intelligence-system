import React from 'react';
import { motion } from 'framer-motion';

export default function Home() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center"
    >
      <div className="max-w-2xl w-full mx-auto px-4 py-12">
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2, duration: 0.5 }}
          className="bg-white rounded-lg shadow-2xl p-8"
        >
          <h1 className="text-4xl font-bold text-center text-gray-800 mb-4">
            💰 Enterprise Incentive Intelligence
          </h1>
          <p className="text-xl text-center text-gray-600 mb-8">
            Advanced Sales Performance & Incentive Management Platform
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <motion.a
              whileHover={{ scale: 1.05 }}
              href="/dashboard"
              className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-4 px-6 rounded-lg text-center transition duration-200"
            >
              📊 Dashboard
            </motion.a>
            <motion.a
              whileHover={{ scale: 1.05 }}
              href="/api/health"
              className="bg-green-600 hover:bg-green-700 text-white font-bold py-4 px-6 rounded-lg text-center transition duration-200"
            >
              ✓ API Status
            </motion.a>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center mb-8">
            <div className="p-4 bg-blue-50 rounded-lg">
              <div className="text-3xl font-bold text-blue-600">750+</div>
              <div className="text-sm text-gray-600">Records</div>
            </div>
            <div className="p-4 bg-green-50 rounded-lg">
              <div className="text-3xl font-bold text-green-600">5</div>
              <div className="text-sm text-gray-600">Regions</div>
            </div>
            <div className="p-4 bg-purple-50 rounded-lg">
              <div className="text-3xl font-bold text-purple-600">7</div>
              <div className="text-sm text-gray-600">Modules</div>
            </div>
          </div>

          <p className="text-center text-gray-600 text-sm">
            Features: Multi-tier incentive calculations, Data validation, Anomaly detection, 
            SQL analytics, Real-time dashboards, Comprehensive reporting
          </p>
        </motion.div>
      </div>
    </motion.div>
  );
}
