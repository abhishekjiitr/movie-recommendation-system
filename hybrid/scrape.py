import requests, json
from movielens import *

item = []
d = Dataset()
d.load_items("data/u.item", item)

def process(arr):
    res = "|".join(arr)

def get_info(id, imdburl, title):
    try:
        title = title.split('(')[0]
        r = requests.get(imdburl) 
        movieid = r.url.split("/")[-2]
        # print(r.url)
        # print(movieid)
        # url = "http://www.omdbapi.com/?i="+movieid
        # print(title)
        url = "http://www.omdbapi.com/?t="+title
        resp = requests.get(url).text
        data = json.loads(resp)
        # print json.dumps(data, indent=4, sort_keys=True)
        # print (data)
        id = str(id)
        actor = data['Actors']
        country = data['Country']
        director = data['Director']
        genre = data['Genre']
        lang = data['Language']
        rating = data['imdbRating']
        year = data['Year']
        production = data['Production'] 
        # print(actor)
        # print(country)
        # print(director)
        # print(genre)
        # print(lang)
        # print(rating)
        # print(year)
        # print(production)
        record = [id, actor, country, director, genre, lang, rating, year, production]
        record = "|".join(record)+"\n"
        print(record)
        with open('scraped_data.txt', 'a') as f:
            f.write(record)
    except:
        return
# for mov in item:
#     url = mov.imdb_url
#     title = mov.title
#     id = mov.id
#     if id > 1182:
#         get_info(id, url, title)

# mov = item[5]
# url = mov.imdb_url
# title = mov.title
# id = mov.id
# get_info(id, url, title)