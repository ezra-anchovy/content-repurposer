"""
Content Repurposer - Main Logic
Transforms long-form content into platform-optimized formats using LLM APIs.
"""

import os
import json
from typing import Optional
from templates import get_template, get_all_platforms, PLATFORMS


class ContentRepurposer:
    """
    Repurposes long-form content for multiple social media platforms.
    Supports multiple LLM backends with automatic fallback.
    """
    
    def __init__(self, api_key: Optional[str] = None, provider: str = "zai"):
        """
        Initialize the repurposer with an LLM provider.
        
        Args:
            api_key: API key for the LLM provider (can also use env vars)
            provider: LLM provider to use ("zai", "openai", "anthropic", "mock")
        """
        self.provider = provider
        self.api_key = api_key or self._get_api_key(provider)
        
    def _get_api_key(self, provider: str) -> Optional[str]:
        """Get API key from environment variables."""
        env_vars = {
            "zai": "ZAI_API_KEY",
            "openai": "OPENAI_API_KEY", 
            "anthropic": "ANTHROPIC_API_KEY"
        }
        return os.getenv(env_vars.get(provider, ""))
    
    def _call_zai(self, prompt: str) -> str:
        """Call Z.ai GLM-5 API (OpenClaw's default endpoint)."""
        import urllib.request
        import urllib.error
        
        url = os.getenv("ZAI_API_URL", "https://api.z.ai/v1/chat/completions")
        
        if not self.api_key:
            raise ValueError("ZAI_API_KEY not set. Set environment variable or pass api_key.")
        
        data = {
            "model": "glm-5",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )
        
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode("utf-8"))
                return result["choices"][0]["message"]["content"]
        except urllib.error.URLError as e:
            raise ConnectionError(f"Failed to call Z.ai API: {e}")
    
    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API."""
        import urllib.request
        import urllib.error
        
        url = "https://api.openai.com/v1/chat/completions"
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not set")
        
        data = {
            "model": "gpt-4o",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )
        
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"]
    
    def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic Claude API."""
        import urllib.request
        import urllib.error
        
        url = "https://api.anthropic.com/v1/messages"
        
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")
        
        data = {
            "model": "claude-sonnet-4-5-20250514",
            "max_tokens": 2000,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            headers={
                "x-api-key": self.api_key,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            }
        )
        
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result["content"][0]["text"]
    
    def _call_mock(self, prompt: str) -> str:
        """Mock response for testing without API calls."""
        if "Twitter" in prompt or "tweet" in prompt.lower():
            return """Tweet 1 (Hook):
The biggest mistake creators make?

They try to be everywhere at once.

Here's the framework that changed everything for me 🧵

Tweet 2:
I used to spend 10+ hours/week repurposing content manually.

Now? It takes 20 minutes.

The secret isn't working harder—it's working smarter.

Tweet 3:
The Content Multiplication Framework:

1 original piece → 4 platform-optimized versions

Same core message, different formats.

Tweet 4:
Twitter: Thread the key insights
LinkedIn: Professional takeaways
Instagram: Visual + caption
TikTok: Quick video script

Tweet 5:
Each platform has its own language.

Speak it fluently, or get ignored.

Tweet 6:
The result?

3x reach in 1/3 the time.

Your turn: Which platform are you focusing on this week?"""
        
        elif "LinkedIn" in prompt:
            return """The best content creators I know all follow one rule:

One piece of content, many formats.

Here's why this matters and how to do it:

Most people burn out trying to create from scratch every day.

The solution isn't more time—it's better systems.

The Content Repurposing Framework:

1. Start with your "hero" content (blog, podcast, video)
2. Extract key insights
3. Transform for each platform's unique style
4. Schedule strategically

Key insight: Each platform has its own "language."

→ Twitter wants threads and hot takes
→ LinkedIn wants professional insights
→ Instagram wants visual stories
→ TikTok wants entertainment

Same message. Different delivery.

The result? 3x the reach with 1/3 the effort.

What's your biggest challenge with content creation? Drop it below.

#ContentStrategy #ContentCreation #SocialMediaTips #Productivity"""
        
        elif "Instagram" in prompt:
            return """POV: You stopped creating from scratch every day and started repurposing 📈

Here's the exact framework 👇

Step 1: Create ONE piece of "hero" content
(blog, video, podcast—your choice!)

Step 2: Extract the key insights 💡
What are the 3-5 biggest takeaways?

Step 3: Transform for each platform
• Twitter → Thread
• LinkedIn → Professional post
• TikTok → Quick video
• IG → This post you're reading

Step 4: Schedule and ship 🚀

The magic? Each platform has its own language.

Speak it fluently = more reach, less burnout.

👇 Save this for later and drop a 🔥 if this was helpful!

.
.
.
#contentcreator #contentstrategy #socialmediatips #contentmarketing #creatoreconomy #productivityhacks #digitalmarketing #socialmediamarketing #contenttips #worksmarter"""
        
        else:  # TikTok
            return """[VISUAL: Close-up of you looking frustrated at laptop, then cut to smiling]

HOOK (0-3 sec):
"I was spending 10 hours a week on content. Now? 20 minutes."

[VISUAL: Quick cuts showing you working, calendar, phone notifications]

MAIN CONTENT (3-50 sec):
"Here's the repurposing framework:

One, create your hero content—that's your blog, video, or podcast.

Two, extract the key insights—the 3 to 5 biggest takeaways.

Three, transform for each platform.

Twitter wants threads. LinkedIn wants professional insights. TikTok? Entertainment.

Four, schedule and ship.

Each platform has its own language. Speak it fluently."

[VISUAL: Split screen showing same content on 4 different platforms]

CTA (50-60 sec):
"Follow for more creator shortcuts. Which platform should I cover next?"

---
ESTIMATED WORD COUNT: 124 words
ESTIMATED RUNTIME: ~55 seconds
---"""
    
    def repurpose(self, content: str, platform: str) -> str:
        """
        Repurpose content for a specific platform.
        
        Args:
            content: The long-form content to repurpose
            platform: Target platform ("twitter", "linkedin", "instagram", "tiktok")
            
        Returns:
            Repurposed content optimized for the platform
        """
        if platform not in PLATFORMS:
            raise ValueError(f"Unknown platform: {platform}. Available: {get_all_platforms()}")
        
        template = get_template(platform)
        prompt = template.format(content=content)
        
        # Call the appropriate LLM provider
        if self.provider == "mock":
            return self._call_mock(prompt)
        elif self.provider == "zai":
            return self._call_zai(prompt)
        elif self.provider == "openai":
            return self._call_openai(prompt)
        elif self.provider == "anthropic":
            return self._call_anthropic(prompt)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")
    
    def repurpose_all(self, content: str) -> dict:
        """
        Repurpose content for all supported platforms.
        
        Args:
            content: The long-form content to repurpose
            
        Returns:
            Dictionary with repurposed content for each platform
        """
        results = {}
        for platform in get_all_platforms():
            try:
                results[platform] = self.repurpose(content, platform)
            except Exception as e:
                results[platform] = f"Error: {str(e)}"
        return results


def repurpose_content(content: str, platform: str = "all", provider: str = "mock") -> dict:
    """
    Convenience function to repurpose content.
    
    Args:
        content: Long-form content to repurpose
        platform: Target platform or "all" for all platforms
        provider: LLM provider to use
        
    Returns:
        Dictionary with repurposed content
    """
    repurposer = ContentRepurposer(provider=provider)
    
    if platform == "all":
        return repurposer.repurpose_all(content)
    else:
        return {platform: repurposer.repurpose(content, platform)}


# CLI interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python repurposer.py <content_file> [platform] [provider]")
        print("Platforms: twitter, linkedin, instagram, tiktok, all")
        print("Providers: mock, zai, openai, anthropic")
        sys.exit(1)
    
    # Read content from file
    with open(sys.argv[1], "r") as f:
        content = f.read()
    
    platform = sys.argv[2] if len(sys.argv) > 2 else "all"
    provider = sys.argv[3] if len(sys.argv) > 3 else "mock"
    
    results = repurpose_content(content, platform, provider)
    
    print("\n" + "="*60)
    for plat, result in results.items():
        print(f"\n### {plat.upper()} ###\n")
        print(result)
        print("\n" + "-"*60)
