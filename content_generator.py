"""
AI Content Generator
Uses Claude API (free tier) to generate affiliate content at scale
"""

import anthropic
import os
import json
from typing import List, Dict

class ContentGenerator:
    """Generate viral affiliate content using Claude."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if self.api_key:
            self.client = anthropic.Anthropic(api_key=self.api_key)
        else:
            self.client = None
            print("⚠️ No Claude API key - will generate template content")

    def generate_reddit_post(self, offer: Dict) -> str:
        """Generate helpful Reddit post (not spammy)."""

        if not self.client:
            return self._template_reddit_post(offer)

        try:
            prompt = f"""Write a helpful Reddit post recommending this product:

Product: {offer['name']}
Niche: {offer.get('niche', 'general')}
Commission: ${offer['commission']}

Rules:
- Be genuinely helpful, not salesy
- Share personal experience (write as if you used it)
- Mention 2-3 specific benefits
- Include affiliate link naturally at end
- Max 300 words
- Sound authentic, not like a robot

Affiliate link: {offer['url']}"""

            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )

            return message.content[0].text

        except Exception as e:
            print(f"❌ Error generating Reddit post: {e}")
            return self._template_reddit_post(offer)

    def generate_twitter_thread(self, offer: Dict) -> List[str]:
        """Generate Twitter thread (5-7 tweets)."""

        if not self.client:
            return self._template_twitter_thread(offer)

        try:
            prompt = f"""Write a Twitter thread (5 tweets) about this product:

Product: {offer['name']}
Niche: {offer.get('niche', 'general')}

Rules:
- Tweet 1: Hook (shocking stat or question)
- Tweets 2-4: Value/benefits
- Tweet 5: CTA with link
- Each tweet max 280 characters
- Use emojis sparingly
- Sound human, not robotic

Affiliate link: {offer['url']}

Format as JSON array of strings."""

            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=700,
                messages=[{"role": "user", "content": prompt}]
            )

            # Parse response
            text = message.content[0].text
            # Extract JSON array if present
            if "[" in text and "]" in text:
                start = text.index("[")
                end = text.rindex("]") + 1
                return json.loads(text[start:end])

            return text.split("\n\n")

        except Exception as e:
            print(f"❌ Error generating Twitter thread: {e}")
            return self._template_twitter_thread(offer)

    def generate_tiktok_script(self, offer: Dict) -> str:
        """Generate TikTok video script (30-60 seconds)."""

        if not self.client:
            return self._template_tiktok_script(offer)

        try:
            prompt = f"""Write a TikTok video script (30-60 seconds) about:

Product: {offer['name']}
Niche: {offer.get('niche', 'general')}

Format:
[HOOK - first 3 seconds, shocking]
[BODY - main content, 20-40 seconds]
[CTA - call to action, last 5 seconds]

Rules:
- Start with attention-grabbing hook
- Fast-paced, energetic
- Show don't tell
- End with clear CTA + link in bio
- Include text overlay suggestions

Affiliate link goes in bio."""

            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=600,
                messages=[{"role": "user", "content": prompt}]
            )

            return message.content[0].text

        except Exception as e:
            print(f"❌ Error generating TikTok script: {e}")
            return self._template_tiktok_script(offer)

    def generate_medium_article(self, offer: Dict) -> Dict:
        """Generate Medium article (1000-1500 words)."""

        if not self.client:
            return self._template_medium_article(offer)

        try:
            prompt = f"""Write a Medium article reviewing this product:

Product: {offer['name']}
Niche: {offer.get('niche', 'general')}

Structure:
- Title (SEO-friendly)
- Introduction (personal story hook)
- What it is
- How it works
- Who it's for
- Pros and cons
- My verdict
- CTA

Length: 1000-1200 words
Tone: Professional but personal
Include: Affiliate link 2-3 times naturally

Affiliate link: {offer['url']}

Return as JSON with title and content."""

            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )

            # Parse response
            text = message.content[0].text
            return {
                "title": offer['name'] + " Review: Worth It?",
                "content": text
            }

        except Exception as e:
            print(f"❌ Error generating Medium article: {e}")
            return self._template_medium_article(offer)

    # Template fallbacks (no API key needed)
    def _template_reddit_post(self, offer: Dict) -> str:
        return f"""I've been using {offer['name']} for the past few weeks and wanted to share my experience.

The main benefits I've noticed:
- [Benefit 1]
- [Benefit 2]
- [Benefit 3]

It's helped me [specific result]. If you're interested, here's the link: {offer['url']}

Happy to answer questions!"""

    def _template_twitter_thread(self, offer: Dict) -> List[str]:
        return [
            f"I found something that changed everything for me 🔥",
            f"{offer['name']} helped me [specific result]",
            "Here's what makes it different: [unique feature]",
            "Who is this for? [target audience description]",
            f"Check it out here: {offer['url']}"
        ]

    def _template_tiktok_script(self, offer: Dict) -> str:
        return f"""[HOOK] Wait, this actually works? 😱

[BODY]
So I tried {offer['name']} and here's what happened...
[Show before/after or result]
The crazy part? [Unique benefit]
[Screen recording or demo]

[CTA]
Link in bio if you want to try it 👆

#affiliate #{offer.get('niche', 'product')}"""

    def _template_medium_article(self, offer: Dict) -> Dict:
        return {
            "title": f"{offer['name']} Review: My Honest Experience",
            "content": f"""I wasn't sure about {offer['name']} at first...

But after [time period], I can say [verdict].

## What It Is
[Description]

## How It Works
[Process]

## Who It's For
[Target audience]

## My Verdict
[Honest review]

[Learn more here]({offer['url']})"""
        }


def main():
    """Test content generator."""
    generator = ContentGenerator()

    test_offer = {
        "name": "Commission Hero",
        "network": "clickbank",
        "commission": 997,
        "url": "https://example.com/affiliate",
        "niche": "make_money_online"
    }

    print("🎨 Generating content...\n")

    # Reddit post
    reddit = generator.generate_reddit_post(test_offer)
    print("REDDIT POST:")
    print(reddit)
    print("\n" + "="*60 + "\n")

    # Twitter thread
    twitter = generator.generate_twitter_thread(test_offer)
    print("TWITTER THREAD:")
    for i, tweet in enumerate(twitter, 1):
        print(f"{i}. {tweet}")
    print("\n" + "="*60 + "\n")

    # TikTok script
    tiktok = generator.generate_tiktok_script(test_offer)
    print("TIKTOK SCRIPT:")
    print(tiktok)


if __name__ == "__main__":
    main()
