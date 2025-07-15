import os
import datetime
import re
import praw
import pdfkit
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_reddit_instance():
    return praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent="RedditPersonaScript"
    )

def get_user_content(username):
    reddit = get_reddit_instance()
    user = reddit.redditor(username)

    content = []
    try:
        image_url = user.icon_img
    except:
        image_url = "https://via.placeholder.com/200x200.png?text=No+Image"

    for post in user.submissions.new(limit=10):
        content.append(f"[POST] {post.title}\n{post.selftext}")
    for comment in user.comments.new(limit=10):
        content.append(f"[COMMENT] {comment.body}")

    return {
        "text": content,
        "image_url": image_url,
        "name": f"u/{username}"
    }

def build_prompt(user_data):
    joined = "\n\n".join(user_data["text"][:10])
    return f"""
You're an expert in psychological profiling. Based on the Reddit activity below, provide the following:

- Age:
- Occupation:
- Location:
- Archetype:
- Status:

Use short, clean, one-line answers. Begin each line with the label.

{joined}
"""

def generate_persona(user_data):
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content(build_prompt(user_data))
    return response.text

def parse_persona(raw_text, username):
    def extract(label):
        match = re.search(rf"{label}[:：]?\s*(.+)", raw_text, re.IGNORECASE)
        return match.group(1).strip() if match else "Unknown"

    return {
        "name": f"u/{username}",
        "age": extract("Age"),
        "occupation": extract("Occupation"),
        "location": extract("Location"),
        "status": extract("Status"),
        "archetype": extract("Archetype"),
        "quote": "“Reddit is my canvas for expression.”",
        "habits": [
            "Checks Reddit multiple times a day, often during breaks or downtime.",
            "Actively participates in discussions across specific subreddits.",
            "Upvotes meaningful content and insightful comments.",
            "Prefers long-form, detailed replies over short one-liners."
        ],
        "frustrations": [
            "Annoyed by low-effort posts or clickbait titles.",
            "Dislikes misinformation and unverified claims.",
            "Frustrated by toxic or hostile comment sections.",
            "Gets discouraged when thoughtful replies go unnoticed."
        ],
        "goals": [
            "Engage in meaningful and constructive discussions.",
            "Expand knowledge through diverse subreddit communities.",
            "Build a positive reputation as a thoughtful contributor.",
            "Stay updated with trends and insights in niche interests."
        ],
        "traits": [
            "Inquisitive",
            "Thoughtful",
            "Open-minded",
            "Community-oriented"
        ],
        "motivations": {
            "Innovation": 95,
            "Impact": 90,
            "Recognition": 85,
            "Curiosity": 80,
            "Wealth": 75
        }
    }

def render_pdf(data, template_path="persona_template.html"):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_path)
    data["date"] = datetime.date.today().strftime("%B %d, %Y")
    rendered_html = template.render(**data)
    filename = f"user_persona_{data['name'].replace('u/', '')}_{datetime.date.today()}.pdf"
    pdfkit.from_string(rendered_html, filename)
    print(f"[✔] PDF generated: {filename}")

if __name__ == "__main__":
    username = input("Enter Reddit username: ").strip()
    print(f"[✓] Scraping Reddit content for u/{username}...")
    user_data = get_user_content(username)

    print("[✓] Generating persona using Gemini...")
    llm_text = generate_persona(user_data)

    parsed_data = parse_persona(llm_text, username)
    parsed_data["image_url"] = user_data["image_url"]

    render_pdf(parsed_data)


