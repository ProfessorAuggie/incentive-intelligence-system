#!/usr/bin/env bash

set -euo pipefail

if ! command -v vercel >/dev/null 2>&1; then
	echo "Vercel CLI is not installed. Install it first with: npm i -g vercel"
	exit 1
fi

if ! vercel env ls >/dev/null 2>&1; then
	echo "This project is not linked or you are not logged in. Run 'vercel login' and 'vercel link' first."
	exit 1
fi

add_env() {
	local name="$1"
	local value="$2"
	printf '%s' "$value" | vercel env add "$name" production >/dev/null
	echo "Added $name"
}

add_env NEXT_PUBLIC_API_URL https://enterprise-incentive-intelligence-s.vercel.app/api
add_env DATABASE_URL sqlite:///data/incentive_system.db
add_env API_PORT 3000
add_env API_TIMEOUT 30000
add_env API_RESPONSE_LIMIT 50mb
add_env NODE_ENV production
add_env PYTHON_PATH /usr/bin/python3
add_env PYTHON_VERSION 3.9
add_env JWT_SECRET super-secret-jwt-key-change-this-production-12345
add_env API_KEY super-secret-api-key-change-this-production-67890
add_env SECRET_KEY super-secret-key-change-this-production-11111
add_env CORS_ORIGIN https://enterprise-incentive-intelligence-s.vercel.app
add_env ALLOWED_ORIGINS enterprise-incentive-intelligence-s.vercel.app
add_env ENABLE_ANALYTICS true
add_env ENABLE_EXPORT true
add_env ENABLE_ANOMALY_DETECTION true
add_env ENABLE_DATA_VALIDATION true
add_env ENABLE_CACHING true
add_env ENABLE_COMPRESSION true
add_env LOG_LEVEL info
add_env LOG_FORMAT json
add_env ENABLE_REQUEST_LOGGING true
add_env ENABLE_ERROR_LOGGING true
add_env CACHE_ENABLED true
add_env CACHE_TTL 3600
add_env CACHE_MAX_SIZE 1000
add_env DATABASE_POOL_SIZE 5
add_env DATABASE_POOL_RECYCLE 3600
add_env RATE_LIMIT_ENABLED true
add_env RATE_LIMIT_REQUESTS 100
add_env RATE_LIMIT_WINDOW 60000
add_env DEFAULT_DATASET_SIZE 750
add_env MAX_DATASET_SIZE 10000
add_env ANOMOLY_THRESHOLD 3.0
add_env ANOMOLY_PERCENTAGE 3
add_env BATCH_SIZE 100
add_env EMAIL_NOTIFICATIONS_ENABLED false
add_env DEBUG_MODE false
add_env HOT_RELOAD false
add_env STRICT_MODE true
add_env EXPOSE_ERROR_DETAILS false

echo "All production environment variables were added to Vercel."
