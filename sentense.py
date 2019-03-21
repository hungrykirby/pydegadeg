import re

s = '''@tos やっほー！！ 診断して 
    a
 1
#tryswift https://t.co/QYFiLbU6zH'''

s = re.sub(r"(\s*https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+)", "" ,s)
s = re.sub(r"(\s*#\S+\s*)", "", s)
s = re.sub(r"(\s*@\S+\s*)", "", s)
s = re.sub(r"診断して", "", s)
s = re.sub(r"\s+", " ", s)
print(s)