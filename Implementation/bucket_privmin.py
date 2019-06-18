import math
import random
import datareader as dr
import privmin as pm

# =============================================================================
#                 Generate Signatures with Bucket PrivMin
# =============================================================================
# Maps all possible hash values to buckets. Returns the bucket containing
# possibly the minimum hash value based on a randomizing algorithm.
# Uses by default the generalized random response, but can be set to use
# the exponential mechanism inherited from the PrivMin.

class Bucket_PrivMin(pm.PrivMin):
  def __init__(self, num_hashes, users, eps, num_buckets, exp_mech):
      pm.PrivMin.__init__(self, num_hashes, users, eps / num_hashes)
      self.universe = dr.get_max_ID(users)
      self.range = int(num_buckets)
      self.buckets = self.shrink_output_range()
      self.val_to_buck = self.make_buck_idx()
      self.exp_mech = exp_mech


  def get_min_hash_val(self, hash_vals):
    """ Returns bucket containing possibly the minimum hash value.
    Uses either RR or the Exponential Mechanism based on the value of the boolean exp_mech
    """
    min_val = min(hash_vals)
    min_buck = self.val_to_buck[min_val]   

    if self.exp_mech:
      util = self.util(hash_vals, min_val)
      delta_util = 1
      prob_sum = self.get_exp_sum(hash_vals, delta_util)
      prob = self.apply_exp_mech(util, delta_util)
    else:
      prob_sum = 1
      prob = self.apply_RR()
    if self.is_chosen(prob, prob_sum):
      return min_buck
    else:
      return self.random_bucket(min_buck)


  def shrink_output_range(self):
    """Maps all possible hash values to the number of buckets
    defined by the range.
    """
    all_poss_hash_vals = [x for x in range(self.highest_ID +1)]
    buckets = [[] for _ in range(self.range)]
    random.shuffle(all_poss_hash_vals)
    for idx, val in enumerate(all_poss_hash_vals):
      buckets[idx % self.range].append(val)
    return buckets


  def make_buck_idx(self):
    """Returns a dictionary mapping each value to its respective bucket."""
    val_to_buck = {}
    for i in range(len(self.buckets)):
      for val in self.buckets[i]:
        val_to_buck[val] = i
    return val_to_buck


  def is_chosen(self, prob, prob_sum):
    rand = random.random() 
    return rand < (prob / prob_sum)


  def apply_RR(self):
    """Computes the output probability of a hash value based on generalized random response.
    Uses the number of buckets (range) and the privacy parameter eps.
    """
    prob = math.exp(self.eps) / (math.exp(self.eps) + (self.range -1))
    return prob
  


  def get_exp_sum(self, hash_vals, delta_util):
    """Returns the sum of ouput probabilites of each item based on the exponential mechanism."""
    exp_sum = 0
    min_buck = self.val_to_buck[min(hash_vals)]
    for bucket in self.buckets:
      util = (bucket == min_buck)
      exp_sum += self.apply_exp_mech(util, delta_util)
    return exp_sum


  def random_bucket(self, min_buck):
    """Returns a random bucket."""
    buck = random.randint(0, self.range)
    while buck == min_buck:
      buck = random.randint(0, self.range)
    return buck

  def util(self, hash_vals, val):
    """Returns the utility score of a hash value based on a binary utility function."""
    min_val = min(hash_vals)
    return val == min_val
  

  def apply_exp_mech(self, util, delta_util):
    """Computes the output probability of a hash value based on the exponential mechanism.
    Uses the number of buckets (range) and the privacy parameter eps.
    """
    return math.exp( (self.eps * util) / (2 * delta_util))


  def calc_est_Jacc(self, sig, other_sig):
    """Returns the estimated Jaccard similarity of two signatures using a
    debiased estimator."""
    collisions = 0
    for i in range(len(sig)):
            collisions += (sig[i] == other_sig[i])
    
    col_prob = math.exp(self.eps)/((self.range-1) + math.exp(self.eps))
    non_col_prob = 1 - col_prob
    b = self.range
    est_Jacc = ((b* collisions) - (2* non_col_prob *self.num_hashes*(col_prob-non_col_prob)))/(self.num_hashes*b* col_prob**2)

    return est_Jacc
