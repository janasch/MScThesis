# =============================================================================
#                  Preprocessing
# =============================================================================
# Script used to generate the true Jaccard similarity values of the data.


def calc_Jacc(pref_set, other_pref_set):
        """Receives two sets and returns their Jaccard similarity."""

        intersection = len(set(pref_set).intersection(set(other_pref_set)))
        union = len(pref_set) + len(other_pref_set) - intersection
        if union == 0:
            return 0
        else:
            return intersection/ union


def set_initial_JSim(data, data_size, filename_truth):
    """Fills in the JSim Matrix and writes it to a file"""

    JSim = [[0 for x in range(data_size)] for y in range(data_size)]
    user_ids = []

    for counter, user in enumerate(data.keys()):
        user_ids.append(user)

        for other_counter, other_user in enumerate(data.keys()):
            if user == other_user:
                continue
            if counter > other_counter:
                JSim[counter][other_counter] = JSim[other_counter][counter]
                continue

            JSim[counter][other_counter] = calc_Jacc(data[user], data[other_user])

    counter = 0

    with open(filename_truth, 'w') as t:
        print('Writing to file '+ '../JSims/'+filename_truth)
        header = '\t' + ('\t'.join([str(id) for id in data.keys()]))
        user_list = [str(id) for id in data.keys()]
        print(len(user_list), len(JSim))
        t.write(header + '\n')
        for i in range(len(JSim)):
            t.write(user_list[i]+'\t')
            counter += 1
            for j in range(len(JSim)):
                t.write(str(round(JSim[i][j], 5)))
                if j < len(JSim) - 1:
                    t.write("\t")
                else:
                    t.write("\n")



def set_JSim(data_size, filename):
    """Reads in from JSim file and returns JSim matrix containing the
    Jaccard similarity."""

    JSim = [[0 for x in range(data_size)] for y in range(data_size)]
    
    with open(filename) as t:
        next(t)
        i = 0
        for row in t:
            JSims = (row.split('\t'))[1:]
            for j in range(len(JSims)):
                JSim[i][j] = float(JSims[j])
            i += 1
    return JSim
 



