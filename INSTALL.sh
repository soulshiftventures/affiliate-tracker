#!/bin/bash
# Affiliate Swarm - One-Click Install
# Makes setup TBI-friendly (copy/paste commands)

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  AFFILIATE SWARM - ONE-CLICK INSTALL                         ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Install from python.org"
    exit 1
fi

echo "✅ Python 3 found"

# Install Python dependencies
echo ""
echo "📦 Installing Python packages..."
pip3 install -r requirements.txt

# Install Playwright browsers
echo ""
echo "🌐 Installing Playwright browsers..."
playwright install chromium

# Install TikTok uploader
echo ""
echo "📱 Installing TikTok uploader..."
pip3 install tiktok-uploader

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  INSTALLATION COMPLETE!                                      ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "🎯 Next steps:"
echo ""
echo "1. Set up TikTok cookies:"
echo "   tiktok-uploader --setup"
echo ""
echo "2. Add your Claude API key:"
echo "   export ANTHROPIC_API_KEY='your_key_here'"
echo ""
echo "3. Edit credentials in auto_poster.py:"
echo "   - Reddit (line 45-50)"
echo "   - Medium (line 123)"
echo ""
echo "4. Start the system:"
echo "   python3 run.py --budget 100"
echo ""
echo "5. Open dashboard:"
echo "   http://localhost:8080"
echo ""
echo "💰 Ready to print money!"
