from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os
import markdown

app = Flask(__name__)

# Folder to store blog posts
POSTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'posts'))


# Homepage: list blog post titles
@app.route('/')
def index():
    posts = []

    for filename in os.listdir(POSTS_DIR):
        if filename.endswith('.md'):
            filepath = os.path.join(POSTS_DIR, filename)
            with open(filepath, 'r') as f:
                lines = f.readlines()

            if len(lines) < 3:
                continue

            title_line = lines[0].strip()
            date_line = lines[1].strip()

            if not title_line.startswith("Title:") or not date_line.startswith("Date:"):
                continue

            title = title_line.replace("Title:", "").strip()
            date_str = date_line.replace("Date:", "").strip()

            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                continue

            posts.append({
                'title': title,
                'date': date_obj.strftime('%b %d, %Y'),
                'filename': filename[:-3]
            })

    # Sort newest first
    posts.sort(key=lambda x: x['date'], reverse=False)
    return render_template('index.html', posts=posts)



# View a single post
@app.route('/posts/<slug>')
def post(slug):
    filepath = os.path.join(POSTS_DIR, slug + '.md')

    print(os.listdir(POSTS_DIR))
    print(filepath)

    if not os.path.exists(filepath):
        return "Post not found", 404

    with open(filepath, 'r') as f:
        lines = f.readlines()

    if len(lines) < 3:
        return "Post is missing required metadata", 500

    title_line = lines[0].strip()
    date_line = lines[1].strip()
    content = ''.join(lines[3:])

    if not title_line.startswith("Title:") or not date_line.startswith("Date:"):
        return "Post metadata malformed", 500

    post_title = title_line.replace("Title:", "").strip()
    post_date = date_line.replace("Date:", "").strip()

    content_html = markdown.markdown(content, extensions=['fenced_code', 'codehilite'])

    return render_template('post.html', title=post_title, date=post_date, content=content_html)



# About page
@app.route('/about')
def about():
    return render_template('about.html')

