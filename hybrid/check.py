import numpy as np
from numpy.linalg import inv


c = [
    [1, 3],
    [4, -1]
]
c = np.matrix(c)
print(c)
print(inv(c))
