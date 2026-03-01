#!/bin/bash

echo "======================================"
echo "DEPLOYING AFFILIATE SWARM"
echo "======================================"
echo ""

# Check if we're in the right directory
if [ ! -f "tracker.py" ]; then
    echo "❌ Error: Run this from affiliate_swarm directory"
    exit 1
fi

echo "📦 Step 1: Creating GitHub repo..."
git init
git add .
git commit -m "affiliate swarm - automated deployment"

# Create repo using gh CLI
gh repo create affiliate-swarm --public --source=. --remote=origin --push

echo ""
echo "✅ GitHub repo created: https://github.com/$(gh api user -q .login)/affiliate-swarm"
echo ""

echo "======================================"
echo "NEXT: Deploy to Render"
echo "======================================"
echo ""
echo "1. Go to: https://dashboard.render.com"
echo "2. Click 'New +' → 'Web Service'"
echo "3. Click 'Connect GitHub'"
echo "4. Select 'affiliate-swarm' repo"
echo "5. Settings:"
echo "   Name: affiliate-tracker"
echo "   Build Command: pip install -r requirements.txt"
echo "   Start Command: python3 tracker.py"
echo "   Instance Type: Free"
echo ""
echo "6. Click 'Create Web Service'"
echo ""
echo "Render will give you a URL like:"
echo "https://affiliate-tracker.onrender.com"
echo ""
echo "======================================"
echo "YOUR TRACKING URLS WILL BE:"
echo "======================================"
echo ""
echo "https://affiliate-tracker.onrender.com/track/click/offer_coaching"
echo "https://affiliate-tracker.onrender.com/track/click/offer_high_ticket_course"
echo "https://affiliate-tracker.onrender.com/track/click/offer_software_tool"
echo ""
echo "Use these in Udimi orders."
echo ""
echo "======================================"
echo "DONE - 5 MINUTES TO DEPLOYMENT"
echo "======================================"
