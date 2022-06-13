import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import string
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import SnowballStemmer
nltk.download('stopwords', quiet=True)
stop_words = nltk.corpus.stopwords.words('english')
nltk.download('wordnet',quiet=True)
nltk.download('omw-1.4',quiet=True)
regexp = RegexpTokenizer('\w+')
snowball = SnowballStemmer(language='english')


df = pd.read_csv('/Users/Alberto/PycharmProjects/total_period.csv')

print(f'Inizialmente il dataframe è composto da {df.shape} (righe/colonne)')


class Cleaner:

    """
        Class that cleans the dataframe and returns a dataframe
        without stopwords, special characters, links, emoji
        and converts the text into lowercase to reduce noise
    """

    def __init__(self, dataframe):
        self.dataframe = dataframe



    def cleaning(self):
        """
            Function that removes Nan, special characters,
            links and emoji and numbers. Sorts the dataframe in
            date order, and converts the text into lowercase
        """
        self.dataframe.dropna(inplace=True)
        self.dataframe.sort_values(by='date', ascending=True, inplace=True)
        self.dataframe.replace(regex=True, inplace=True, to_replace=r'(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(https?\S+)',
                               value=r'')
        self.dataframe['selftext'] = self.dataframe['selftext'].str.replace('\d+', '')
        self.dataframe['selftext'] = self.dataframe['selftext'].apply(str.lower)
        self.dataframe['title'] = self.dataframe['title'].str.replace('\d+', '')
        self.dataframe['title'] = self.dataframe['title'].apply(str.lower)



    def cleaning_selftext(self):
        """
            Function removes 'removed' and 'deleted' in the column selftext
            and removes rows that contain duplicates from the dataframe.
            The function also replaces 'ampx200b' with an empty strings,
            reddit uses markdown to style comments and text posts,
            for this after the scraping we can read in the csv file
            'ampx200b' in different rows when a user tries to create
            an extra white space between paragraphs in markdown.
            Function tokenizes the selftext column
            and later deletes stopwords. Removes also
            infrequent words in the columns text_token
            Function lemmatizes text with the snowballstemmer
            removing the plurals and the final suffixes
        """
        self.dataframe.drop(self.dataframe.index[self.dataframe['selftext'] == 'removed'], inplace=True)
        self.dataframe.drop(self.dataframe.index[self.dataframe['selftext'] == 'deleted'], inplace=True)
        self.dataframe.drop_duplicates(subset = ['selftext'],keep=False, inplace=True)
        self.dataframe['selftext'] = self.dataframe['selftext'].str.replace('ampx200b', '')
        self.dataframe['selftext'] = self.dataframe['selftext'].str.replace('ampxb', '')
        self.dataframe['text_token'] = self.dataframe['selftext'].apply(regexp.tokenize)
        self.dataframe['text_token'] = self.dataframe['text_token'].apply(
            lambda x: [item for item in x if item not in stop_words and item not in string.punctuation])
        self.dataframe['text_string'] = self.dataframe['text_token'].apply(
            lambda x: ' '.join([item for item in x if len(item) > 2]))
        self.dataframe['clean_post'] = self.dataframe['text_string'].apply(snowball.stem)
        # self.dataframe['is_equal'] = (self.dataframe['text_string'] == df['text_lemma'])





    def cleaning_title(self):
        """
            Function tokenizes the title column
            and later deletes stopwords. Removes also
            infrequent words in the columns title_token.
            Lemmatizes text with the snowballstemmer
            removing the plurals and the final suffixes
        """
        self.dataframe.drop_duplicates(subset=['title'], keep=False, inplace=True)
        self.dataframe['title_token'] = self.dataframe['title'].apply(regexp.tokenize)
        self.dataframe['title_token'] = self.dataframe['title_token'].apply(
            lambda x: [item for item in x if item not in stop_words and item not in string.punctuation])
        self.dataframe['title_string'] = self.dataframe['title_token'].apply(
            lambda x: ' '.join([item for item in x if len(item) > 2]))
        self.dataframe['clean_title'] = self.dataframe['title_string'].apply(snowball.stem)




    def csv(self):
        """"
            The function returns a csv file that contains a cleaned up dataframe
            We can choose clean_post or clean_title
        """
        self.dataframe['date'] = pd.to_datetime(self.dataframe['date'], format='%Y%m%d %H%M%S')
        self.dataframe['date'] = self.dataframe['date'].dt.date
        # self.dataframe.to_csv('/Users/Alberto/PycharmProjects/00302_mastromarino/total_period_cleaned_post.csv', columns=['date','clean_post'], index=False)
        self.dataframe.to_csv('/Users/Alberto/PycharmProjects/total_period_cleaned_title.csv', columns=['date','clean_title'], index=False)
        print(f'Il dataframe dopo la ripulitura è composto da {df.shape} (righe/colonne)')




if __name__ == '__main__':

    df_clean = Cleaner(df)

    df_clean.cleaning()
    # df_clean.cleaning_selftext()
    df_clean.cleaning_title()
    df_clean.csv()
