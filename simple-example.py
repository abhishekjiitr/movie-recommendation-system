"""
This script demonstrates how to design the simplest recommender system based of
Collaborative Filtering. In order to make these predictions, we must first measure
similarity of users or items from the rows and columns of the Utility Matrix.
We will use the Pearson Correlation Similarity Measure to find similar users.

Use this template for Part 1 of your ud741 project.
Project Description is in http://goo.gl/9PGxtR
"""
#!/bin/python
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
rating.append(Rating(1, 1, 4))
rating.append(Rating(1, 4, 1))
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

# The utility matrix stores the rating for each user-item pair in the matrix form.
utility = zeros((n_users, n_items))
for r in rating:
    utility[r.user_id-1][r.item_id-1] = r.rating

"""
Definition of the pcs(x, y) and guess (u, i, top_n) functions.
Complete these after reading the project description.
"""

# Finds the Pearson Correlation Similarity Measure between two users
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

# Guesses the ratings that user with id, user_id, might give to item with id, i_id.
# We will consider the top_n similar users to do this. Use top_n as 3 in this example.
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
print guess(1,2,4)
"""
Displays utility matrix and mean squared error.
This is for answering Q1,2 of Part 1.
"""

# Display the utility matrix as given in Part 1 of your project description
set_printoptions(precision=3)
print  utility

# Finds the average rating for each user and stores it in the user's object
for i in range(0, n_users):
    user[i].avg_r = mean([ ri for ri in  utility[i] if ri > 0])
print user[0].avg_r
n = 3 # Assume top_n users

# Finds all the missing values of the utility matrix
utility_copy = copy(utility)
for i in range(0, n_users):
    for j in range(0, n_items):
        if utility_copy[i][j] == 0:
            utility_copy[i][j] = guess(i+1, j+1, n)

print utility_copy

# Finds the utility values of the particular users in the test set. Refer to Q2
# print "Ann's rating for SW2 should be " + str(guess(1, 5, n))
# print "Carl's rating for HP1 should be " + str(guess(3, 1, n))
# print "Carl's rating for HP2 should be " + str(guess(3, 2, n))
# print "Doug's rating for SW1 should be " + str(guess(4, 4, n))
# print "Doug's rating for SW2 should be " + str(guess(4, 5, n))

guess = array([guess(1, 5, n), guess(3, 1, n), guess(3, 2, n), guess(4, 4, n), guess(4, 5, n)])

### Ratings from the test set
# Ann rates SW2 with 2 stars
# Carl rates HP1 with 2 stars
# Carl rates HP2 with 2 stars
# Doug rates SW1 with 4 stars
# Doug rates SW 2 with 3 stars

test = array([2, 2, 2, 4, 3])

# Finds the mean squared error of the ratings with respect to the test set
print "Mean Squared Error is " + str(mean_squared_error(guess, test))
