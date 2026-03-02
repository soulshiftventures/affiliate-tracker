# Deploy Affiliate Tracker to Render

## ⚡ One-Click Deploy (FASTEST)

Click this button to deploy in 60 seconds:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/soulshiftventures/affiliate-tracker)

This will:
1. Create a new Render service named "affiliate-tracker-live"
2. Install dependencies (flask, requests)
3. Start tracker.py on a public URL
4. Auto-deploy on every git push

**Your tracking URL will be:** `https://affiliate-tracker-live.onrender.com`

---

## 🔧 Manual Deploy (5 minutes)

If one-click doesn't work:

### Step 1: Open Render Dashboard
```
https://dashboard.render.com
```

### Step 2: Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Click **"Connect GitHub"** (if not connected)
3. Select repository: **soulshiftventures/affiliate-tracker**
4. Click **"Connect"**

### Step 3: Configure Service
```
Name:           affiliate-tracker-live
Branch:         main
Build Command:  pip install flask requests
Start Command:  python3 tracker.py
Instance Type:  Free
```

### Step 4: Create Service
Click **"Create Web Service"**

Render will:
- Build your app (~2 minutes)
- Deploy to a public URL
- Show you the URL when ready

---

## ✅ Verify Deployment

Once deployed, test these URLs:

### 1. Stats Endpoint
```bash
curl https://affiliate-tracker-live.onrender.com/api/stats
```

Expected response:
```json
{
  "total_clicks": 0,
  "total_conversions": 0,
  "total_revenue": 0,
  "total_cost": 0,
  "roi": 0,
  "conversion_rate": 0,
  "offers": {}
}
```

### 2. Test Click Tracking
```bash
curl -I https://affiliate-tracker-live.onrender.com/track/click/test_offer
```

Expected: 302 redirect to example.com

---

## 🎯 Use With Udimi

Your tracking URLs for Udimi traffic:

```
https://affiliate-tracker-live.onrender.com/track/click/offer_1
https://affiliate-tracker-live.onrender.com/track/click/offer_2
https://affiliate-tracker-live.onrender.com/track/click/offer_3
```

Replace `offer_1`, `offer_2`, etc. with your actual offer IDs.

### Register Offers First

Before buying traffic, register your offers:

```python
import requests

url = "https://affiliate-tracker-live.onrender.com/api/register_offer"
data = {
    "offer_id": "coaching_program",
    "name": "High Ticket Coaching",
    "url": "https://your-clickbank-hoplink.com",
    "payout": 500
}

requests.post(url, json=data)
```

Or manually add to `data/tracking/offers.json` in the deployed service.

---

## 🚨 Important Notes

### Free Tier Limitations
- Service spins down after 15 min inactivity
- First request after sleep takes ~30 seconds
- Data persists in `/data/tracking/` directory

### Keep Service Alive (Optional)
Use a cron job to ping every 10 minutes:

```bash
*/10 * * * * curl https://affiliate-tracker-live.onrender.com/api/stats > /dev/null 2>&1
```

Or use a service like [UptimeRobot](https://uptimerobot.com) (free).

---

## 🔄 Auto-Deploy Updates

Every `git push` to main branch will automatically redeploy.

To update:
```bash
cd ~/DeepDiveSystems/projects/affiliate_swarm
# Make changes
git add -A
git commit -m "update: your changes"
git push origin main
```

Render will rebuild and deploy automatically (~2 min).

---

## 📊 View Logs

Check service logs in Render dashboard:
1. Go to https://dashboard.render.com
2. Click on "affiliate-tracker-live" service
3. Click "Logs" tab

You'll see:
- All clicks tracked
- Conversions recorded
- Traffic sources
- Errors (if any)

---

## 🎉 Done!

Your affiliate tracker is now live and ready for Udimi traffic.

**Next steps:**
1. Register your ClickBank/JVZoo offers
2. Use tracking URLs in Udimi orders
3. Watch conversions in dashboard

**Dashboard:** Open `dashboard.html` locally and point it to your Render URL in the JavaScript fetch calls.

---

**Questions?** Check tracker.py logs in Render dashboard or test endpoints with curl.
