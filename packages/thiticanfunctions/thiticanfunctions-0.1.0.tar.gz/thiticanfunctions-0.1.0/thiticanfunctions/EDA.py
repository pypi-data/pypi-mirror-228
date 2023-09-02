import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#df = pd.read_csv('titanic_dataset.csv')
#print(df.head())

def csv_read(path):
    return pd.read_csv(path)

def easy_plot(df):
    plt.hist(df.Age.values)
    plt.show()
    
def gender_pie_plot(df):
    fig, ax = plt.subplots()
    df['Sex'].value_counts().plot.pie()
    ax.set_title('Gender of all passenger')
    plt.show()
    
    
def gender_bar_plot(df):
    fig, ax = plt.subplots()
    df['Sex'].value_counts().plot(kind='bar')
    ax.set_title('Gender of all passenger')
    plt.show()
    
    
def survived_plot(df):
    fig, ax = plt.subplots()
    labels = ['Not survived', 'Survived']
    df['Survived'].value_counts().plot.pie(explode=[0,0.1],autopct='%1.1f%%',shadow=True,labels=labels)
    ax.set_title('Number of Survived')
    plt.show()

def class_plot(df):
    f, ax = plt.subplots()
    df['Pclass'].value_counts().plot.bar(color=['#CD7F32','#FFDF00','#D3D3D3'])
    ax.set_title('Number Of Passengers By Pclass')
    ax.set_ylabel('Count')
    plt.show()
    
def class_survived(df):
    print(pd.crosstab(df.Pclass,df.Survived,margins=True))
    
def bar_plot(df,variable):
    """
        input: variable ex: "Sex"
        output: bar plot & value count
    """
    # get feature
    var = df[variable]
    # count number of categorical variable(value/sample)
    varValue = var.value_counts()
    
    # visualize
    plt.figure(figsize = (9,3))
    plt.bar(varValue.index, varValue)
    plt.xticks(varValue.index, varValue.index.values)
    plt.ylabel("Frequency")
    plt.title(variable)
    plt.show()
    print("{}: \n {}".format(variable,varValue))
    
def plot_hist(df,variable):
    plt.figure(figsize = (6,3))
    plt.hist(df[variable], bins = 10)
    plt.xlabel(variable)
    plt.ylabel("Frequency")
    plt.title("{} distribution".format(variable))
    plt.show()