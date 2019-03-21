import pandas as pd
npjp = pd.read_csv('./dict/pn_ja.dic', sep=':',encoding='cp932', names=('Tango','Yomi','Hinshi', 'Score'))
print(npjp)