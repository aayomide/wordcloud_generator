from flask import Flask, render_template, url_for, request
from newscloud import generate_wc


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        news_source = request.form["source"]
        maxWords = request.form["count"]
    
        maxWords = int(maxWords)
        
        image_data = generate_wc(news_source, maxWords)
        
        return render_template('index.html', image=image_data)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)
