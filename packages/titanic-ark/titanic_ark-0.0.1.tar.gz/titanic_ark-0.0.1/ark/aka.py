import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np


def csv_read(path):
    return pd.read_csv(path)

def plot1(df):
    class_counts = df['Pclass'].value_counts()
    plt.bar(class_counts.index, class_counts.values)
    plt.xlabel('Passenger Class')
    plt.ylabel('Count')
    plt.title('Passenger Class Distribution')
    plt.xticks([1, 2, 3], ['1st Class', '2nd Class', '3rd Class'])
    plt.show()

def plot2(df):
    plt.hist(df['Age'].dropna(), bins=20, edgecolor='k')
    plt.xlabel('Age')
    plt.ylabel('Count')
    plt.title('Age Distribution')
    plt.show()

def plot3(df):
    gender_survival = df.groupby('Sex')['Survived'].mean()
    gender_survival.plot(kind='bar', color=['skyblue', 'lightcoral'])
    plt.xlabel('Gender')
    plt.ylabel('Survival Rate')
    plt.title('Survival Rate by Gender')
    plt.xticks(rotation=0)
    plt.show()

def age_and_fare(df):
    plt.scatter(df[df['Survived'] == 1]['Age'], df[df['Survived'] == 1]['Fare'], label='survive', alpha=0.5, color='green')
    plt.scatter(df[df['Survived'] == 0]['Age'], df[df['Survived'] == 0]['Fare'], label='dead', alpha=0.5, color='red')
    plt.xlabel('Age')
    plt.ylabel('Fare')
    plt.title('Survival by Age and Fare')
    plt.legend()
    plt.show()

def embarked_port(df):
    embarked_counts = df['Embarked'].value_counts()
    plt.pie(embarked_counts, labels=embarked_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title('Distribution of Passengers by Embarked Port')
    plt.axis('equal')
    plt.show()














