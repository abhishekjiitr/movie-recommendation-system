from movielens import *
from numpy import *

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

def pcs(x, y):
    A = utility[x-1]
    B = utility[y-1]
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

def guess(user_id, i_id, top_n):
    similarity = []
    for i in range(n_users):
        if i+1 != user_id:
            similarity.append((pcs(user_id, i+1), i+1))
    similarity.sort(key = lambda x : x[0], reverse = True)
    r_similar, indexes = zip(*similarity[:top_n])
    rating_top = [ (index, utility[index-1][i_id-1]) for index in indexes if utility[index-1][i_id-1] > 0]
    rating_top_avg = [ v-user[i-1].avg_r for i, v in rating_top ]
    avg_rating_diff = mean(rating_top_avg) if len(rating_top_avg) > 0 else 0
    ans = abs(user[user_id-1].avg_r + avg_rating_diff)
    return ans

n = 50

utility_copy = copy(utility)
for i in range(n_users/1000):
    for j in range(n_items):
        if utility_copy[i][j] == 0:
            utility_copy[i][j] = guess(i, j, n)