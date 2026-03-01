"""
Self-Hosted Tracking System (FREE - No ClickMagick needed)
Tracks clicks, conversions, and ROI in real-time
"""

from flask import Flask, request, redirect, jsonify, send_file
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import hashlib

# Tracking data storage
DATA_DIR = Path("data/tracking")
DATA_DIR.mkdir(parents=True, exist_ok=True)

CLICKS_FILE = DATA_DIR / "clicks.json"
CONVERSIONS_FILE = DATA_DIR / "conversions.json"
OFFERS_FILE = DATA_DIR / "offers.json"

app = Flask(__name__)

class Tracker:
    """Track clicks and conversions."""

    def __init__(self):
        self.clicks = self._load_json(CLICKS_FILE, [])
        self.conversions = self._load_json(CONVERSIONS_FILE, [])
        self.offers = self._load_json(OFFERS_FILE, {})

    def _load_json(self, filepath: Path, default):
        """Load JSON file or return default."""
        if filepath.exists():
            with open(filepath) as f:
                return json.load(f)
        return default

    def _save_json(self, filepath: Path, data):
        """Save data to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def register_offer(self, offer_id: str, offer_data: Dict):
        """Register an offer for tracking."""
        self.offers[offer_id] = {
            **offer_data,
            "clicks": 0,
            "conversions": 0,
            "revenue": 0,
            "cost": 0,
            "roi": 0
        }
        self._save_json(OFFERS_FILE, self.offers)

    def track_click(self, offer_id: str, source: str = "unknown") -> str:
        """Track a click and return tracking ID."""
        click_id = hashlib.md5(f"{offer_id}{time.time()}".encode()).hexdigest()[:12]

        click_data = {
            "click_id": click_id,
            "offer_id": offer_id,
            "source": source,
            "timestamp": datetime.now().isoformat(),
            "converted": False,
            "ip": request.remote_addr if request else "unknown",
            "user_agent": request.headers.get("User-Agent", "unknown") if request else "unknown"
        }

        self.clicks.append(click_data)
        self._save_json(CLICKS_FILE, self.clicks)

        # Update offer stats
        if offer_id in self.offers:
            self.offers[offer_id]["clicks"] += 1
            self._save_json(OFFERS_FILE, self.offers)

        return click_id

    def track_conversion(self, click_id: str, amount: float):
        """Track a conversion."""
        # Find click
        click = next((c for c in self.clicks if c["click_id"] == click_id), None)

        if not click:
            print(f"⚠️ Click ID {click_id} not found")
            return False

        # Mark click as converted
        click["converted"] = True
        self._save_json(CLICKS_FILE, self.clicks)

        # Record conversion
        conversion_data = {
            "click_id": click_id,
            "offer_id": click["offer_id"],
            "amount": amount,
            "timestamp": datetime.now().isoformat()
        }

        self.conversions.append(conversion_data)
        self._save_json(CONVERSIONS_FILE, self.conversions)

        # Update offer stats
        offer_id = click["offer_id"]
        if offer_id in self.offers:
            self.offers[offer_id]["conversions"] += 1
            self.offers[offer_id]["revenue"] += amount
            self._calculate_roi(offer_id)
            self._save_json(OFFERS_FILE, self.offers)

        print(f"✅ Conversion tracked: ${amount} from offer {offer_id}")
        return True

    def update_offer_cost(self, offer_id: str, cost: float):
        """Update traffic cost for an offer."""
        if offer_id in self.offers:
            self.offers[offer_id]["cost"] += cost
            self._calculate_roi(offer_id)
            self._save_json(OFFERS_FILE, self.offers)

    def _calculate_roi(self, offer_id: str):
        """Calculate ROI for an offer."""
        offer = self.offers[offer_id]
        if offer["cost"] > 0:
            offer["roi"] = ((offer["revenue"] - offer["cost"]) / offer["cost"]) * 100
        else:
            offer["roi"] = 0

    def get_stats(self) -> Dict:
        """Get overall statistics."""
        total_clicks = len(self.clicks)
        total_conversions = len(self.conversions)
        total_revenue = sum(c["amount"] for c in self.conversions)
        total_cost = sum(o["cost"] for o in self.offers.values())

        return {
            "total_clicks": total_clicks,
            "total_conversions": total_conversions,
            "total_revenue": total_revenue,
            "total_cost": total_cost,
            "roi": ((total_revenue - total_cost) / total_cost * 100) if total_cost > 0 else 0,
            "conversion_rate": (total_conversions / total_clicks * 100) if total_clicks > 0 else 0,
            "offers": self.offers
        }

    def get_winners(self, min_conversion_rate: float = 2.0) -> List[Dict]:
        """Get winning offers (>2% conversion rate)."""
        winners = []

        for offer_id, offer in self.offers.items():
            if offer["clicks"] < 20:  # Need minimum data
                continue

            conversion_rate = (offer["conversions"] / offer["clicks"] * 100) if offer["clicks"] > 0 else 0

            if conversion_rate >= min_conversion_rate:
                winners.append({
                    "offer_id": offer_id,
                    "name": offer.get("name", offer_id),
                    "conversion_rate": conversion_rate,
                    "revenue": offer["revenue"],
                    "roi": offer["roi"],
                    "clicks": offer["clicks"],
                    "conversions": offer["conversions"]
                })

        # Sort by ROI (best first)
        winners.sort(key=lambda x: x["roi"], reverse=True)
        return winners


# Global tracker instance
tracker = Tracker()


# Flask routes
@app.route('/track/click/<offer_id>')
def track_click_endpoint(offer_id: str):
    """Track click and redirect to offer."""
    source = request.args.get('source', 'unknown')
    click_id = tracker.track_click(offer_id, source)

    # Get offer URL
    offer = tracker.offers.get(offer_id, {})
    target_url = offer.get("url", "https://example.com")

    # Redirect to offer
    return redirect(f"{target_url}?ref={click_id}")


@app.route('/track/conversion', methods=['POST'])
def track_conversion_endpoint():
    """Track conversion (called by postback URL)."""
    data = request.get_json()
    click_id = data.get("click_id")
    amount = data.get("amount", 0)

    success = tracker.track_conversion(click_id, amount)

    return jsonify({"success": success})


@app.route('/api/stats')
def get_stats_endpoint():
    """Get tracking stats."""
    return jsonify(tracker.get_stats())


@app.route('/api/winners')
def get_winners_endpoint():
    """Get winning offers."""
    min_rate = float(request.args.get('min_rate', 2.0))
    winners = tracker.get_winners(min_rate)
    return jsonify(winners)


@app.route('/pixel/<click_id>.gif')
def tracking_pixel(click_id: str):
    """Tracking pixel for email opens."""
    # Log pixel view
    print(f"📧 Pixel viewed: {click_id}")

    # Return 1x1 transparent GIF
    return send_file('pixel.gif', mimetype='image/gif')


def main():
    """Start tracking server."""
    print("=" * 60)
    print("SELF-HOSTED TRACKER")
    print("=" * 60)
    print("\n🔍 Tracking clicks and conversions...")
    print("📊 Stats: http://localhost:9000/api/stats")
    print("🏆 Winners: http://localhost:9000/api/winners")
    print("\n✅ Ready to track!\n")

    app.run(host='0.0.0.0', port=9000, debug=False)


if __name__ == "__main__":
    main()
