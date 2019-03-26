import pandas as pd
pn_ja = pd.read_csv('./dict/pn_ja.dic', sep=':',encoding='cp932', names=('Tango','Yomi','Hinshi', 'Score'))
print(pn_ja)

word = pn_ja['Tango']
score = pn_ja['Score']

pnja_dic = dict(zip(word, score))

#print(pnja_dic['すもも'])
print('すもも' in pnja_dic)
print('春' in pnja_dic)
