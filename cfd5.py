from movielens import *
from numpy import *
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import mean_squared_error
import sys
import time
import random
from gui import *
    
# Store data in arrays
user = []
item = []
rating = []
rating_test = []

# Load the movie lens dataset into arrays
d = Dataset()
d.load_users("data/u.user", user)
d.load_items("data/u.item", item)
d.load_ratings("data/u.base", rating)
d.load_ratings("data/u.test", rating_test)

n_users = len(user)
n_items = len(item)


mypcs = open("pcs_stored", "rb")
mypcs = np.load(mypcs)

utility = zeros((n_users, n_items))
for r in rating:
    utility[r.user_id-1][r.item_id-1] = r.rating

# Finds the average rating for each user and stores it in the user's object
for i in range(0, n_users):
    user[i].avg_r = mean([ ri for ri in  utility[i] if ri > 0])

def pcs(x, y):
    A = utility[x-1]
    B = utility[y-1]
    avg_x = user[x-1].avg_r
    avg_y = user[y-1].avg_r
    sxy = sx = sy = 0
    for i in range(n_items):
        if A[i] > 0 and B[i] > 0:
            sx += (A[i]-avg_x) ** 2
            sy += (B[i]-avg_y) ** 2
            sxy += (A[i]-avg_x) * (B[i]-avg_y)
    sx = sqrt(sx)
    sy = sqrt(sy)
    return sxy / (sx * sy) if sx*sy != 0 else 0

def guess(user_id, i_id, top_n):
    similar_users = []
    for i in range(n_users):
        if i != user_id-1:
            similarity = mypcs[user_id-1][i-1]
            similar_users.append((similarity, i+1))
    similar_users.sort(reverse = True, key = lambda x : x[0])
    similar_users = similar_users[:top_n]
    rating_sum = 0
    similar_users_count = 0
    for (similarity, index) in similar_users:
        if utility[index-1][i_id-1] > 0:
            rating_sum += utility[index-1][i_id-1] - user[index-1].avg_r
            similar_users_count += 1
    to_add = rating_sum / similar_users_count if similar_users_count > 0 else 0
    final_rating =  user[user_id-1].avg_r + to_add
    # return min(max(1,final_rating), 5)
    return final_rating
top_n = 100


mymovies = range(1, n_users+1)
random.shuffle(mymovies)
print("Get ready to rate some movies:\nRules")
print("Enter a number 1-5 to rate the movie")
print("Enter 0 to skip")
print("Enter anything else to stop\n===============================================\n")

myrating = np.zeros(n_items)
index = 0
while True:
    movie_index = mymovies[index]
    movie_title = item[movie_index].title
    year = item[movie_index].release_date
    if year < 1995:
        index += 1
        continue
    print(movie_title)
    inp = raw_input()
    if len(inp) != 1:
        break
    if inp == "0":
        index+=1
        continue
    if 49 <= ord(inp) <= 53:
        val = int(inp)
        myrating[movie_index-1] = val
    else:
        break        
    index += 1

utility = np.vstack((utility, myrating))
mypcs = np.vstack((mypcs, np.zeros(n_users)))
user.append(User(n_users+1, 20, "M", "pro","12345"))
user[n_users].avg_r = mean([ ri for ri in  utility[n_users] if ri > 0]) if len(myrating) > 0 else 0

for i in range(n_users):
    mypcs[n_users][i] = pcs(n_users+1, i+1)

recoms = []    
for i in range(n_items):
    if utility[n_users][i] == 0:
        utility[n_users][i] = guess(n_users+1, i+1, top_n)
        recoms.append((i+1, utility[n_users][i]))

recoms.sort(reverse = True, key = lambda x : x[1])

num_to_recom = 10
recoms = recoms[:num_to_recom]

print "Here's your recommendations buddy:\n"

place = 0
for i, util in recoms:
    print str(place+1) + ". " + item[i].title + " " + "\n"
    imdb = item[i].imdb_url
    try:
        if i < 2:
            get_poster(imdb, place+1)
    except Exception as e:
        pass
    place += 1
