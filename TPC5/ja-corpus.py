#!/usr/bin/env python3
import os
import datetime
import re
import json

path = os.getcwd()
if not os.path.exists('/tmp/.newspaper_scraper'):
    origem = os.path.join(path,'newspaper_scraper')
    os.symlink('/tmp/.newspaper_scraper',origem)
    
import newspaper

url = 'https://www.jornaldeangola.ao/ao/'
ja = newspaper.build(url)

print(ja.size(),"articles!")

with open("ja.json","r") as f:
    ja_dic = json.load(f)

i=1
for article in ja.articles:
    if article.url not in map(lambda x: x["url"],ja_dic):
        ar = newspaper.Article(article.url)
        try:
            ar.download()
            ar.parse()
            article_obj = {
                'title': ar.title,
                'url': ar.url,
                'authors': ar.authors,
                'publish_date': ar.publish_date,
                'text': ar.text
            }
            print(f"{i}:",ar.url,"OK")
        except:
            article_obj = {
                'url': ar.url,
                'text': "404"
            }
            print(f"{i}:",ar.url,"404")
        ja_dic.append(article_obj)
        i+=1

with open("ja.json","w") as f:
    json.dump(ja_dic,f,indent=4,default=str)
    