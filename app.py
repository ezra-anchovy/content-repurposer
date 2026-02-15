"""
Content Repurposer - Simple Web Interface
A Flask-based web app for easy content repurposing.
"""

from flask import Flask, render_template, request, jsonify
from repurposer import ContentRepurposer, get_all_platforms, PLATFORMS

app = Flask(__name__)


@app.route("/")
def index():
    """Render the main page."""
    return render_template("index.html", platforms=PLATFORMS)


@app.route("/api/repurpose", methods=["POST"])
def api_repurpose():
    """API endpoint to repurpose content."""
    data = request.get_json()
    
    if not data or "content" not in data:
        return jsonify({"error": "Missing 'content' field"}), 400
    
    content = data["content"]
    platform = data.get("platform", "all")
    provider = data.get("provider", "mock")
    
    if len(content.strip()) < 50:
        return jsonify({"error": "Content too short. Please provide at least 50 characters."}), 400
    
    try:
        repurposer = ContentRepurposer(provider=provider)
        
        if platform == "all":
            results = repurposer.repurpose_all(content)
        else:
            results = {platform: repurposer.repurpose(content, platform)}
        
        return jsonify({
            "success": True,
            "results": results
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/platforms", methods=["GET"])
def api_platforms():
    """Get list of supported platforms."""
    return jsonify({
        "platforms": [
            {
                "id": pid,
                "name": p["name"],
                "description": p["description"],
                "max_length": p["max_length"]
            }
            for pid, p in PLATFORMS.items()
        ]
    })


# HTML template (inline for simplicity)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Content Repurposer</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        
        header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        
        header p {
            opacity: 0.9;
            font-size: 1.1rem;
        }
        
        .main-card {
            background: white;
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.2);
        }
        
        .input-section {
            margin-bottom: 25px;
        }
        
        .input-section label {
            display: block;
            font-weight: 600;
            margin-bottom: 8px;
            color: #333;
        }
        
        textarea {
            width: 100%;
            min-height: 200px;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 15px;
            font-family: inherit;
            resize: vertical;
            transition: border-color 0.3s;
        }
        
        textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .options-row {
            display: flex;
            gap: 20px;
            margin-bottom: 25px;
            flex-wrap: wrap;
        }
        
        .option-group {
            flex: 1;
            min-width: 200px;
        }
        
        .option-group label {
            display: block;
            font-weight: 600;
            margin-bottom: 8px;
            color: #333;
        }
        
        select, button {
            width: 100%;
            padding: 12px 15px;
            border-radius: 8px;
            font-size: 15px;
            font-family: inherit;
        }
        
        select {
            border: 2px solid #e0e0e0;
            background: white;
            cursor: pointer;
        }
        
        select:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        
        .btn-primary:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .results {
            margin-top: 30px;
        }
        
        .results h2 {
            margin-bottom: 20px;
            color: #333;
        }
        
        .platform-result {
            background: #f8f9fa;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }
        
        .platform-result h3 {
            color: #667eea;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .platform-result .content {
            background: white;
            padding: 15px;
            border-radius: 8px;
            white-space: pre-wrap;
            font-size: 14px;
            line-height: 1.6;
            max-height: 400px;
            overflow-y: auto;
        }
        
        .copy-btn {
            background: #e0e0e0;
            border: none;
            padding: 8px 15px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 13px;
            margin-top: 10px;
            transition: background 0.2s;
        }
        
        .copy-btn:hover {
            background: #d0d0d0;
        }
        
        .copy-btn.copied {
            background: #4caf50;
            color: white;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        
        .loading::after {
            content: '';
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 2px solid #667eea;
            border-top-color: transparent;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-left: 10px;
            vertical-align: middle;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .error {
            background: #ffebee;
            color: #c62828;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
        }
        
        footer {
            text-align: center;
            color: white;
            opacity: 0.8;
            margin-top: 30px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📝 Content Repurposer</h1>
            <p>Transform one piece of content into platform-optimized posts</p>
        </header>
        
        <div class="main-card">
            <div class="input-section">
                <label for="content">Your Long-Form Content</label>
                <textarea id="content" placeholder="Paste your blog post, newsletter, video transcript, or any long-form content here...

Minimum 50 characters required."></textarea>
            </div>
            
            <div class="options-row">
                <div class="option-group">
                    <label for="platform">Target Platform</label>
                    <select id="platform">
                        <option value="all">All Platforms</option>
                        {% for pid, p in platforms.items() %}
                        <option value="{{ pid }}">{{ p.name }}</option>
                        {% endfor %}
                    </select>
                </div>
                
                <div class="option-group">
                    <label for="provider">LLM Provider</label>
                    <select id="provider">
                        <option value="mock">Mock (Demo)</option>
                        <option value="zai">Z.ai GLM-5</option>
                        <option value="openai">OpenAI GPT-4</option>
                        <option value="anthropic">Anthropic Claude</option>
                    </select>
                </div>
            </div>
            
            <button class="btn-primary" id="repurpose-btn" onclick="repurposeContent()">
                ✨ Repurpose Content
            </button>
            
            <div id="results" class="results"></div>
        </div>
        
        <footer>
            Built with ❤️ by OpenClaw | Supports Twitter, LinkedIn, Instagram, TikTok
        </footer>
    </div>
    
    <script>
        async function repurposeContent() {
            const content = document.getElementById('content').value;
            const platform = document.getElementById('platform').value;
            const provider = document.getElementById('provider').value;
            const btn = document.getElementById('repurpose-btn');
            const resultsDiv = document.getElementById('results');
            
            if (content.trim().length < 50) {
                resultsDiv.innerHTML = '<div class="error">Please enter at least 50 characters of content.</div>';
                return;
            }
            
            btn.disabled = true;
            btn.textContent = '⏳ Processing...';
            resultsDiv.innerHTML = '<div class="loading">Repurposing your content</div>';
            
            try {
                const response = await fetch('/api/repurpose', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ content, platform, provider })
                });
                
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.error || 'Failed to repurpose content');
                }
                
                displayResults(data.results);
                
            } catch (error) {
                resultsDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`;
            } finally {
                btn.disabled = false;
                btn.textContent = '✨ Repurpose Content';
            }
        }
        
        function displayResults(results) {
            const resultsDiv = document.getElementById('results');
            
            let html = '<h2>🎉 Repurposed Content</h2>';
            
            const platformEmojis = {
                twitter: '🐦',
                linkedin: '💼',
                instagram: '📸',
                tiktok: '🎵'
            };
            
            for (const [platform, content] of Object.entries(results)) {
                html += `
                    <div class="platform-result">
                        <h3>${platformEmojis[platform] || '📄'} ${platform.charAt(0).toUpperCase() + platform.slice(1)}</h3>
                        <div class="content">${escapeHtml(content)}</div>
                        <button class="copy-btn" onclick="copyToClipboard(this, '${platform}')">📋 Copy to Clipboard</button>
                    </div>
                `;
            }
            
            resultsDiv.innerHTML = html;
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        async function copyToClipboard(btn, platform) {
            const content = btn.previousElementSibling.textContent;
            await navigator.clipboard.writeText(content);
            
            btn.textContent = '✅ Copied!';
            btn.classList.add('copied');
            
            setTimeout(() => {
                btn.textContent = '📋 Copy to Clipboard';
                btn.classList.remove('copied');
            }, 2000);
        }
    </script>
</body>
</html>
"""


@app.route("/templates/index.html")
def get_template():
    """Serve the inline template."""
    return HTML_TEMPLATE


# Override the index route to use inline template
@app.route("/")
def index_inline():
    """Render the main page with inline template."""
    return HTML_TEMPLATE


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Content Repurposer Web App")
    parser.add_argument("--port", type=int, default=5000, help="Port to run on")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    print(f"\n🚀 Content Repurposer starting at http://{args.host}:{args.port}")
    print("Press Ctrl+C to stop\n")
    
    app.run(host=args.host, port=args.port, debug=args.debug)
