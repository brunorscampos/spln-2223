import json

with open("ja.json","r") as f:
    ja_dic = json.load(f)
    
out = open("ja.txt","w")
 
for article in ja_dic:
    out.write(article['text'])