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
        twitter_handle = request.form["handle"]
        maximum_words = request.form["count"]
    
        maximum_words = int(maximum_words)
        
        image_str = generate_wc(twitter_handle, maximum_words)
        
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
