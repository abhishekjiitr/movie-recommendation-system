import numpy as np

mypcs = np.zeros((2,2))
mypcs[0][0] = 1

pcs_stored = open("pcs_stored", "wb")
np.save(pcs_stored, mypcs)