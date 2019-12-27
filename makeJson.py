import pandas as pd

#Database#
#df = pd.read_csv("data/dataSampleDefs.csv", sep=",", index_col="id")
#df.to_json("data/dataSample.json", orient='index', force_ascii=True)

#Example Sentences#
df = pd.read_csv("data/exampleSentences.csv", sep=",")
df.to_json("data/exampleSentences.json", orient='index', force_ascii=True)