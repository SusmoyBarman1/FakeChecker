import requests
from bs4 import BeautifulSoup
import os

class DailyStarRss():
    url = "https://www.thedailystar.net/top-news/rss.xml"

    resp = requests.get(url)    

    soup = BeautifulSoup(resp.content, features="xml")
    items = soup.findAll('item')

    news_items = []
    for item in items:
        news_item = {}
        news_item['title'] = item.title.text
        news_item['description'] = item.description.text
        news_item['link'] = item.link.text
        news_item['image'] = item.content['url']
        news_items.append(news_item)
        
    BASE = os.path.dirname(os.path.abspath(__file__))
    file1 = open(os.path.join(BASE.replace("utils", "lorem"), "dailyStar_top_news.txt"), "w")
    # # file1 = open("dailyStar_top_news.txt","w")

    for i in range(len(news_items)):
        #print('Titles: ',news_items[i]['title'])
        #print('Description: ',news_items[i]['description'],'\n')
        title = news_items[i]['title']+'\n'
        #print(title)
        file1.writelines(title) 
        description = news_items[i]['description']+'\n'
        #print(description)
        file1.writelines(description) 

    file1.close()