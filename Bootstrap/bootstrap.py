import os
import csv
import json
import random
import numpy as np
from ast import literal_eval


def compute_num_games(data):
    """
    Given a data set represented as a list of lists, computes and returns the number
    of games in the data set
    """
    return int((len(data) - 2) / 3)  # return the number of games


def bootstrap(data, sample_size=int(1e4), num_iter=int(1e3)):
    """
    Given the original data matrix, the number of observations to be included in each
    bootstrap sample and the number of bootstrap samples to create, produces and returns
    the bootstrap samples
    """
    samples = dict()  # initialize data structure to hold the bootstrap samples
    num_games = (len(data) - 2) / 3  # compute the total number of games in the original data set
    for iter_index in range(num_iter):  # for every bootstrap sample to be created
        current_sample = list([list(data[0]), list(data[1])])  # initialize the data matrix heading
        for sample_index in range(sample_size):  # for the specified number of observations to include in each sample
            game_index = 3 * random.randrange(num_games) + 2  # select a game at random with replacement

            fav_row = data[game_index]  # extract the favorite, underdog and spacer rows
            dog_row = data[game_index + 1]
            spacer_row = data[game_index + 2]

            current_sample.append(list(fav_row))  # add the rows to the current bootstrap sample matrix
            current_sample.append(list(dog_row))
            current_sample.append(list(spacer_row))
        samples[iter_index] = list(current_sample)  # store the sample
    return samples  # return all the samples


def compute_nth_percentile(data, n):
    """
    Given a data represented as a python iterable and an integer n, computes and returns
    the nth percentile of the input data
    """
    return np.percentile(np.array(data), n)  # compute and return the nth percentile


def write_bootstrap_samples(samples, weight_fn, num_iter, sample_size, sport_name):
    """
    Given the bootstrap samples, the weight function, the number of iterations, the
    sample size and the name of the sport, writes the bootstrap samples to memory
    """
    # find a unique target directory name to avoid overwriting pre-written bootstrap samples
    directory_name = __determine_directory_name(sport_name, weight_fn, num_iter, sample_size)
    os.makedirs(directory_name)  # create the target directory
    for sample_index, sample in samples.items():  # for every sample
        # create the unique bootstrap sample csv name
        sample_filename = sport_name + " Bootstrap Sample " + str(sample_index) + ".csv"
        # build the path to which the sample csv should be written
        sample_filepath = "/".join(list([directory_name, sample_filename]))
        write_csv(sample_filepath, sample)  # write the sample csv to memory
    return directory_name  # return the name of the target directory


def __determine_directory_name(sport_name, weight_fn, num_iter, sample_size):
    """
    Given the name of the sport, the weight function, the number of iterations and
    the sample size of each bootstrap sample, determines a unique directory name in
    which to store the bootstrap samples
    """
    id_no = 1  # initialize the id number to 1
    while True:  # enter an infinite loop - termination criteria discussed below
        # specify the current directory name
        directory_name = sport_name + " Bootstrap Samples (f(x) = " + str(weight_fn) + ", Iterations = " + \
                         str(num_iter) + ", Sample Size = " + str(sample_size) + ") (" + str(id_no) + ")"
        if os.path.exists(directory_name):  # if directory already exists
            id_no += 1  # increment id number
        else:
            return directory_name  # otherwise return the unique directory name


def write_csv(filepath, data):
    """
    Given a list of lists representing a data matrix and a file path, stores the input
    matrix in a csv file
    """
    with open(filepath, "w") as csv_file:  # create and open the csv file
        csv_writer = csv.writer(csv_file, delimiter=",")  # create a csv writer
        for row in data:  # for every row in the input matrix
            csv_writer.writerow(list(row))  # write the input matrix to the csv file


def write_json(filepath, data):
    """
    Given a python data structure and a file path, converts the data structure to a json
    string which is then stored in the input file path
    """
    with open(filepath, "w") as write_file:  # create and open the json file
        json.dump(data, write_file)  # store the python data structure in the json file


def read_json(filepath):
    """
    Given the path to a json file represented as a string, loads and parses the json
    string contained in the file to return the resulting python data structure
    """
    with open(filepath, 'r') as read_file:  # open the json filename
        # read the json string, parse and return the python data structure
        return literal_eval(str(json.load(read_file)))

