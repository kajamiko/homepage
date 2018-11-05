import os
from socket import gethostname
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")
    
    
    
if __name__ == '__main__':
    if 'liveconsole' not in gethostname():
        app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)