from app import db, createApp
from app.models import User, Post

app = createApp()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
