import os, pickle
from movielens import *
import numpy as np
from numpy.linalg import pinv
from difflib import SequenceMatcher
from gui import *

item = []
rating = []
user = []

d = Dataset()
d.load_items("data/u.item", item)
d.load_ratings("data/u.base", rating)
d.load_users("data/u.user", user)


n_movies = len(item)
n_users = len(user)
total_movies = d.total_movies

ratings = [ [0 for i in range(total_movies)] for j in range(n_users) ]
n_ratings = [0 for i in range(n_users)]
avg_rating = [0 for i in range(n_users)]
for r in rating:
    uid = r.user_id
    mid = r.item_id
    uid -= 1
    mid -= 1
    ratings[uid][mid] = r.rating
    avg_rating[uid] += r.rating
    n_ratings[uid] += 1
for uid in range(n_users):
    avg_rating[uid] /= float(n_ratings[uid])

# print(len(item))  
# print(avg_rating[0])
# print(a)

def s_year(r1, r2):
     return (300 - abs(r1-r2) ) / 300.0

def s_rating(r1, r2):
    return (10-abs(r1-r2)) / 10.0

def s_list(l1, l2):
    s1 = set(l1)
    s2 = set(l2)
    s = s1.intersection(s2)
    return 1.0 * len(s) / max(len(s1), len(s2))

rows = n_movies * (n_movies-1) /2
# print(rows)
# print(n_users)
cols = 9
x = []
y = []
index = 0

if not os.path.exists("saved_data.p"):
    for i in range(n_movies):
        for j in range(i+1, n_movies):
            similarity_vector = []
            id1 = item[i].id-1
            id2 = item[j].id-1
            mov1 = item[i]
            mov2 = item[j]
            similarity_vector.append(1)
            #similarity_vector.append(s_year(mov1.year, mov2.year))
            similarity_vector.append(s_rating(mov1.rating, mov2.rating))
            similarity_vector.append(s_list(mov1.actor, mov2.actor))
            similarity_vector.append(s_list(mov1.country, mov2.country))
            similarity_vector.append(s_list(mov1.director, mov2.director))
            similarity_vector.append(s_list(mov1.genre, mov2.genre))
            similarity_vector.append(s_list(mov1.lang, mov2.lang))
            similarity_vector.append(s_list(mov1.production, mov2.production))
            x.append(similarity_vector)
            temp = 0
            for k in range(n_users):
                 if ratings[k][id1] >= avg_rating[k] and ratings[k][id2] >= avg_rating[k]:
                    temp += 1
            y.append(temp)
            index += 1
    pickle.dump( (x, y), open( "saved_data.p", "wb" ) )
else:
    (x, y) = pickle.load( open( "saved_data.p", "rb" ) )

# print(len(x))
# print(len(y))
x = np.matrix(x)
y = np.matrix(y)
#i=[[0 for i in range(9)]for j in range(9)]

#pinv=inv(x.T*x+)
w = pinv(x) * y.T

top_n = 1

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def recommendation(mid):
    recoms = []
    for i in range(n_movies):
        if i != mid:
            similarity_vector = []
            id1 = item[i].id-1
            id2 = item[mid].id-1
            mov1 = item[mid]
            mov2 = item[i]
            similarity_vector.append(1)
            #similarity_vector.append(s_year(mov1.year, mov2.year))
            similarity_vector.append(s_rating(mov1.rating, mov2.rating))
            similarity_vector.append(s_list(mov1.actor, mov2.actor))
            similarity_vector.append(s_list(mov1.country, mov2.country))
            similarity_vector.append(s_list(mov1.director, mov2.director))
            similarity_vector.append(s_list(mov1.genre, mov2.genre))
            similarity_vector.append(s_list(mov1.lang, mov2.lang))
            similarity_vector.append(s_list(mov1.production, mov2.production))

            similarity = np.dot(similarity_vector, w)
            recoms.append( (similarity, i) )
    recoms.sort(key = lambda x : x[0], reverse = True)
    recoms = recoms[:top_n]
    return recoms

def find_index(name):
    maxi = -1000
    index = 0
    for i in range(n_movies):
        title = item[i].title
        similarity = similar(title, name)
        if maxi < similarity:
            maxi = similarity
            index = i
    return index

def get_recommendation(name):    
    index = find_index(name)
    # print(index)
    movie = item[index].title
    print("Searching Recommendations for movie: " + movie+"\n")
    url = ''
    indexes = recommendation(index)
    for (similarity, index) in indexes:
        movie = item[index]
        if url == '':
            url = movie.imdb_url
        print(movie.title)
    # print(url)
    # get_poster(url)

# get_recommendation('GoldenEye')
get_recommendation(raw_input('Enter the title of any movie you like:\n'))