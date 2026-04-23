# importing app from __init__
from app import app

# creating the first page
@app.route('/')
def test():
    return "Hello! This is a test."