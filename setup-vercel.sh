#!/usr/bin/env bash
# Pre-deployment setup script for Vercel

set -euo pipefail

require_command() {
	local command_name="$1"

	if ! command -v "$command_name" >/dev/null 2>&1; then
		echo "Missing required command: $command_name"
		exit 1
	fi
}

add_vercel_envs() {
	require_command vercel

	if ! vercel env ls >/dev/null 2>&1; then
		echo "Vercel project is not linked or you are not logged in. Run 'vercel login' and 'vercel link' first."
		exit 1
	fi

	echo "✓ Adding production environment variables to Vercel..."

	while IFS='=' read -r name value; do
		if [[ -z "$name" ]]; then
			continue
		fi

		printf '%s' "$value" | vercel env add "$name" production >/dev/null
		echo "  - Added $name"
	done <<'EOF'
NEXT_PUBLIC_API_URL=https://enterprise-incentive-intelligence-s.vercel.app/api
DATABASE_URL=sqlite:///data/incentive_system.db
API_PORT=3000
API_TIMEOUT=30000
API_RESPONSE_LIMIT=50mb
NODE_ENV=production
PYTHON_PATH=/usr/bin/python3
PYTHON_VERSION=3.9
JWT_SECRET=super-secret-jwt-key-change-this-production-12345
API_KEY=super-secret-api-key-change-this-production-67890
SECRET_KEY=super-secret-key-change-this-production-11111
CORS_ORIGIN=https://enterprise-incentive-intelligence-s.vercel.app
ALLOWED_ORIGINS=enterprise-incentive-intelligence-s.vercel.app
ENABLE_ANALYTICS=true
ENABLE_EXPORT=true
ENABLE_ANOMALY_DETECTION=true
ENABLE_DATA_VALIDATION=true
ENABLE_CACHING=true
ENABLE_COMPRESSION=true
LOG_LEVEL=info
LOG_FORMAT=json
ENABLE_REQUEST_LOGGING=true
ENABLE_ERROR_LOGGING=true
CACHE_ENABLED=true
CACHE_TTL=3600
CACHE_MAX_SIZE=1000
DATABASE_POOL_SIZE=5
DATABASE_POOL_RECYCLE=3600
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60000
DEFAULT_DATASET_SIZE=750
MAX_DATASET_SIZE=10000
ANOMOLY_THRESHOLD=3.0
ANOMOLY_PERCENTAGE=3
BATCH_SIZE=100
EMAIL_NOTIFICATIONS_ENABLED=false
DEBUG_MODE=false
HOT_RELOAD=false
STRICT_MODE=true
EXPOSE_ERROR_DETAILS=false
EOF
}

echo "🚀 Setting up Enterprise Incentive Intelligence System for Vercel..."

# Check Node.js
echo "✓ Checking Node.js..."
node --version

# Check Python
echo "✓ Checking Python..."
python3 --version

# Create necessary directories
echo "✓ Creating directories..."
mkdir -p data
mkdir -p reports

# Install npm dependencies
echo "✓ Installing npm dependencies..."
npm install

# Install Python requirements
echo "✓ Installing Python requirements..."
pip install -r requirements.txt

# Configure Vercel production environment variables
add_vercel_envs

# Build Next.js
echo "✓ Building Next.js..."
npm run build

echo "✅ Setup complete! Ready for deployment."
echo ""
echo "To deploy to Vercel:"
echo "  1. Push to GitHub: git push origin main"
echo "  2. Go to https://vercel.com/new"
echo "  3. Import your repository"
echo "  4. Click 'Deploy'"
echo ""
echo "For local testing:"
echo "  npm run dev"
echo ""
echo "Learn more: See VERCEL_DEPLOYMENT.md"
