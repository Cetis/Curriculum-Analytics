
import nltk
import utils
import pandas as pd
import psycopg2
from nltk.corpus import stopwords
from itertools import chain 
import matplotlib.pyplot as plt
from collections import Counter

#https://pythonhealthcare.org/2018/12/14/101-pre-processing-data-tokenization-stemming-and-removal-of-stop-words/

def pull_data(connection="csv",query=False):
    #pull data from postgres

    if connection == "csv":
        #https://pythondata.com/text-analytics-visualization/
        df = pd.read_csv('test.csv')

        data = []
        for index, row in df.iterrows():
            data.append((row['comment'], row['URL']))
        data_df = pd.DataFrame(data, columns=['description' ,'level'])
        
        return(data_df)
 
    if connection=="postgres":
        # see https://jgardiner.co.uk/blog/read_sql_pandas
        df = pd.DataFrame()
        con = psycopg2.connect(database="postgres", user="postgres", password="gladdylight", host="127.0.0.1", port="5432")
        cur = con.cursor()
 
        for chunk in pd.read_sql('select * from module', con=con, chunksize=5000):
            data_df = df.append(chunk)

        return(data_df)

def identify_tokens(row):
    #https://pythonhealthcare.org/2018/12/14/101-pre-processing-data-tokenization-stemming-and-removal-of-stop-words/
    stop_words=set(stopwords.words("english"))
    description = row['description']
    tokens = nltk.word_tokenize(description)
    token_words = [w for w in tokens if w.isalpha()]

    return token_words

def it_stop_words(row):
    ##too lazy to look up args to .apply
    stop_words=set(stopwords.words("english"))
    description = row['description']
    tokens = nltk.word_tokenize(description)
    token_words = [w for w in tokens if w.isalpha() and w not in stop_words]
    return token_words

def find_ngrams(input_list, n):
    return list(zip(*[input_list[i:] for i in range(n)]))
    


if __name__ =="__main__":

    ##import data
    try:
        docs = pull_data(connection="postgres")
         
    except:
        print("error")

    #processing, make lower case,  create a column that has tokenizer, removing punctutation (no stemming yet).
    docs['description'] = docs['description'].str.lower()
    docs['description_tokenizer'] = docs.apply(identify_tokens, axis=1)
    docs['description_tokenizer_stopwords'] = docs.apply(it_stop_words, axis=1)

    #get ngrams in columns
    docs['2grams'] = docs['description'].map(lambda x: find_ngrams(x.split(" "), 2))
    docs['3grams'] = docs['description'].map(lambda x: find_ngrams(x.split(" "), 3))
    docs['4grams'] = docs['description'].map(lambda x: find_ngrams(x.split(" "), 4))
    docs['5grams'] = docs['description'].map(lambda x: find_ngrams(x.split(" "), 5))

    #example of ngram counting
    grams2 = docs['2grams'].tolist()
    grams2 = list(chain(*grams2))
    grams2 = [(x.lower(), y.lower()) for x,y in grams2]

    ##give me a full frequency dist and plot them
    all_stopwords  = docs['description_tokenizer_stopwords'].tolist()
    fdist = nltk.FreqDist(list(chain.from_iterable(all_stopwords)))
    #print(fdist.most_common(30))
    #fdist.plot(30,cumulative=False)
    plt.show()

    #example of how to do get frequencies for level 6 docs
    #docs = docs.loc[docs['level'] == '6']
    docs4.to_csv (r'export_dataframe.csv', index = None, header=True)
    all_stopwords  = docs['description_tokenizer_stopwords'].tolist()
    fdist = nltk.FreqDist(list(chain.from_iterable(all_stopwords)))
    #print(fdist.most_common(50))
    fdist.plot(30,cumulative=False)
    #plt.show()

   
    docs.to_csv (r'additional.csv', index = None, header=True)



#https://stackoverflow.com/questions/56000266/counting-the-frequency-of-each-word-in-a-dataframe-column
#https://likegeeks.com/nlp-tutorial-using-python-nltk/
#https://www.nltk.org/book/ch01.html