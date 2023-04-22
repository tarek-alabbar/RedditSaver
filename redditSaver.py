import os
import praw
import requests

# Set your Reddit API credentials
client_id = "RycAI5jwR7OsVjhfUyLqvg"
client_secret = "l_WcCKlWDhHvaubmaXbhHi4IyxQ2KQ"
user_agent = "redditdevScraper"
username = "LEEEEEEEEEEEEEEEEROY"
password = "Teadog-099132"

# Initialize the Reddit instance
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
    username=username,
    password=password,
)

def download_content(url, folder, filename):
    response = requests.get(url)
    with open(os.path.join(folder, filename), "wb") as f:
        f.write(response.content)

def save_comment(comment, file, level=0):
    if comment.author is not None:
        author_name = comment.author.name
    else:
        author_name = "[deleted]"

    score = comment.score
    file.write("-" * level + author_name + " (Score: " + str(score) + "): " + comment.body.replace("\n", " ") + "\n")
    for reply in comment.replies:
        save_comment(reply, file, level + 1)

# Create directories for different media types if not exist
folders = {"media": "media", "texts": "texts"}
for folder in folders.values():
    if not os.path.exists(folder):
        os.makedirs(folder)

# Iterate through saved posts
for post in reddit.user.me().saved(limit=None):
    if isinstance(post, praw.models.Submission) and not post.is_self:
        post_id = post.id
        file_extension = None
        folder = None

        if post.url.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".mp4")):
            file_extension = os.path.splitext(post.url)[1]
            folder = folders["media"]

        if file_extension:
            print(f"Downloading post {post_id}...")
            filename = f"{post_id}{file_extension}"
            download_content(post.url, folder, filename)
            
            print("Creating text file...")
            text_filename = f"{post_id}.txt"
            text_filepath = os.path.join(folders["texts"], text_filename)
            with open(text_filepath, "w", encoding="utf-8") as text_file:
                text_file.write(post.title + "\n")
                text_file.write(post.author.name + "\n")
                text_file.write("\n")

                post.comments.replace_more(limit=None)
                for comment in post.comments.list():
                    if not isinstance(comment, praw.models.MoreComments):
                        save_comment(comment, text_file)
            
            print(f"Finished downloading {post_id} and its text file.")