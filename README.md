# Content Repurposer

Transform one piece of long-form content into platform-optimized posts for Twitter, LinkedIn, Instagram, and TikTok.

## Features

- **Multi-Platform Support**: Generate content optimized for:
  - 🐦 **Twitter**: Engaging threads (5-8 tweets with hook)
  - 💼 **LinkedIn**: Professional thought-leadership posts
  - 📸 **Instagram**: Emoji-rich captions with hashtags
  - 🎵 **TikTok**: 60-second video scripts with visual cues

- **Multiple LLM Backends**: Support for:
  - Z.ai GLM-5 (OpenClaw's default)
  - OpenAI GPT-4
  - Anthropic Claude
  - Mock mode for testing

- **Simple Interfaces**:
  - **Live Demo**: [ezra-anchovy.github.io/content-repurposer](https://ezra-anchovy.github.io/content-repurposer/)
  - Web UI (Flask)
  - Python API
  - CLI

## Quick Start

### 1. Installation

```bash
cd /Users/al/.openclaw/workspace/products/content-repurposer

# No external dependencies required for mock mode!
# For web interface:
pip install flask

# For real LLM calls, you'll need API keys:
export ZAI_API_KEY="your-key"        # For Z.ai
export OPENAI_API_KEY="your-key"     # For OpenAI
export ANTHROPIC_API_KEY="your-key"  # For Claude
```

### 2. Using the Web Interface

```bash
python app.py
```

Then open http://127.0.0.1:5000 in your browser.

### 3. Using the CLI

```bash
# Create a file with your content
echo "Your long-form blog post content here..." > content.txt

# Repurpose for all platforms (mock mode)
python repurposer.py content.txt all mock

# Repurpose for specific platform
python repurposer.py content.txt twitter mock

# Use real LLM
python repurposer.py content.txt all zai
```

### 4. Using the Python API

```python
from repurposer import ContentRepurposer, repurpose_content

# Simple function
results = repurpose_content(
    content="Your long-form content here...",
    platform="all",  # or "twitter", "linkedin", "instagram", "tiktok"
    provider="mock"  # or "zai", "openai", "anthropic"
)

print(results["twitter"])
print(results["linkedin"])

# Or use the class for more control
repurposer = ContentRepurposer(provider="zai")
twitter_thread = repurposer.repurpose(content, "twitter")
all_platforms = repurposer.repurpose_all(content)
```

## API Reference

### `ContentRepurposer` Class

```python
from repurposer import ContentRepurposer

repurposer = ContentRepurposer(
    api_key=None,      # Optional: API key (or use env vars)
    provider="zai"     # "zai", "openai", "anthropic", or "mock"
)

# Repurpose for single platform
result = repurposer.repurpose(content, "twitter")

# Repurpose for all platforms
results = repurposer.repurpose_all(content)
```

### `repurpose_content()` Function

```python
from repurposer import repurpose_content

results = repurpose_content(
    content="Your content",
    platform="all",    # or specific platform
    provider="mock"
)
```

### Web API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web UI |
| `/api/repurpose` | POST | Repurpose content |
| `/api/platforms` | GET | List supported platforms |

#### POST `/api/repurpose`

```json
{
  "content": "Your long-form content...",
  "platform": "all",
  "provider": "mock"
}
```

Response:
```json
{
  "success": true,
  "results": {
    "twitter": "...",
    "linkedin": "...",
    "instagram": "...",
    "tiktok": "..."
  }
}
```

## Platform Output Formats

### Twitter Thread
- Strong hook in first tweet
- 5-8 tweets total
- Under 280 characters per tweet
- Clear call-to-action at the end

### LinkedIn Post
- Professional, conversational tone
- Short paragraphs (1-2 sentences)
- Actionable insights with bullet points
- Engagement question at the end
- 3-5 hashtags

### Instagram Caption
- Scroll-stopping hook with emojis
- Emojis throughout (but not overdone)
- Line breaks for readability
- Clear call-to-action
- 10-15 relevant hashtags

### TikTok Script
- Pattern interrupt opening
- 60-second runtime (~150-180 words)
- Visual cues in [brackets]
- Structure: Hook → Content → CTA
- Spoken-language style

## Configuration

### Environment Variables

| Variable | Description |
|----------|-------------|
| `ZAI_API_KEY` | Z.ai API key |
| `ZAI_API_URL` | Z.ai API endpoint (optional) |
| `OPENAI_API_KEY` | OpenAI API key |
| `ANTHROPIC_API_KEY` | Anthropic API key |

### Customizing Templates

Edit `templates.py` to customize the prompts for each platform:

```python
# In templates.py
TWITTER_THREAD_TEMPLATE = """Your custom prompt here...
{content}
..."""
```

## Examples

### Example Input

```
The future of work is hybrid. After three years of remote work 
experiments, companies are settling into a new normal. But here's 
what most people get wrong: hybrid isn't just about splitting time 
between home and office. It's about fundamentally rethinking how 
we collaborate...

[Full blog post continues...]
```

### Example Output (Twitter)

```
Tweet 1 (Hook):
Most companies are doing hybrid work wrong.

After studying 50+ teams, here's what actually works 🧵

Tweet 2:
The mistake? Treating hybrid as "some days home, some days office."

Real hybrid is about matching the work to the environment.

Tweet 3:
Deep work → Home
Collaboration → Office
Relationships → Office
Routine tasks → Anywhere

Tweet 4:
The best teams I studied had one rule:
"If you're in office, you're collaborating. No solo work."
...
```

## Project Structure

```
content-repurposer/
├── repurposer.py    # Main logic and LLM integration
├── templates.py     # Platform-specific prompt templates
├── app.py           # Flask web interface
└── README.md        # This file
```

## Tips for Best Results

1. **Input Length**: Provide at least 200 words of content for best results
2. **Clear Structure**: Well-organized input produces better output
3. **Key Insights**: Highlight the main takeaways in your content
4. **Review & Edit**: Always review the generated content before posting
5. **Platform Voice**: Each platform has its own tone—customize templates if needed

## Troubleshooting

### "API key not set"
Set the appropriate environment variable for your chosen provider.

### "Content too short"
Provide at least 50 characters of input content.

### Rate Limiting
If you hit API rate limits, wait a few minutes or switch providers.

## Future Enhancements

- [ ] Batch processing for multiple content pieces
- [ ] Custom tone/style settings
- [ ] Integration with scheduling tools
- [ ] Content calendar generation
- [ ] Analytics and engagement prediction

## License

MIT License - Feel free to use and modify!

---

Built with ❤️ by OpenClaw
