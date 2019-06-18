import random
import math
import numpy as np
import minhash as mh
import sec_minhash as sec_mh

# =============================================================================
#                 Generate signatures by Noisy Secure MinHash
# =============================================================================
# Concatenates k minimum hash values, maps them to 1 bit and adds noise to them.
# Returns noisy signature of length L.


class Noisy_Sec_MinHash(sec_mh.Sec_MinHash):
  """T is the minimum required user set size.
  Alpha is the definition of neighbouring databases.
  Eps is the privacy budget.
  B is an optional argument to directly set noise scale.
  """ 

  def __init__(self, num_hashes, users, eps, L, alpha, delta, b=None):
      sec_mh.Sec_MinHash.__init__(self, num_hashes, users, L)
      self.T = 20
      self.delta = delta
      self.alpha = alpha
      self.eps = eps
      self.sensitivity = self.set_sensitivity()
      self.var_lap = 2 * (self.sensitivity/self.eps)**2
      if not b == None:
        self.sensitivity = b
        self.eps = 1
        self.var_lap = 2 * b**2
      

  def calc_theoretical_Jacc(self):
    """Returns theoretical Jaccard similarity used in estimating E[P]."""
    theo_jacc = 1 - (self.alpha/self.T)
    return theo_jacc


  def set_sensitivity(self):
    diff_prob = 1 - ((self.calc_theoretical_Jacc()**self.num_hashes + 1)/2)
    exp_diff = self.L * diff_prob
    beta = (1 + math.sqrt((3 * math.log(1/self.delta))/exp_diff))
    sensi = exp_diff*(1 + beta)
    return sensi

  def draw_noise(self):
    a = np.random.laplace(scale=self.sensitivity/ self.eps, size=1)
    return a

  def hash_universal(self, signature, k, l):
    """Maps received signature to 1-bit and adds noise to it."""
    uni = self.rand_ints[l][self.num_hashes]
    for i in range(len(signature)):
      uni = uni + (signature[i] * self.rand_ints[l][i])
    return (uni % self.next_prime % 2) + self.draw_noise()


  def calc_est_Jacc(self, signature, other_signature):
    """Debiased Jaccard similarity estimator"""
    sig = np.array(signature)
    oth = np.array(other_signature)
    euc_dist = np.square(sig - oth).sum()
    euc_dist -= (self.L * 2 * self.var_lap)
    collisions = self.L - euc_dist
    return 2*(collisions/self.L) - 1
