
import nltk
import utils
import pandas as pd

#https://pythonhealthcare.org/2018/12/14/101-pre-processing-data-tokenization-stemming-and-removal-of-stop-words/

def pull_data(connection="csv",query=False):
    #pull data from postgres

    if connection == "csv":
        #https://pythondata.com/text-analytics-visualization/
        #data = pd.read_csv("test.csv")
        #docs = data['comment']
        #print(data['comment'])
        df = pd.read_csv('test.csv')

        data = []
        for index, row in df.iterrows():
            data.append((row['comment'], row['URL']))
        data_df = pd.DataFrame(data, columns=['description' ,'level'])
        
        return(data_df)
 
    if connection=="postgres":
        # see https://jgardiner.co.uk/blog/read_sql_pandas
        df = pd.DataFrame()
        for chunk in pd.read_sql('select * from table_name', con=conn, chunksize=5000):
            df = df.append(chunk)


        print("not yet written")



if __name__ =="__main__":

    ##import data
    try:
        docs = pull_data()
         
    except:
        print("error")

    #processing
    #to lower case
    docs['description'] = docs['description'].str.lower()

    ##tokenizer
    #print (nltk.word_tokenize(docs['description']))
    df = []
    docs['tokenizer'] = docs['description'].apply(nltk.word_tokenize)


    ##stemming, remove punctutation?

   ##list of interesting things to try:


    words = docs['tokenizer'][1]
    fdist = nltk.FreqDist(words)
    print(fdist.most_common(50))

#https://stackoverflow.com/questions/56000266/counting-the-frequency-of-each-word-in-a-dataframe-column
#https://likegeeks.com/nlp-tutorial-using-python-nltk/
#https://www.nltk.org/book/ch01.html