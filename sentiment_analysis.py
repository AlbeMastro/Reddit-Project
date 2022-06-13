from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from nrclex import NRCLex
sid = SentimentIntensityAnalyzer()

# Scelgo quali dei due dataframe utilizzare nell'analisi del sentiment

# clean_df = pd.read_csv('/Users/Alberto/PycharmProjects/total_period_cleaned_post.csv')
clean_df = pd.read_csv('/Users/Alberto/PycharmProjects/total_period_cleaned_title.csv')


class Sentiment(object):



    def __init__(self, dataframe):
        self.dataframe = dataframe



    def get_sentiment_post(self):
        """
            Function that through the use of the nltk library makes a sentiment analysis
            of the columns clean_post obtaining the type of sentiment and the compound.
            The function returns a csv file with sentiment analysis
        """
        self.dataframe['polarity'] = self.dataframe['clean_post'].apply(lambda x: sid.polarity_scores(str(x)))
        self.dataframe = pd.concat([self.dataframe.drop(['polarity'],
                axis=1),self.dataframe['polarity'].apply(pd.Series)], axis=1)
        self.dataframe['sentiment'] = self.dataframe['compound'].apply\
            (lambda x: 'positive' if x > 0 else 'neutral' if x == 0 else 'negative')
        print(self.dataframe.head())
        # self.dataframe.to_csv('only_sentiment_post.csv', index=False)
        # if we want only positive and negative, we can choose to save this csv




    def get_emotions_post(self):
        """
            Function that analyzing the text
            reports the emotions of the post.
            We have eight emotions:
            fear, anger, anticipation, trust, surprise,
            sadness, disgust, joy
        """
        self.dataframe['emotions'] = self.dataframe['clean_post'].apply(lambda x: NRCLex(str(x)).affect_frequencies)
        self.dataframe = pd.concat([self.dataframe.drop(['emotions'], axis=1), self.dataframe['emotions'].apply
        (pd.Series)],axis=1)
        self.dataframe.to_csv('/Users/Alberto/PycharmProjects/sentiment_emotion_total_post.csv',
                              columns=['date', 'clean_post', 'neg', 'neu', 'pos',
                                       'compound', 'sentiment',
                                       'fear', 'anger', 'anticipation', 'trust', 'surprise',
                                       'sadness', 'disgust', 'joy'], index=False)




    def get_sentiment_title(self):
        """
            Function that through the use of the nltk library makes a sentiment analysis
            of the columns clean_title obtaining the type of sentiment and the compound.
            The function returns a csv file with sentiment analysis
        """
        self.dataframe['polarity'] = self.dataframe['clean_title'].apply(lambda x: sid.polarity_scores(str(x)))
        self.dataframe = pd.concat([self.dataframe.drop(['polarity'],
                axis=1),self.dataframe['polarity'].apply(pd.Series)], axis=1)
        self.dataframe['sentiment'] = self.dataframe['compound'].apply\
            (lambda x: 'positive' if x > 0 else 'neutral' if x == 0 else 'negative')
        print(self.dataframe.head())
        # self.dataframe.to_csv('only_sentiment_title.csv', index=False)
        # if we want only positive and negative, we can choose to save this csv





    def get_emotions_title(self):
        """
            Function that analyzing the text
            reports the emotions of the titles.
            We have eight emotions:
            fear, anger, anticipation, trust, surprise,
            sadness, disgust, joy
        """
        self.dataframe['emotions'] = self.dataframe['clean_title'].apply(lambda x: NRCLex(str(x)).affect_frequencies)
        self.dataframe = pd.concat([self.dataframe.drop(['emotions'], axis=1), self.dataframe['emotions'].apply
        (pd.Series)],axis=1)
        self.dataframe.to_csv('/Users/Alberto/PycharmProjects/sentiment_emotion_total_title.csv',
                              columns=['date', 'clean_title', 'neg', 'neu', 'pos',
                                       'compound', 'sentiment',
                                       'fear', 'anger', 'anticipation', 'trust', 'surprise',
                                       'sadness', 'disgust', 'joy'], index=False)






    def high_sentiment(self):
        """
            Returns the post or the title
            with the highest/lowest sentiment
            compound
        """
        print('Post/Titolo con il sentimento più positivo: ')
        print(self.dataframe.loc[self.dataframe['compound'].idxmax()].values)
        print('Post/Titolo con il sentimento più negativo: ')
        print(self.dataframe.loc[self.dataframe['compound'].idxmin()].values)




    def plotting(self):
        """
            Returns a countplot
        """
        sns.countplot(y='sentiment',
                      data=self.dataframe,
                      palette=['#b2d8d8', "#008080", '#db3d13']
                      )

        plt.show()




if __name__ == '__main__':

    df_emotion = Sentiment(clean_df)

    # df_emotion.get_sentiment_post()
    # df_emotion.get_emotions_post()
    df_emotion.get_sentiment_title()
    df_emotion.get_emotions_title()
    # df_emotion.high_sentiment()
    # df_emotion.plotting()
