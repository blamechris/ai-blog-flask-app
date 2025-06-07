import openai
import os
from dotenv import load_dotenv

# Load environment variables and initialize OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

def generate_blog(keyword: str, seo_metrics: str, aff_link: str = "https://examplesite.com/product1") -> str:
    """
    Generates blog content using OpenAI's GPT-4 model.

    Args:
        keyword (str): The main keyword for the blog.
        seo_metrics (str): SEO metrics or guidelines for optimization.
        aff_link (str): Affiliate link to inject into the content.

    Returns:
        str: Generated blog content, or an error message if generation fails.
    """
    # Dynamic prompt using keyword and SEO metrics
    fakePrompt = f"""
    <html>
        <body>
            <h1>{keyword} Blog</h1>
            <p>This blog aims to optimize for: {seo_metrics}</p>
            <!-- Use {{AFF_LINK_1}} in your response to reference the affiliate link. -->
        </body>
    </html>
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": fakePrompt}],
            temperature=0.8
        )
        # Verify response structure
        if 'choices' in response and len(response['choices']) > 0:
            content = response['choices'][0]['message']['content']
            return content.replace("{{AFF_LINK_1}}", aff_link)
        else:
            raise ValueError("Unexpected response from OpenAI API.")
    except openai.error.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return "An error occurred while generating the blog content."
    except Exception as e:
        print(f"General error: {e}")
        return "An unexpected error occurred."