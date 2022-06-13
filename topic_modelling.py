import warnings
import pandas as pd
import nltk
import gensim
from gensim import corpora, models
import seaborn as sns
import matplotlib.pyplot as plt
import pyLDAvis.gensim_models
warnings.filterwarnings("ignore")

# df_cleaned = pd.read_csv('/Users/Alberto/PycharmProjects/total_period_cleaned_post.csv')
df_cleaned = pd.read_csv('/Users/Alberto/PycharmProjects/total_period_cleaned_title.csv')

class LDA(object):

    def __init__(self, dataframe):
        self.dataframe = dataframe



    def tokenize_column(self):
        """
            Function reads the dataframe already
            cleaned and tokenize the columns for
            the dictionary
        """

        # self.dataframe['tokens'] = self.dataframe['clean_post'].apply(lambda x: nltk.word_tokenize(str(x)))
        self.dataframe['tokens'] = self.dataframe['clean_title'].apply(lambda x: nltk.word_tokenize(str(x)))




    def topic(self):
        """
            Creates bag of words model using
            gensim and build LDA model and
            visualizes the topics
        """

        dataset = self.dataframe['tokens']
        dic = gensim.corpora.Dictionary(dataset)
        bow_corpus = [dic.doc2bow(x) for x in dataset]
        lda_model = gensim.models.ldamodel.LdaModel(corpus=bow_corpus,
                                                    id2word=dic,
                                                    num_topics=10,
                                                    random_state=10,
                                                    update_every=1,
                                                    chunksize=200,
                                                    passes=5,
                                                    alpha='auto',
                                                    eval_every=1,
                                                    iterations=100,
                                                    per_word_topics=True)

        for idx, topic in lda_model.print_topics():
            print('Topic: {} \nWords: {}'.format(idx, topic))


        vis = pyLDAvis.gensim_models.prepare(lda_model, bow_corpus, dic)
        # pyLDAvis.save_html(vis, 'LDA_Visualization_post.html')
        pyLDAvis.save_html(vis, 'LDA_Visualization_title.html')

        figure = plt.figure(figsize=(30, 30)) #15 30
        for i in range(10):
            df = pd.DataFrame(lda_model.show_topic(i), columns=['term', 'prob']).set_index('term')
            df = df.sort_values('prob')

            plt.subplot(5, 2, i + 1)
            plt.title('topic ' + str(i + 1))
            sns.barplot(x='prob', y=df.index, data=df, label='Cities', palette='Reds_d')
            plt.xlabel('probability')

        plt.show()






if __name__ == '__main__':

    df = df_cleaned
    lda = LDA(df)
    lda.tokenize_column()
    lda.topic()
