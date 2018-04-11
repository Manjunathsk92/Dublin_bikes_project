
from dublibikes import app
@app.route('/')
def index():
    return '<h1>Hi</h1>'
