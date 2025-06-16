from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)

# Folder to store blog posts
POSTS_DIR = 'posts'
os.makedirs(POSTS_DIR, exist_ok=True)

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
@app.route('/post/<slug>')
def post(slug):
    filepath = os.path.join(POSTS_DIR, slug + '.md')
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

    return render_template('post.html', title=post_title, date=post_date, content=content)



# About page
@app.route('/about')
def about():
    with open('about.txt', 'r') as file:
        about_text = file.read()
    return render_template('about.html', content=about_text)

if __name__ == '__main__':
    app.run(debug=True)

from flask_frozen import Freezer

freezer = Freezer(app)
@freezer.register_generator
def post():
    import os
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith(".md"):
            yield {'slug': filename[:-3]} 