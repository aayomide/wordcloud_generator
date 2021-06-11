import snscrape.modules.twitter as sntwitter
import pandas as pd
import re
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk import word_tokenize
from nltk.corpus import stopwords
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
from PIL import Image
from io import BytesIO
import base64

 
def generate_wc(username):
    stopwords = set(STOPWORDS)
    wc = WordCloud(max_words = 300, 
    width = 1600,
    height = 590,
    min_font_size = 4,
    max_font_size = 300,
    colormap='Dark2_r', background_color='white').generate(get_tweets(username))

    image = wc.to_image()
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    
    return img_str.decode('utf-8') 


def get_tweets(username):
    maxTweets = 1000  
    search_input = 'from:{}'.format(username)   
        
    # Creating list to append tweet data to
    tweets_list = []
    
    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(search_input).get_items()):
       if i > maxTweets:
         break
       tweets_list.append([tweet.content])

    tweets_df = pd.DataFrame(tweets_list, columns=['tweet'])


    def clean_tweets(message):
        stop_word = stopwords.words('english')
        message = re.sub('(http\S+)|(#\w+)|(@\w+)|([^a-zA-Z])', ' ', message)        # remove links, hashtags, mentions, non-words

        return ' '.join([word.lower().strip() for word in nltk.word_tokenize(message) if not word in stop_word and len(word)>2])    # remove stop words    

    tweets_df['tweet'] = tweets_df.content.apply(lambda w: clean_tweets(w))

    tweets_corpus = ' '.join(tweet for tweet in tweets_df['tweet'])

    return tweets_corpus
