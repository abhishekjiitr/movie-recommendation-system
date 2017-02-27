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
    return 0
def guess(user_id, i_id, top_n):
    return 0
