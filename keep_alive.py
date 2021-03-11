from flask import Flask
import markdown
import markdown.extensions.fenced_code
from threading import Thread
import random


app = Flask('')

@app.route('/')
def home():
    with open('readme.md') as f:
        text = f.read()
        md_template_string = markdown.markdown(
            text, extensions=["fenced_code"]
        )
        return md_template_string

def run():
    app.run(
        host='0.0.0.0',
        port=random.randint(2000,9000)
    )

def keep_alive():
    '''
    Creates and starts new thread that runs the function run.
    '''
    t = Thread(target=run)
    t.start()