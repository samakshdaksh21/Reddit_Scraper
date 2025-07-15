import praw
import os
from dotenv import load_dotenv

load_dotenv()

def get_reddit_instance():
    return praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent="userPersonaScript"
    )

def get_user_content(username, limit=20):
    reddit = get_reddit_instance()
    user = reddit.redditor(username)

    posts = []
    comments = []

    for submission in user.submissions.new(limit=limit):
        posts.append(f"[POST] Title: {submission.title}\nContent: {submission.selftext}\n")

    for comment in user.comments.new(limit=limit):
        comments.append(f"[COMMENT] {comment.body}\n")

    return {
        "profile_image_url": user.icon_img,  # 👈 include profile picture
        "posts": posts,
        "comments": comments
    }
