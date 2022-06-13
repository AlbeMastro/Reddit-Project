import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split



df1 = pd.read_csv('sentiment_emotion_total_title.csv',parse_dates=['date'])
df1['date'] = df1['date'].astype('int')

df2 = pd.read_csv('total_stocks.csv', parse_dates=['Date'])
df2['Date'] = df2['Date'].astype('int')


df1 = df1[['date', 'compound', 'sentiment', 'neg', 'neu', 'pos']]
df1 = df1.rename(columns={'date': 'Date'})
df1 = df1.groupby(['Date']).mean()


df2 = df2[['Date', 'Open', 'Close', 'Volume']]
df2['Closing_Difference'] = df2['Close'] - df2['Open']
df2['Trend'] = np.where(df2['Closing_Difference'] >= 0,  1, 0)


merge = df1.merge(df2, how='inner', on='Date')
# merge.to_csv('merge_post.csv',index=False)
merge.to_csv('merge_title.csv',index=False)


#Create the feature data set
X = merge
X = np.array(X.drop(['Trend'], 1))

#Create the target data set
y = np.array(merge['Trend'])

#Split the data into 80% training and 20% testing data sets
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state = 0)

model = LinearDiscriminantAnalysis().fit(x_train, y_train)

#Get the models predictions/classification
predictions = model.predict(x_test)
print(predictions)

#Show the models metrics
print(classification_report(y_test, predictions))
