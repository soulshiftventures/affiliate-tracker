"""
JVZoo/ClickBank Offer Scraper with Auto-Registration
Finds high-commission offers and registers them in tracker
"""

import requests
import json
import os
from datetime import datetime
from typing import List, Dict
from tracker import tracker

class OfferScraper:
    """Scrape and auto-register affiliate offers."""

    def __init__(self, jvzoo_api_key: str = None):
        self.jvzoo_api_key = jvzoo_api_key or os.getenv("JVZOO_API_KEY")
        self.offers = []

    def get_jvzoo_offers(self) -> List[Dict]:
        """Get JVZoo offers via API and auto-generate affiliate links."""
        print("🔍 Fetching JVZoo offers...")

        if not self.jvzoo_api_key:
            print("⚠️ No JVZoo API key - using manual registration")
            return self._get_manual_offers()

        try:
            # JVZoo API endpoint for marketplace
            url = "https://www.jvzoo.com/api/affiliate/products"
            headers = {"Authorization": f"Bearer {self.jvzoo_api_key}"}

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                products = response.json()

                # Filter for high commission instant payout
                offers = []
                for product in products.get('products', [])[:20]:
                    if product.get('instant_commission') and product.get('commission_amount', 0) >= 50:
                        offers.append({
                            "id": f"jvzoo_{product['id']}",
                            "name": product['name'],
                            "network": "jvzoo",
                            "commission": product['commission_amount'],
                            "payout_type": "instant",
                            "url": product['affiliate_url'],
                            "niche": product.get('category', 'unknown'),
                            "score": product['commission_amount'] * 2.0  # Instant payout bonus
                        })

                self.offers.extend(offers)
                print(f"✅ Found {len(offers)} JVZoo offers")
                return offers
            else:
                print(f"❌ JVZoo API error: {response.status_code}")
                return self._get_manual_offers()

        except Exception as e:
            print(f"❌ Error: {e}")
            return self._get_manual_offers()

    def _get_manual_offers(self) -> List[Dict]:
        """Fallback: Manual high-performing offers to test."""
        print("📝 Using curated manual offers...")

        # These are proven JVZoo/ClickBank offers you can promote
        # Replace with your actual affiliate links after approval
        offers = [
            {
                "id": "offer_high_ticket_course",
                "name": "High-Ticket Course (Example)",
                "network": "jvzoo",
                "commission": 300,
                "payout_type": "instant",
                "url": "YOUR_AFFILIATE_LINK_HERE",
                "niche": "make_money_online",
                "score": 600
            },
            {
                "id": "offer_software_tool",
                "name": "Software Tool (Example)",
                "network": "jvzoo",
                "commission": 150,
                "payout_type": "instant",
                "url": "YOUR_AFFILIATE_LINK_HERE",
                "niche": "marketing_tools",
                "score": 300
            },
            {
                "id": "offer_membership",
                "name": "Membership Site (Example)",
                "network": "clickbank",
                "commission": 97,
                "payout_type": "weekly",
                "url": "YOUR_AFFILIATE_LINK_HERE",
                "niche": "business",
                "score": 97
            },
            {
                "id": "offer_ebook_bundle",
                "name": "Ebook Bundle (Example)",
                "network": "jvzoo",
                "commission": 47,
                "payout_type": "instant",
                "url": "YOUR_AFFILIATE_LINK_HERE",
                "niche": "self_help",
                "score": 94
            },
            {
                "id": "offer_coaching",
                "name": "Coaching Program (Example)",
                "network": "jvzoo",
                "commission": 497,
                "payout_type": "instant",
                "url": "YOUR_AFFILIATE_LINK_HERE",
                "niche": "coaching",
                "score": 994
            }
        ]

        self.offers.extend(offers)
        print(f"✅ Loaded {len(offers)} manual offers")
        print(f"⚠️ Replace 'YOUR_AFFILIATE_LINK_HERE' with real links from JVZoo")
        return offers

    def rank_offers(self) -> List[Dict]:
        """Sort offers by score (commission × payout speed)."""
        self.offers.sort(key=lambda x: x.get("score", 0), reverse=True)
        return self.offers

    def auto_register_offers(self, count: int = 10):
        """Auto-register top offers in tracker."""
        print(f"\n📦 Auto-registering top {count} offers...")

        top_offers = self.offers[:count]

        for offer in top_offers:
            # Register in tracker
            tracker.register_offer(offer["id"], {
                "name": offer["name"],
                "url": offer["url"],
                "commission": offer["commission"],
                "network": offer["network"],
                "payout_type": offer["payout_type"]
            })

            print(f"✅ {offer['name']} - ${offer['commission']} ({offer['payout_type']})")

        print(f"\n🎉 {len(top_offers)} offers registered!")
        print(f"\n📊 View at: http://localhost:9000/api/stats")

    def get_tracking_links(self):
        """Show tracking links for registered offers."""
        print("\n🔗 YOUR TRACKING LINKS:")
        print("="*60)

        for offer in self.offers[:10]:
            tracking_url = f"http://localhost:9000/track/click/{offer['id']}"
            print(f"\n{offer['name']}")
            print(f"   Tracking URL: {tracking_url}")
            print(f"   Commission: ${offer['commission']}")

        print("\n" + "="*60)
        print("Use these links in Udimi, not your raw affiliate links")

    def save_config(self):
        """Save offer config for easy updates."""
        config = {
            "offers": [
                {
                    "id": offer["id"],
                    "name": offer["name"],
                    "url": "REPLACE_WITH_YOUR_AFFILIATE_LINK",
                    "commission": offer["commission"]
                }
                for offer in self.offers[:10]
            ]
        }

        with open("offer_config.json", "w") as f:
            json.dump(config, f, indent=2)

        print(f"\n💾 Saved offer_config.json")
        print("Edit this file to add your real affiliate links")


def main():
    """Setup offers and register automatically."""
    print("="*60)
    print("AFFILIATE OFFER SETUP")
    print("="*60)
    print()

    # Initialize scraper
    api_key = os.getenv("JVZOO_API_KEY")
    if api_key:
        print(f"✅ JVZoo API key found")
    else:
        print("⚠️ No JVZOO_API_KEY - using manual offers")

    scraper = OfferScraper(api_key)

    # Get offers
    scraper.get_jvzoo_offers()

    # Rank by potential
    scraper.rank_offers()

    # Show top offers
    print("\n🏆 TOP 10 OFFERS:")
    print("="*60)
    for i, offer in enumerate(scraper.offers[:10], 1):
        print(f"{i}. {offer['name']}")
        print(f"   ${offer['commission']} - {offer['payout_type']}")
        print(f"   Score: {offer['score']:.0f}")
        print()

    # Ask to register
    response = input("Auto-register these offers? (y/n): ").lower()

    if response == 'y':
        scraper.auto_register_offers(10)
        scraper.get_tracking_links()
        scraper.save_config()
    else:
        print("❌ Cancelled - no offers registered")


if __name__ == "__main__":
    main()
