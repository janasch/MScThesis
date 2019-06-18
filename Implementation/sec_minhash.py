import random
import math
import minhash as mh


# =============================================================================
#                 Generate signatures by Secure MinHash
# =============================================================================
# Concatenates k minimum hash values, maps them to 1 bit and
# returns signature of length L.


class Sec_MinHash(mh.MinHash):
  def __init__(self, num_hashes, users, L):
    mh.MinHash.__init__(self, num_hashes, users)
    self.L = L # length of signature
    self.rand_ints = None


  def pick_random_ints(self):
    return [random.randint(0, self.next_prime) for x in range(self.num_hashes+1)]

  def setup(self):
    self.rand_ints = [self.pick_random_ints() for x in range(self.L + 1)]
    self.coeffA = [self.pick_random_coeffs() for l in range(self.L)]
    self.coeffB = [self.pick_random_coeffs() for l in range(self.L)]


  def hash_item(self, item, k, l):
    val = ((self.coeffA[l][k] * item + self.coeffB[l][k]) % self.next_prime) % self.highest_ID
    return val


  def hash_universal(self, signature, k, l):
    """Receives signature of minimum hash values and maps them to 1 bit."""
    uni = self.rand_ints[l][self.num_hashes]
    for i in range(len(signature)):
      uni = uni + (signature[i] * self.rand_ints[l][i])
    return uni % self.next_prime % 2


  def get_minHash_sig(self, userID): 
    """Receives a user and returns it final signature."""   
    item_set = self.users[userID]
    uni_signature = []
    for l in range(self.L):
      signature = []
      for k in range(self.num_hashes):
        hash_vals = []
        for item in item_set:
          hashCode = self.hash_item(item, k, l)
          hash_vals.append(hashCode)     
        signature.append(self.get_min_hash_val(hash_vals))
      uni_signature.append(self.hash_universal(signature, k, l))
    return uni_signature
        

  def calc_est_Jacc(self, sig, other_sig):
    """Receives two signatures and returns their estimated Jaccard
    similarity computed by a debiased estimator."""
    collisions = 0
    for i in range(len(sig)):
            collisions += (sig[i] == other_sig[i])
    est_Jacc = 2*(collisions/self.L) -1 
    return est_Jacc

