from flask import Flask, render_template, url_for, request
import sys
import logging
from tweetscloud import generate_wc


app = Flask(__name__)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        twitter_handle = request.form["twitter_handle"]
        
        image_str = generate_wc(twitter_handle)
        
        return render_template('index.html', image=image_str)
    else:
        return render_template('index.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
