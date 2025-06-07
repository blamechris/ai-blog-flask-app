"""
Flask app for generating SEO-optimized blog posts based on a keyword.
"""

import re
import logging
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

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

if __name__ == '__main__':
    app.run(debug=True)  # Set debug=False in production!