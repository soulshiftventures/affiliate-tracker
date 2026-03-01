"""
Auto Poster - Uses proven GitHub tools for distribution
- TikTok: wkaisertexas/tiktok-uploader
- Reddit: PRAW
- Twitter: Playwright automation
"""

import subprocess
import time
import json
from pathlib import Path
from typing import List, Dict

class AutoPoster:
    """Automatically post content across platforms."""

    def __init__(self):
        self.stats = {
            "tiktok_posted": 0,
            "reddit_posted": 0,
            "twitter_posted": 0,
            "medium_posted": 0,
            "failures": 0
        }

    def post_to_tiktok(self, video_path: str, description: str, hashtags: List[str]) -> bool:
        """
        Post to TikTok using tiktok-uploader package.
        98% success rate, 10-20 videos/hour
        """
        try:
            print(f"📱 Posting to TikTok: {description[:50]}...")

            full_description = description + " " + " ".join(f"#{tag}" for tag in hashtags)

            # Using tiktok-uploader CLI
            # Install: pip install tiktok-uploader
            # Setup: tiktok-uploader --setup (one-time cookie setup)

            cmd = [
                "tiktok-uploader",
                video_path,
                "-d", full_description,
                "--headless"
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

            if result.returncode == 0:
                self.stats["tiktok_posted"] += 1
                print("✅ TikTok posted successfully")
                return True
            else:
                print(f"❌ TikTok upload failed: {result.stderr}")
                self.stats["failures"] += 1
                return False

        except Exception as e:
            print(f"❌ Error posting to TikTok: {e}")
            self.stats["failures"] += 1
            return False

    def post_to_reddit(self, subreddit: str, title: str, content: str) -> bool:
        """
        Post to Reddit using PRAW.
        Industry standard, reliable.
        """
        try:
            import praw

            print(f"🤖 Posting to r/{subreddit}...")

            # Initialize Reddit client
            # Credentials should be in environment or config
            reddit = praw.Reddit(
                client_id="YOUR_CLIENT_ID",
                client_secret="YOUR_CLIENT_SECRET",
                user_agent="affiliate_bot",
                username="YOUR_USERNAME",
                password="YOUR_PASSWORD"
            )

            # Post
            subreddit_obj = reddit.subreddit(subreddit)
            submission = subreddit_obj.submit(title, selftext=content)

            self.stats["reddit_posted"] += 1
            print(f"✅ Posted to Reddit: {submission.url}")
            return True

        except ImportError:
            print("❌ PRAW not installed: pip install praw")
            return False
        except Exception as e:
            print(f"❌ Error posting to Reddit: {e}")
            self.stats["failures"] += 1
            return False

    def post_to_twitter(self, thread: List[str]) -> bool:
        """
        Post Twitter thread using Playwright (no API cost).
        """
        try:
            from playwright.sync_api import sync_playwright

            print(f"🐦 Posting to Twitter ({len(thread)} tweets)...")

            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()

                # Load cookies for authentication
                if Path("twitter_cookies.json").exists():
                    context.add_cookies(json.load(open("twitter_cookies.json")))

                page = context.new_page()
                page.goto("https://twitter.com/compose/tweet")

                # Post each tweet in thread
                for i, tweet in enumerate(thread):
                    time.sleep(2)  # Human-like delay

                    # Type tweet
                    tweet_box = page.locator('[data-testid="tweetTextarea_0"]')
                    tweet_box.fill(tweet)

                    # Click tweet button
                    tweet_btn = page.locator('[data-testid="tweetButtonInline"]')
                    tweet_btn.click()

                    time.sleep(3)  # Wait for post

                    self.stats["twitter_posted"] += 1
                    print(f"✅ Posted tweet {i+1}/{len(thread)}")

                browser.close()
                return True

        except ImportError:
            print("❌ Playwright not installed: pip install playwright && playwright install")
            return False
        except Exception as e:
            print(f"❌ Error posting to Twitter: {e}")
            self.stats["failures"] += 1
            return False

    def post_to_medium(self, title: str, content: str, tags: List[str]) -> bool:
        """
        Post to Medium using their API.
        """
        try:
            import requests

            print(f"📝 Posting to Medium: {title[:50]}...")

            # Medium API requires access token
            # Get from: https://medium.com/me/settings
            headers = {
                "Authorization": f"Bearer YOUR_MEDIUM_TOKEN",
                "Content-Type": "application/json"
            }

            # Get user ID first
            user_response = requests.get("https://api.medium.com/v1/me", headers=headers)
            user_id = user_response.json()["data"]["id"]

            # Create post
            post_data = {
                "title": title,
                "contentFormat": "markdown",
                "content": content,
                "tags": tags,
                "publishStatus": "public"
            }

            response = requests.post(
                f"https://api.medium.com/v1/users/{user_id}/posts",
                headers=headers,
                json=post_data
            )

            if response.status_code == 201:
                post_url = response.json()["data"]["url"]
                self.stats["medium_posted"] += 1
                print(f"✅ Posted to Medium: {post_url}")
                return True
            else:
                print(f"❌ Medium post failed: {response.status_code}")
                self.stats["failures"] += 1
                return False

        except Exception as e:
            print(f"❌ Error posting to Medium: {e}")
            self.stats["failures"] += 1
            return False

    def get_stats(self) -> Dict:
        """Get posting statistics."""
        return self.stats


def main():
    """Test auto poster."""
    poster = AutoPoster()

    # Test Reddit
    success = poster.post_to_reddit(
        "test",
        "Testing Auto Poster",
        "This is an automated test post."
    )

    # Show stats
    print("\n📊 STATS:")
    print(json.dumps(poster.get_stats(), indent=2))


if __name__ == "__main__":
    main()
