from movielens import *
from numpy import *
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import mean_squared_error
import sys
import time

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

# The utility matrix stores the rating for each user-item pair in the matrix form.
utility = zeros((n_users, n_items))
for r in rating:
    utility[r.user_id-1][r.item_id-1] = r.rating

for i in range(0, n_users):
    user[i].avg_r = mean([ri for ri in utility[i] if ri > 0])

print utility

test = np.zeros((n_users, n_items))
for r in rating_test:
    test[r.user_id - 1][r.item_id - 1] = r.rating

# clustering on the basis of movie genre
movie_genre = []
for movie in item:
    movie_genre.append([movie.unknown, movie.action, movie.adventure, movie.animation, movie.childrens, movie.comedy,
                        movie.crime, movie.documentary, movie.drama, movie.fantasy, movie.film_noir, movie.horror,
                        movie.musical, movie.mystery, movie.romance, movie.sci_fi, movie.thriller, movie.war, movie.western])

movie_genre = np.array(movie_genre)
cluster = KMeans(n_clusters=19)
cluster.fit_predict(movie_genre)

utility_clustered = []
for i in range(n_users):
    average = np.zeros(19)
    temp = []
    for m in range(19):
        temp.append([])
    for j in range(n_items):
        if utility[i][j] != 0:
            genre = cluster.labels_[j]-1
            temp[genre].append(utility[i][j])
    for m in range(19):
        if len(temp[m]):
            average[m] = mean(temp[m])
    utility_clustered.append(average)

utility_clustered = np.array(utility_clustered)

def pcs(x, y):
    A = utility_clustered[x-1]
    B = utility_clustered[y-1]
    avg_rx = user[x-1].avg_r
    avg_ry = user[y-1].avg_r
    I =  [(ri, rj) for (ri, rj) in zip(A, B) if ri > 0 and rj > 0]
    if len(I) > 0:
        sxy = sum([(rxi-avg_rx) * (ryi-avg_ry) for (rxi, ryi) in I])
        sx = sum([(rxi-avg_rx) ** 2 for (rxi, ryi) in I])
        sy = sum([(ryi-avg_ry) ** 2 for (rxi, ryi) in I])
        sx = sqrt(sx)
        sy = sqrt(sy)
        if (sx*sy) != 0:
            return sxy/(sx*sy)
    return 0.0

def norm():
    normalize = np.zeros((n_users, 19))
    for i in range(n_users):
        for j in range(19):
            if utility_clustered[i][j] != 0:
                normalize[i][j] = utility_clustered[i][j] - user[i].avg_r
            else:
                normalize[i][j] = float("Inf")
    return normalize

def guess(user_id, i_id, top_n):
    similarity = []
    for i in range(n_users):
        if i+1 != user_id:
            similarity.append((pcs(user_id, i+1)))
    temp = norm()
    temp = np.delete(temp, user_id-1, 0)
    top = [x for (y, x) in sorted(zip(similarity, temp), key = lambda x : x[0], reverse = True)]
    s = c = 0
    for i in range(top_n):
        if top[i][i_id-1] != float('Inf'):
            s += top[i][i_id-1]
            c += 1
    ans = user[user_id-1].avg_r if c == 0 else user[user_id-1].avg_r + s/float(c)
    return max(1, min(5,ans))

n = 150
utility_copy = copy(utility_clustered)
for i in range(0, n_users):
    for j in range(19):
        if utility_copy[i][j] == 0:
            sys.stdout.write("\rGuessing Utility of Element [%d:%d]" % (i+1, j+1))
            sys.stdout.flush()
            time.sleep(0.00005)
            utility_copy[i][j] = guess(i+1, j+1, n)
sys.stdout.write("\n")
# Predict ratings for u.test and find the mean squared error
y_true = []
y_pred = []
f = open('test.txt', 'w')
for i in range(0, n_users):
    for j in range(0, n_items):
        if test[i][j] > 0:
            f.write("%d, %d, %.4f\n" % (i+1, j+1, utility_copy[i][cluster.labels_[j]-1]))
            y_true.append(test[i][j])
            y_pred.append(utility_copy[i][cluster.labels_[j]-1])
f.close()

print "Mean Squared Error: %f" % mean_squared_error(y_true, y_pred)
