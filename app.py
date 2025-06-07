"""
Flask app for generating SEO-optimized blog posts based on a keyword.
"""

import re
import logging
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime, timedelta

from seo_fetcher import random_metrics
from ai_generator import generate_blog
from scheduler import start_scheduler

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

app = Flask(__name__)

# Rate limiter: 5 requests per minute per IP
limiter = Limiter(get_remote_address, app=app, default_limits=["5 per minute"])

start_scheduler()

def is_valid_keyword(keyword):
    """Validate keyword: must be alphanumeric and may include spaces."""
    return bool(re.match("^[a-zA-Z0-9 ]+$", keyword))

@app.route('/generate', methods=["GET"])
@limiter.limit("5 per minute")
def generate():
    """
    Endpoint to generate a blog post.
    ---
    Parameters:
        keyword (str): The keyword for SEO and content generation.
    Returns:
        JSON response with generated content and SEO metrics.
    """
    keyword = request.args.get("keyword")
    logging.info(f"Request received with keyword: {keyword}")

    if not keyword:
        logging.warning("No keyword provided")
        return jsonify({"error": "Keyword is required"}), 400
    if not is_valid_keyword(keyword):
        logging.warning(f"Invalid keyword format: {keyword}")
        return jsonify({"error": "Invalid keyword format"}), 400

    try:
        seo_metrics = random_metrics(keyword)
        blog_post = generate_blog(keyword, seo_metrics)
        response = {
            "keyword": keyword,
            "seo": seo_metrics,
            "content": blog_post
        }
        logging.info(f"Successfully generated blog for keyword: {keyword}")
        return jsonify(response)
    except Exception as e:
        logging.error(f"Internal error: {e}", exc_info=True)
        return jsonify({"error": "An internal error occurred"}), 500

@app.route('/')
def home():
    """
    Home route that confirms the app is running and shows time until the next scheduled cron job.
    """
    # Assume the cron job runs daily at 23:59 (11:59 PM) server time
    now = datetime.now()
    next_run = now.replace(hour=23, minute=59, second=0, microsecond=0)
    if now >= next_run:
        next_run += timedelta(days=1)
    time_remaining = next_run - now

    return f"""
    <h2>AI Blog Flask App is running!</h2>
    <p>Next scheduled job runs in: <strong id="timer">{str(time_remaining).split('.')[0]}</strong></p>
    <p>Use <code>/generate?keyword=YOUR_KEYWORD</code> to generate a blog post.</p>
    <script>
    let seconds = {int(time_remaining.total_seconds())};
    function updateTimer() {{
        if (seconds > 0) {{
            seconds--;
            let hrs = Math.floor(seconds / 3600);
            let mins = Math.floor((seconds % 3600) / 60);
            let secs = seconds % 60;
            document.getElementById('timer').textContent =
                hrs.toString().padStart(2, '0') + ':' +
                mins.toString().padStart(2, '0') + ':' +
                secs.toString().padStart(2, '0');
        }}
    }}
    setInterval(updateTimer, 1000);
    </script>
    """

if __name__ == '__main__':
    app.run(debug=True)  # Set debug=False in production!