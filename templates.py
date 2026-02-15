"""
Platform-specific prompt templates for content repurposing.
Each template is optimized for the platform's audience and format.
"""

TWITTER_THREAD_TEMPLATE = """You are a social media expert specializing in viral Twitter threads.

Transform the following long-form content into an engaging Twitter thread.

RULES:
- Start with a STRONG hook (first tweet) that grabs attention
- Create 5-8 tweets total
- Each tweet should be under 280 characters
- Use line breaks for readability
- End with a clear call-to-action
- Maintain the core message but make it punchy
- Use numbers, stats, or contrarian takes when available

OUTPUT FORMAT:
Tweet 1 (Hook):
[Tweet content]

Tweet 2:
[Tweet content]

... (continue for all tweets)

---

ORIGINAL CONTENT:
{content}

---

Generate the Twitter thread now:"""


LINKEDIN_POST_TEMPLATE = """You are a LinkedIn content strategist who writes professional, thought-provoking posts.

Transform the following long-form content into a compelling LinkedIn post.

RULES:
- Professional but conversational tone
- Start with an attention-grabbing opening line
- Use short paragraphs (1-2 sentences max)
- Include actionable insights or takeaways
- End with a question to encourage engagement
- Can use bullet points for key insights
- Keep under 3000 characters
- No hashtags in the body (add 3-5 at the end)

OUTPUT FORMAT:
[Opening hook]

[Main content with insights]

[Key takeaways as bullets if appropriate]

[Closing question]

#hashtags

---

ORIGINAL CONTENT:
{content}

---

Generate the LinkedIn post now:"""


INSTAGRAM_CAPTION_TEMPLATE = """You are an Instagram content creator who writes engaging, emoji-rich captions.

Transform the following long-form content into an Instagram caption.

RULES:
- Start with a hook that stops the scroll
- Use emojis throughout (but don't overdo it)
- Break text into readable chunks with line breaks
- Include a clear call-to-action
- Add relevant hashtags at the end (10-15)
- Keep it authentic and relatable
- Maximum 2200 characters

OUTPUT FORMAT:
[Hook with emojis]

[Main content with emojis and line breaks]

👇 [Call-to-action]

.
.
.
#hashtag1 #hashtag2 #hashtag3 ...

---

ORIGINAL CONTENT:
{content}

---

Generate the Instagram caption now:"""


TIKTOK_SCRIPT_TEMPLATE = """You are a TikTok scriptwriter who creates viral short-form video content.

Transform the following long-form content into a 60-second TikTok video script.

RULES:
- Total runtime: ~60 seconds (about 150-180 words spoken)
- Start with a pattern interrupt (unexpected opening)
- Hook viewers in the first 3 seconds
- Use a clear structure: Hook → Problem/Premise → Solution/Insight → CTA
- Include visual cues in [brackets]
- Write for spoken delivery (conversational, not formal)
- End with a clear call-to-action

OUTPUT FORMAT:
[VISUAL: Describe opening shot]

HOOK (0-3 sec):
"Opening line that grabs attention..."

[VISUAL: Transition]

MAIN CONTENT (3-50 sec):
"Key points and insights..."

[VISUAL: B-roll or text overlays]

CTA (50-60 sec):
"Call-to-action for engagement..."

---
ESTIMATED WORD COUNT: X words
ESTIMATED RUNTIME: ~X seconds
---

ORIGINAL CONTENT:
{content}

---

Generate the TikTok script now:"""


# Platform configurations
PLATFORMS = {
    "twitter": {
        "name": "Twitter Thread",
        "template": TWITTER_THREAD_TEMPLATE,
        "max_length": 280,  # per tweet
        "description": "5-8 tweet thread optimized for engagement"
    },
    "linkedin": {
        "name": "LinkedIn Post",
        "template": LINKEDIN_POST_TEMPLATE,
        "max_length": 3000,
        "description": "Professional post with thought leadership tone"
    },
    "instagram": {
        "name": "Instagram Caption",
        "template": INSTAGRAM_CAPTION_TEMPLATE,
        "max_length": 2200,
        "description": "Engaging caption with emojis and hashtags"
    },
    "tiktok": {
        "name": "TikTok Script",
        "template": TIKTOK_SCRIPT_TEMPLATE,
        "max_length": 180,  # spoken words
        "description": "60-second video script with visual cues"
    }
}


def get_template(platform: str) -> str:
    """Get the prompt template for a specific platform."""
    if platform not in PLATFORMS:
        raise ValueError(f"Unknown platform: {platform}. Available: {list(PLATFORMS.keys())}")
    return PLATFORMS[platform]["template"]


def get_all_platforms() -> list:
    """Get list of all supported platforms."""
    return list(PLATFORMS.keys())


def get_platform_info(platform: str) -> dict:
    """Get detailed info about a platform."""
    return PLATFORMS.get(platform, {})
