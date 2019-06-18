import random
import collections
import datareader as dr



# =============================================================================
#                 Generate MinHash Signatures
# =============================================================================
# Generates MinHash signatures of length (num_hashes) for all users.

class MinHash:
  def __init__(self, num_hashes, users):
    self.num_hashes = num_hashes
    self.users = users 
    self.data_size = len(users)
    self.highest_ID = dr.get_max_ID(users)
    self.next_prime = 2**31 -1
    self.id_to_idx = {}   
    self.coeffA = None
    self.coeffB = None



  def pick_random_coeffs(self):
    """Generates unique random coefficients for the hash functions."""
    rand_list = []
    for i in range(self.num_hashes):  
      rand_idx = random.randint(0, self.next_prime) 
      while rand_idx in rand_list:
        rand_idx = random.randint(0, self.next_prime)     
      rand_list.append(rand_idx)
    return rand_list


  def setup(self):
    self.coeffA = self.pick_random_coeffs()
    self.coeffB = self.pick_random_coeffs() 


  def get_min_hash_val(self, hash_vals):
    return min(hash_vals)


  def hash_item(self, item, k):
    return ((self.coeffA[k] * item + self.coeffB[k]) % self.next_prime) % self.highest_ID


  def get_minHash_sig(self, userID):  
    """Receives a user and returns its MinHash signature."""   
    item_set = self.users[userID]
    signature = []
    for k in range(self.num_hashes):
      hash_vals = [self.hash_item(item, k) for item in item_set]
      signature.append(self.get_min_hash_val(hash_vals))
    return signature


  def generate_minHash_sigs(self):
    """Generates MinHash signatures for all users."""
    self.setup()
    user_to_sig = collections.OrderedDict()
    for userID in self.users.keys():
      signature = self.get_minHash_sig(userID)
      user_to_sig[userID] = signature
    return user_to_sig


  def calc_est_Jacc(self, sig, other_sig):
    """Receives two signatures and calculates their estimated Jaccard similarity."""
    intersection = 0
    for i in range(len(sig)):
      if sig[i] == other_sig[i]:
        intersection += 1
    union = len(sig)
    if union == 0:
        return 0
    else:
        return intersection/ union


 


    
  



