import numpy as np

pcs_stored = open("pcs_stored", "rb")
mypcs = np.load(pcs_stored)

print mypcs