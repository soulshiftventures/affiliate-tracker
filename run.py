#!/usr/bin/env python3
"""
Affiliate Swarm - Main Runner
ONE COMMAND to start the money printer

Usage:
    python run.py --budget 100
"""

import argparse
import yaml
import json
import time
import threading
from pathlib import Path
from flask import Flask, jsonify, send_file
from datetime import datetime

# Import our modules
from offer_scraper import OfferScraper
from content_generator import ContentGenerator
from auto_poster import AutoPoster

# Flask app for dashboard
app = Flask(__name__)

# Global state
STATE = {
    "running": False,
    "revenue": 0,
    "spent": 0,
    "tiktok": 0,
    "reddit": 0,
    "twitter": 0,
    "medium": 0,
    "recent_activity": []
}

def log_activity(message: str):
    """Log activity to dashboard."""
    STATE["recent_activity"].insert(0, {
        "message": message,
        "time": datetime.now().strftime("%H:%M:%S")
    })
    # Keep only last 20 activities
    STATE["recent_activity"] = STATE["recent_activity"][:20]
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

def run_swarm(config: dict):
    """Main swarm logic - runs in background thread."""
    STATE["running"] = True
    log_activity("🚀 Affiliate Swarm starting...")

    # Load budget
    budget = config["budget"]["total"]
    log_activity(f"💰 Budget: ${budget}")

    # Step 1: Find offers
    log_activity("🔍 Finding top affiliate offers...")
    scraper = OfferScraper()
    scraper.scrape_jvzoo_launches()
    scraper.scrape_clickbank_top()
    scraper.rank_offers()
    offers = scraper.get_top_offers(5)
    log_activity(f"✅ Found {len(offers)} offers to promote")

    # Step 2: Generate content
    log_activity("🎨 Generating content with AI...")
    generator = ContentGenerator()
    poster = AutoPoster()

    content_count = 0

    while STATE["running"] and STATE["spent"] < budget:
        for offer in offers:
            if not STATE["running"]:
                break

            # Generate content for this offer
            log_activity(f"📝 Creating content for {offer['name']}...")

            # Reddit post
            reddit_post = generator.generate_reddit_post(offer)
            # TODO: Post to relevant subreddits
            # poster.post_to_reddit("entrepreneurship", offer['name'], reddit_post)
            STATE["reddit"] += 1
            log_activity(f"✅ Posted to Reddit")

            # Twitter thread
            twitter_thread = generator.generate_twitter_thread(offer)
            # TODO: Post thread
            # poster.post_to_twitter(twitter_thread)
            STATE["twitter"] += 1
            log_activity(f"✅ Posted to Twitter")

            # TikTok (if video exists)
            # tiktok_script = generator.generate_tiktok_script(offer)
            # TODO: Generate video from script
            # TODO: Upload with poster.post_to_tiktok()
            STATE["tiktok"] += 1
            log_activity(f"✅ Posted to TikTok")

            content_count += 3

            # Rate limiting (don't spam)
            time.sleep(60)  # 1 minute between batches

        # Check for conversions
        # TODO: Track clicks and sales
        # Update STATE["revenue"] when sales come in

        log_activity(f"📊 Stats: {content_count} posts, ${STATE['spent']}/{budget} spent")

        # Sleep before next round
        time.sleep(300)  # 5 minutes

    log_activity("⏸ Swarm stopped")
    STATE["running"] = False

# Flask routes for dashboard
@app.route('/')
def dashboard():
    """Serve dashboard HTML."""
    return send_file('dashboard.html')

@app.route('/api/stats')
def get_stats():
    """Return current stats as JSON."""
    return jsonify(STATE)

@app.route('/api/start', methods=['POST'])
def start_system():
    """Start the swarm."""
    if not STATE["running"]:
        # Load config
        with open('config.yaml') as f:
            config = yaml.safe_load(f)

        # Start swarm in background thread
        thread = threading.Thread(target=run_swarm, args=(config,))
        thread.daemon = True
        thread.start()

        return jsonify({"status": "started"})
    return jsonify({"status": "already running"})

@app.route('/api/stop', methods=['POST'])
def stop_system():
    """Stop the swarm."""
    STATE["running"] = False
    return jsonify({"status": "stopped"})

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Affiliate Swarm - Automated Money Printer')
    parser.add_argument('--budget', type=int, default=100, help='Total budget to spend')
    parser.add_argument('--port', type=int, default=8080, help='Dashboard port')
    args = parser.parse_args()

    print("=" * 60)
    print("💰 AFFILIATE SWARM")
    print("=" * 60)
    print(f"\n✅ Budget: ${args.budget}")
    print(f"✅ Dashboard: http://localhost:{args.port}")
    print(f"\n🚀 Opening dashboard...\n")

    # Update config with budget
    config_path = Path('config.yaml')
    if config_path.exists():
        with open(config_path) as f:
            config = yaml.safe_load(f)
        config['budget']['total'] = args.budget
        with open(config_path, 'w') as f:
            yaml.dump(config, f)

    # Start Flask dashboard
    app.run(host='0.0.0.0', port=args.port, debug=False)

if __name__ == "__main__":
    main()
