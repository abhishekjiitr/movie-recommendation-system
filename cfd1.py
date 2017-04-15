from numpy import *
from sklearn.metrics import mean_squared_error

# User class stores the names and average rating for each user
class User:
    def __init__(self, name):
        self.name = name
        self.avg_r = 0.0

# Item class stores the name of each item
class Item:
    def __init__(self, name):
        self.name = name

# Rating class is used to assign ratings
class Rating:
    def __init__(self, user_id, item_id, rating):
        self.user_id = user_id
        self.item_id = item_id
        self.rating = rating

# We store users in an array. The index of the array marks the id of that user
user = []
user.append(User("Ann"))
user.append(User("Bob"))
user.append(User("Carl"))
user.append(User("Doug"))

# Items are also stored in an array. The index of the array marks the id of that item.
item = []
item.append(Item("HP1"))
item.append(Item("HP2"))
item.append(Item("HP3"))
item.append(Item("SW1"))
item.append(Item("SW2"))
item.append(Item("SW3"))

rating = []
rating.append(Rating(1, 1, 5))
rating.append(Rating(1, 4, 5))
rating.append(Rating(2, 1, 5))
rating.append(Rating(2, 2, 5))
rating.append(Rating(2, 3, 4))
rating.append(Rating(3, 4, 4))
rating.append(Rating(3, 5, 5))
rating.append(Rating(4, 2, 3))
rating.append(Rating(4, 6, 3))

n_users = len(user)
n_items = len(item)
n_ratings = len(rating)

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
            similarity = pcs(user_id, i+1)
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
    return min(max(1,final_rating), 5)
    
top_n = 2

print utility

# Finds all the missing values of the utility matrix
utility_copy = copy(utility)
for i in range(0, n_users):
    for j in range(0, n_items):
        if utility_copy[i][j] == 0:
            utility_copy[i][j] = guess(i+1, j+1, top_n)

print utility_copy