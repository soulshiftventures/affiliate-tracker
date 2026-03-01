"""
Udimi Traffic Buyer Integration
Automatically buys solo ads and tracks spend
"""

import requests
import json
import time
from typing import Dict, List
from datetime import datetime
from pathlib import Path

class TrafficBuyer:
    """Buy traffic from Udimi automatically."""

    def __init__(self, budget: float = 500):
        self.budget = budget
        self.spent = 0
        self.orders = []
        self.orders_file = Path("data/traffic/orders.json")
        self.orders_file.parent.mkdir(parents=True, exist_ok=True)
        self._load_orders()

    def _load_orders(self):
        """Load existing orders."""
        if self.orders_file.exists():
            with open(self.orders_file) as f:
                data = json.load(f)
                self.orders = data.get("orders", [])
                self.spent = data.get("spent", 0)

    def _save_orders(self):
        """Save orders to file."""
        with open(self.orders_file, 'w') as f:
            json.dump({
                "orders": self.orders,
                "spent": self.spent,
                "budget": self.budget,
                "remaining": self.budget - self.spent
            }, f, indent=2)

    def buy_traffic(
        self,
        offer_id: str,
        offer_url: str,
        amount: float,
        seller: str = "top_rated"
    ) -> Dict:
        """
        Buy traffic from Udimi.

        Args:
            offer_id: Offer identifier
            offer_url: Tracking URL to send traffic to
            amount: Budget for this order
            seller: "top_rated" or specific seller username

        Returns:
            Order details
        """
        if self.spent + amount > self.budget:
            print(f"❌ Budget exceeded: ${self.spent + amount} > ${self.budget}")
            return {"error": "budget_exceeded"}

        print(f"💰 Buying ${amount} traffic for {offer_id}...")

        # Note: This is a PLACEHOLDER
        # Real implementation would use Udimi API or manual ordering
        # For now, we simulate the order

        order = {
            "order_id": f"order_{int(time.time())}",
            "offer_id": offer_id,
            "offer_url": offer_url,
            "amount": amount,
            "seller": seller,
            "status": "pending",
            "clicks_ordered": int(amount / 0.5),  # Assume $0.50/click
            "clicks_received": 0,
            "created_at": datetime.now().isoformat()
        }

        self.orders.append(order)
        self.spent += amount
        self._save_orders()

        print(f"✅ Order placed: {order['clicks_ordered']} clicks for ${amount}")
        print(f"💵 Budget remaining: ${self.budget - self.spent}")

        return order

    def update_order_status(self, order_id: str, clicks_received: int):
        """Update order with clicks received."""
        for order in self.orders:
            if order["order_id"] == order_id:
                order["clicks_received"] = clicks_received
                if clicks_received >= order["clicks_ordered"]:
                    order["status"] = "completed"
                else:
                    order["status"] = "in_progress"
                self._save_orders()
                print(f"✅ Order {order_id}: {clicks_received}/{order['clicks_ordered']} clicks")
                break

    def get_pending_orders(self) -> List[Dict]:
        """Get orders that are still pending/in progress."""
        return [o for o in self.orders if o["status"] in ["pending", "in_progress"]]

    def get_budget_remaining(self) -> float:
        """Get remaining budget."""
        return self.budget - self.spent

    def test_offers(self, offers: List[Dict], budget_per_offer: float = 10) -> List[str]:
        """
        Test multiple offers with small budget.

        Args:
            offers: List of offer dicts with 'id' and 'url'
            budget_per_offer: Budget for each test

        Returns:
            List of order IDs
        """
        print(f"\n🧪 TESTING {len(offers)} OFFERS")
        print(f"💰 Budget per offer: ${budget_per_offer}")
        print(f"💵 Total test budget: ${len(offers) * budget_per_offer}\n")

        order_ids = []

        for offer in offers:
            order = self.buy_traffic(
                offer_id=offer["id"],
                offer_url=offer["url"],
                amount=budget_per_offer
            )

            if "error" not in order:
                order_ids.append(order["order_id"])
                time.sleep(1)  # Rate limit

        return order_ids

    def scale_winners(self, winners: List[Dict], total_budget: float):
        """
        Scale winning offers proportionally.

        Args:
            winners: List of winner dicts with 'offer_id', 'url', 'roi'
            total_budget: Total budget to split
        """
        if not winners:
            print("❌ No winners to scale")
            return

        print(f"\n🚀 SCALING {len(winners)} WINNERS")
        print(f"💰 Total budget: ${total_budget}\n")

        # Calculate total ROI for proportional split
        total_roi = sum(w["roi"] for w in winners)

        for winner in winners:
            # Allocate budget proportional to ROI
            if total_roi > 0:
                winner_budget = (winner["roi"] / total_roi) * total_budget
            else:
                # Equal split if no ROI data
                winner_budget = total_budget / len(winners)

            print(f"📈 {winner['name']}")
            print(f"   ROI: {winner['roi']:.1f}%")
            print(f"   Budget: ${winner_budget:.2f}")

            self.buy_traffic(
                offer_id=winner["offer_id"],
                offer_url=winner["url"],
                amount=winner_budget
            )

            time.sleep(1)  # Rate limit

        print(f"\n✅ All winners scaled!")
        print(f"💵 Remaining budget: ${self.get_budget_remaining()}")

    def get_stats(self) -> Dict:
        """Get traffic buying stats."""
        return {
            "budget": self.budget,
            "spent": self.spent,
            "remaining": self.budget - self.spent,
            "orders": len(self.orders),
            "clicks_ordered": sum(o["clicks_ordered"] for o in self.orders),
            "clicks_received": sum(o["clicks_received"] for o in self.orders),
            "pending_orders": len(self.get_pending_orders())
        }


def main():
    """Test traffic buyer."""
    buyer = TrafficBuyer(budget=500)

    # Test offers
    test_offers = [
        {"id": "offer_1", "url": "http://localhost:9000/track/click/offer_1"},
        {"id": "offer_2", "url": "http://localhost:9000/track/click/offer_2"},
        {"id": "offer_3", "url": "http://localhost:9000/track/click/offer_3"},
    ]

    buyer.test_offers(test_offers, budget_per_offer=10)

    # Show stats
    print("\n📊 TRAFFIC STATS:")
    print(json.dumps(buyer.get_stats(), indent=2))


if __name__ == "__main__":
    main()
