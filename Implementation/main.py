import os
import sys
import math
import datareader as dr
import preprocessing
import analysis as anal
import argparse
import minhash
import privmin
import bucket_privmin
import sec_minhash
import noisy_sec_minhash




def setup(file):
    
    data = dr.read_data(file) 
    data_size = len(data.keys()) 
    
    filename_JSim = 'JSims/'+ file.replace('.dat', '_truth.txt')
    
    # comment in when using an unknown data set
    # preprocessing.set_initial_JSim(data, data_size, filename_JSim)
    
    JSim = preprocessing.set_JSim(data_size, filename_JSim)
        
    return data, JSim



def hashing(data, num_hashes, eps, minhash_type, l, b, alpha, delta, num_buckets):
    next_prime = 2**31 -1

    if 'privmin' == minhash_type.lower():
        priv = privmin.PrivMin(num_hashes, data, eps)
        user_to_sig = priv.generate_minHash_sigs()
        estJSim = anal.set_estJSim(priv, user_to_sig)

    elif 'bucket' in minhash_type.lower():
        bucket_priv = bucket_privmin.Bucket_PrivMin(num_hashes, data, eps, num_buckets, False)
        user_to_sig = bucket_priv.generate_minHash_sigs()
        estJSim = anal.set_estJSim(bucket_priv, user_to_sig)
        
    elif 'sec_minhash' == minhash_type.lower():
        sec_mh = sec_minhash.Sec_MinHash(num_hashes, data, l)
        user_to_sig = sec_mh.generate_minHash_sigs()
        estJSim = anal.set_estJSim(sec_mh, user_to_sig)

    elif 'noisy' in minhash_type.lower():
        noisy_sec = noisy_sec_minhash.Noisy_Sec_MinHash(num_hashes, data, eps, l, alpha, delta, b=b)
        user_to_sig = noisy_sec.generate_minHash_sigs()
        estJSim = anal.set_estJSim(noisy_sec, user_to_sig)

    else:
        reg_mh = minhash.MinHash(num_hashes, data)
        user_to_sig = reg_mh.generate_minHash_sigs()
        estJSim = anal.set_estJSim(reg_mh, user_to_sig)

    return user_to_sig, estJSim




def run_analysis(user_to_sig, JSim, estJSim, neighbours):
    
    analysis = anal.Analysis(user_to_sig, JSim, estJSim)
    MSE = analysis.MSE()
    prec, recall, f1 = analysis.PRF()

    print('MSE', MSE)
    print('recall ', recall)



def main(data, JSim, minhash_type, num_hashes, eps=None, delta = None, l=None, b=None, alpha=None, num_buckets = None):

    user_to_sig, est_JSim = hashing(data, num_hashes, eps, minhash_type, l, b, alpha, delta, num_buckets)

    analysis = anal.Analysis(user_to_sig, JSim, est_JSim)
    
    return analysis


