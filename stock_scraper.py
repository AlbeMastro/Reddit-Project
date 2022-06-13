import sys, os
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt



class Finance(object):

    """
        Class that scrapes every info about stocks
        We can choose the stock, the period, actions,
        dividends, major holders, splits,
        institutional holders and every datas about the stock chosen

    """

    def __init__(self, stock, start, end, interval):
        self.stock = stock
        self.start = start
        self.end = end
        self.interval = interval


    def get_stock(self):

        """
            Function that returns info about the stock,
            It's possible to choose the start, the end
            and the interval

        """

        try:
            info = yf.Ticker(self.stock)
            info_stock = info.history(start= self.start,
                                      end = self.end,
                                      interval= self.interval,

            )
            df = pd.DataFrame(info_stock)
            df = df.reset_index()
            print(df)
            plot = info_stock.plot(kind= 'line', figsize= (12,12))
            subplot = info_stock.plot(kind='line',figsize=(12,12), subplots=True)
            plt.show()
            df.to_csv('/Users/Alberto/PycharmProjects/00302_mastromarino/info_stocks.csv',
                      columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'], index=False)

        except Exception as e:
            print("Unexpected error")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)






if __name__ == '__main__':

#TODO interval = “1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”, “1h”, “1d”, “5d”, “1wk”, “1mo”, “3mo"

    stock = 'GME'
    start = '2020-12-01'
    end = '2022-06-01'
    interval = '1d'

    Finance(stock, start, end, interval).get_stock()
