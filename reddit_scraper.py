import pandas as pd
import datetime as dt
from psaw import PushshiftAPI
import sys, os
import logging

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger = logging.getLogger('psaw')
logger.setLevel(logging.INFO)
logger.addHandler(handler)

scraper = PushshiftAPI()


class Reddit_Scraper(object):

    """
        Class that scrapes a specified subreddit in different ways:
        1) historical posts with datetime
        3) query research

    """

    def __init__(self,before, after):
        self.before = before
        self.after = after

        print(f'Si inizia a raccogliere dati :-) Attendi...')




    def historical_posts(self,subreddit, limit):
        """
            Functions that through psaw API scrapes posts from a specified
            subreddit, choosing the start and the end and the limits
        """
        self.subreddit = subreddit
        self.limit = limit
        try:
            posts = scraper.search_submissions(
                subreddit= self.subreddit,
                before= after,
                after= before,
                limit= self.limit
            )
            df = pd.DataFrame([i.d_ for i in posts])
            df['date'] = pd.to_datetime(df['created'], unit='s')
            df = df[['author', 'date', 'title', 'selftext', 'score', 'num_comments']]
            print(df.head())
            print(df.shape)
            # df.to_csv('/Users/Alberto/PycharmProjects/00302_mastromarino/reddit_post.csv', index= False)

        except Exception as e:
            print("Unexpected error")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)




    def query_posts(self, q, score):
        """
            Functions that through psaw API scrapes posts from a specified
            subreddit, choosing a keyword and the number of upvotes
            We can use in this way:
            1) query, after, before
            2) query, score
        """
        self.q = q
        self.score = score
        try:
            query_posts = scraper.search_submissions(
                q = self.q,
                before=after,
                after=before,
                score = self.score
            )
            df = pd.DataFrame([i.d_ for i in query_posts])
            df['date'] = pd.to_datetime(df['created'], unit='s')
            df = df[['author', 'date', 'title', 'selftext', 'score', 'num_comments']]
            print(df.head())
            print(df.shape)
            df.to_csv('/Users/Alberto/PycharmProjects/00302_mastromarino/query_post.csv', index=False)

        except Exception as e:
            print("Unexpected error")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)




if __name__ == '__main__':
    # TODO To get historical posts

    subreddit = 'WallStreetBets'
    limit = 300
    before = int(dt.datetime(2022, 5, 1).timestamp())
    after = int(dt.datetime(2022, 6, 1).timestamp())

    Reddit_Scraper(before, after).historical_posts(subreddit, limit)

    #TODO To get query posts

    # q = "GME"
    # score = ">10"
    # before = int(dt.datetime(2022, 1, 1).timestamp())
    # after = int(dt.datetime(2022, 5, 31).timestamp())
    #
    # Reddit_Scraper(before, after).query_posts(q,score)

