import random
import math
import datareader as dr
import minhash as mh


# =============================================================================
#                 Generate Signatures based on PrivMin
# =============================================================================
# Generates MinHash signatures using the exponential mechanism to choose
# returned hash values. Shrinks output range based on range parameter as in Yan.

class PrivMin(mh.MinHash):

  def __init__(self, num_hashes, users, eps):
      mh.MinHash.__init__(self, num_hashes, users)
      self.eps = eps
      self.range = (dr.avg_set_size(users) / 1.995) ** (-eps)
      
   
  def shrink_output_range(self, hash_vals):
    """Shrinks output range based on range"""
    hash_vals.sort()
    range_shrink = math.ceil(len(hash_vals)*self.range)
    hash_vals = hash_vals[:range_shrink]
    return hash_vals


  def util(self, hash_vals, r):
    """Returns utility score based on index of hash value"""
    return len(hash_vals) -r


  def apply_exp_mech(self, util, delta_util):
    """Applies exponential mechanism"""
    return math.exp( (self.eps * util) / (2 * self.num_hashes* delta_util))


  def get_exp_sum(self, hash_vals, delta_util):
    """Returns the ormalization term of the exponential mechanism."""
    exp_sum = 0
    for r in range(len(hash_vals)):
      exp_sum += self.apply_exp_mech(self.util(hash_vals, r), delta_util)
    return exp_sum 


  def is_chosen(self, exp_sum, util, delta_util):
    """Returns true if hash value is chosen."""
    proportional_prob = self.apply_exp_mech(util, delta_util)
    prob = proportional_prob / exp_sum
    rand = random.random()
    return rand < prob


  def get_return_val(self, hash_vals, exp_sum, delta_util):
    """Chooses and returns a hash value based on exponential mechanism."""
    hash_returned = False
    while not hash_returned:
      for r, val in enumerate(hash_vals):
        if self.is_chosen(exp_sum, self.util(hash_vals,r), delta_util):
          hash_returned = True
          return val


  def get_min_hash_val(self, hash_vals):
    """Receives a list of possible hash values and selects one based on probability function
    Not necessarily minimum hash value."""
      
    hash_vals = self.shrink_output_range(hash_vals)
    delta_util = len(hash_vals)  # sensitivity is bound by num of hash values
    exp_sum = self.get_exp_sum(hash_vals, delta_util)
    return self.get_return_val(hash_vals, exp_sum, delta_util)

  
            