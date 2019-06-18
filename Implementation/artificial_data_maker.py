import random
import datareader as dr
import preprocessing as pr 
import main

# =============================================================================
#                 Generate Artificial Data Sets
# =============================================================================
# Script to generate artificial data sets and write them to a text file.


def make_data_set(data_size, user_size, density):

    universe_size = int(user_size/density)
    data = [[] for _ in range(data_size)]
    
    for i in range(data_size):
        size = random.randint(1,4) * user_size
        for j in range(size):
            val = random.randint(0, universe_size)
            while val in data[i]:
                val = random.randint(0, universe_size)
            data[i].append(val)
    
    return data


def make_clust_data_set(data_size, user_size, density, clusters):
    
    universe_size = int(user_size/density)
    data = [[] for _ in range(data_size)]

    min_lim = 0
    max_lim = int(universe_size/clusters)
    elements_per_cluster = int(data_size/clusters)

    counter = 0
    for i in range(clusters):
        for j in range(elements_per_cluster):
            val = random.randint(min_lim, max_lim)
            data[counter].append(val)
        min_lim = max_lim
        max_lim += int(universe_size/clusters)
    
    return data


def get_avg_simi(data):
    avg_sim = 0
    counter = 0
    for i in range(len(data)):
        for j in range(i+1, len(data)):
            jac = pr.calc_Jacc(data[i], data[j])
            avg_sim += jac
            counter += 1
    return avg_sim/counter

def write_to_file(data, filename, size, simi):
    with open(filename, 'w') as f:
        f.write(str(size) + ',' + str(simi) + '\n')
        for i in range(len(data)):
            for j in range(len(data[i])):
                f.write(str(data[i][j]))
                if not j == len(data[i]) -1:
                    f.write(',')
            if not i == len(data) -1:
                f.write('\n')

user_size = 20
data_size = 2000
densities = [0.2, 0.1, 0.01, 0.0001]
for dens in densities:
    data = make_data_set(data_size, user_size, dens)
    size = int(user_size/dens)
    simi = get_avg_simi(data)
    filename = 'input_data/Artificial_data/artificial_data_' + str(size) + '.dat'
    write_to_file(data, filename, size, simi)
    truth_file_name = 'Artificial_data/artificial_data_' + str(size) + '.dat'
    data, JSim = main.setup(truth_file_name)
    


    
        



