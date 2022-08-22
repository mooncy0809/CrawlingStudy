import pandas as pd
from pprint import pprint
df = pd.read_csv('proxy_list_20220808.txt', sep=':',names=['Ip','Port'])

file_list = []
for i in range(len(df['Ip'])):
    tempdict = dict()
    tempdict['ip'] = df['Ip'][i]
    tempdict['port'] = df['Port'][i]
    file_list.append(tempdict)

pprint(file_list)
