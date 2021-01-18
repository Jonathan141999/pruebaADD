import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient


if __name__ == '__main__':
    db_client = MongoClient('mongodb://localhost:27017')
    prueba = db_client.prueba
    my_posts = prueba.posts


    response = requests.get("https://www.elsevier.com/es-es/connect")
    soup = BeautifulSoup(response.content, "lxml")

    post_titles = soup.find_all("a", class_="tile-image-anchor")

    extracted = []
    for post_title in post_titles:
        extracted.append({
            'title' : post_title['title'],
            'link'  : post_title['href']
        })

   
    for post in extracted:
        if db_client.prueba.my_posts.find_one({'link': post['link']}) is None:
            print("Found a new listing at the following url: ", post['link'])
            db_client.prueba.my_posts.insert(post)