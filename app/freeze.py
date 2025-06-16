from flask_frozen import Freezer
from app import app

freezer = Freezer(app)

app.config['FREEZER_DEFAULT_MIMETYPE'] = 'text/html'
app.config['FREEZER_APPEND_SLASH'] = False


@freezer.register_generator
def post():
    import os
    for filename in os.listdir('posts'):
        if filename.endswith('.md'):
            slug = filename.replace('.md', '')
            yield {'slug': slug}

if __name__ == '__main__':
    freezer.freeze()
