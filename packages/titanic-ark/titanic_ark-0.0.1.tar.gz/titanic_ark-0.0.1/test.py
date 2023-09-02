from ark import aka
df=aka.csv_read("titanic_dataset.csv")
print(df.head())
#aka.age_plot(df)
#

#aka.age_and_fare(df)
aka.embarked_port(df)



