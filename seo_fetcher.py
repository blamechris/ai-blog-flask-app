import random

def random_metrics(keyword):
    """
    Generate random SEO metrics for a given keyword.
    Args:
        keyword (str): The keyword to generate metrics for.
    Returns:
        dict: A dictionary containing SEO metrics.
    """
    return {
        "keyword": keyword,
        "search_volume": random.randint(100, 10000),
        "competition": round(random.uniform(0.1, 1.0), 2),
        "cpc": round(random.uniform(0.1, 10.0), 2),
        "difficulty": random.randint(1, 100)
    }