from thiticanfunctions.EDA import *

df = csv_read('titanic_dataset.csv')
print(df.head())

#easy_plot(df)

#gender_plot(df)

#gender_plot2(df)

#survived_plot(df)

class_plot(df)

#class_survived(df)

#bar_plot(df,"Embarked")

#plot_hist(df,'Fare')