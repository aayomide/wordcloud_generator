import config
import requests
import json
from nltk.tokenize import word_tokenize  # to split sentences into words
from nltk.corpus import stopwords  # to get a list of stopwords
from collections import Counter  # to get words-frequency
from wordcloud import WordCloud, STOPWORDS,ImageColorGenerator
from PIL import Image
from io import BytesIO
import base64


# get news
def get_news(news_source):
    NEWS_API_KEY = config.api_key
    # news_source = "bbc-news"
    url = f'https://newsapi.org/v1/articles?source={news_source}&apiKey={NEWS_API_KEY}'
    response = requests.get(url)    # connect to NEWSAPI
    result = response.json()
            
    # create a long sentence of all news
    sentences = ""
    for article in result['articles']:
        sentences = sentences + " " + str(article['description'])

    # split sentences into words
    words = word_tokenize(sentences)

    # remove stopwords from our words list
    stop_words = set(stopwords.words('english'))
    words = [word.lower().strip() for word in words if word not in stop_words and len(word) > 2]

    return words


# generate word cloud
def generate_wc(source, maxWords):
    words = get_news(source)

    # get the words and their frequency
    words_freq = Counter(words)
    
    # generete word cloud of news contents
    wc = WordCloud(max_words = maxWords, 
                    width = 600,
                    height = 400,
                    min_font_size = 4,
                    max_font_size = 150,
                    colormap='Dark2_r', background_color='black').generate_from_frequencies(words_freq) 

    # display word cloud
    image = wc.to_image()
    data = BytesIO()
    image.save(data, format="JPEG")
    encoded_imgage_data = base64.b64encode(data.getvalue())
    
    return encoded_imgage_data.decode('utf-8')