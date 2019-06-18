import collections
import heapq

# =============================================================================
#                 Read in user profiles
# =============================================================================
# Reads in user data from text files and returns a mapping from users
# to item sets.


def avg_set_size(data):
    total = 0
    for pref_set in data.values():
        total += len(pref_set)
    return total / len(data)


def get_max_ID(users):
    high = 0
    for user in users.keys():
        for item in users[user]:
            if item > high:
                high = item
    return high


def del_weights(users):
    """Helper function to clean the last.FM data"""
    users_cleaned = collections.OrderedDict()
    for user, weight_artist_tuples in users.items():
        artists = []
        for tupl in weight_artist_tuples:
            artists.append(tupl[1])
        users_cleaned[user] = artists
    return users_cleaned


def read_lastfm(data_file):
    """Receives the last.FM dataset as textfile. Returns a dictionary
    mapping each user to her max 20 favourite artists.
    """
    users = collections.OrderedDict()
    with open(data_file) as f:
        next(f) # skip header line 
        prev_user = 0
        min_heap = []
        for line in f:
            user_id, artist_id, weight = [int(x) for x in line.split("\t")[:3]] 
            if user_id != prev_user :
                users[prev_user] = min_heap
                prev_user = user_id
                min_heap = []
            if len(min_heap) < 20:
                heapq.heappush(min_heap, (weight, artist_id))
            elif weight > min_heap[0][0]:
                heapq.heapreplace(min_heap, (weight, artist_id))
        users[prev_user] = min_heap
    del users[0] #first one empty
    users_cleaned = del_weights(users)        
    return (users_cleaned)


def read_movielens(data_file):
    """Receives the MovieLens dataset as textfile. Returns a dictionary
    mapping each user to all her movies rated with score of >= 4.5.
    """
    users = collections.OrderedDict()  # maps user to pref_set
    with open(data_file) as f:
        next(f) # skip header line 
        for line in f:
            info = line.split("\t")[:3]  
            users.setdefault(int(info[0]), []) 
            if float(info[2]) >= 4:
                users[int(info[0])].append(int(info[1]))

    clean_users = {}
    for user in users:
        if len(users[user]) > 0:
            clean_users[user] = users[user] 
    return (clean_users)



def make_test_file(data_file):
    test_file = 'input_data/test_files/test_lastfm_10.txt'
    test_content = []
    with open(data_file) as f:
        user_counter = 0
        prev_user = -1
        test_content.append(f.readline())
        for line in f:
            test_content.append(line)
            user_id = line.split("\t")[0]
            if user_id != prev_user :
                prev_user = user_id
                user_counter += 1
                if user_counter > 10:
                    break
    with open(test_file, 'w') as out:
        for line in test_content[0:-1]:
            out.write(line)
            
def read_artificial_data(data_file):
    """Receives a self-produced dataset as textfile. Returns a dictionary
    mapping each user to her set of items.
    """
    users = collections.OrderedDict() 
    with open(data_file) as f:
        avg_sim = float(f.readline().split(',')[1])
        counter = 0 
        for line in f:
            counter += 1
            user_id = counter
            pref_set = [int(x) for x in line.split(',')]
            users[user_id] = pref_set
    print(len(users))
    return users


def read_data(data_file):
    """Main method of class. Receives a text file as string and chooses which
    function to call to process the data set. Returns a dictionary mapping user IDs
    to item sets.
    """
    data_file = 'input_data/' + data_file
    if 'movielens' in data_file:
        users = read_movielens(data_file)
    elif 'lastfm' in data_file:
        users = read_lastfm(data_file)
    elif 'artificial' in data_file.lower():
        users = read_artificial_data(data_file)
    else:
        print("ERROR: DataReader couldn't determine dataset")
    return users




