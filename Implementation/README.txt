
The experiments used in the thesis report can be found in the Jupyter Notebook named Experiments.ipynb


Running algorithms from the command line using Pyhton 3.+:

Arguments:

    # The dataset used by the algorithm

    -s      --set               0 = MovieLens , 1 = Last.FM  

    # The algorithm used

    -a      --algorithm         0 = MinHash , 1 = Secure MinHash , 2 = Bucket PrivMin , 3 = Noisy Secure MinHash, 4 = PrivMin 

    # Number of hash functions (Number of minimum values hashed to 1 bit in (Noisy) Secure MinHash)

    -k      --hashes 

    # Length of signature in (Noisy) Secure MinHash

    -l      --length 

    # Privacy budget - not applicable for (Secure) MinHash

    -e      --epsilon

    # Probability of problematic data release in Noisy Secure MinHash (delta)

    -d      --delta

    # Number of buckets in Bucket PrivMin

    -b      --buckets    


Algorithms:

    # Mandatory arguments
    
    MinHash                     -a -s -k

    Secure MinHash              -a -s -k -l

    Bucket PrivMin              -a -s -k -e -b

    Noisy Secure MinHash        -a -s -k -l -e -d 

    PrivMin                     -a -s -k -e 


