#!/bin/bash
# Pre-deployment setup script for Vercel

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

# Build Next.js
echo "✓ Building Next.js..."
npm run build

echo "✅ Setup complete! Ready for deployment."
echo ""
echo "To deploy to Vercel:"
echo "  1. Push to GitHub: git push origin main"
echo "  2. Go to https://vercel.com/new"
echo "  3. Import your repository"
echo "  4. Configure environment variables"
echo "  5. Click 'Deploy'"
echo ""
echo "For local testing:"
echo "  npm run dev"
echo ""
echo "Learn more: See VERCEL_DEPLOYMENT.md"
