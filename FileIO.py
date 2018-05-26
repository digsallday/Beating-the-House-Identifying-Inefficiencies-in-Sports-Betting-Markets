import csv
import json


class FileIO:
    """
    Class containing useful static methods for reading from and writing to files on memory.
    Currently supported formats include:
    - .txt
    - .csv
    - .json
    """

    @staticmethod
    def read_file(filename):
        """
        Given the filename of a generic file format, reads and returns the contents of the
        file as a string
        """
        return open(filename, "r").read()  # open, read and return the contents of the file

    @staticmethod
    def write_file(string, filename):
        """
        Given a string and a filename, creates a file of generic format and stores the string
        within the file
        """
        # create a file with the input filename, open it and store the input string within
        open(filename, "w").write(string)

    @staticmethod
    def read_csv(csv_filename):
        """
        Given a csv filename, reads the file from memory and returns the csv data using a
        list of lists representation
        """
        csv_matrix = list()  # initialize an empty list
        with open(csv_filename, "r") as csv_file:  # open the csv file
            csv_reader = csv.reader(csv_file, delimiter=",")
            for row in csv_reader:  # for every row in the csv file
                # adds a list representing the row to the initialized matrix at the top
                csv_matrix.append(list([str(elem) for elem in row]))
        return csv_matrix  # returns the matrix of data

    @staticmethod
    def write_csv(csv_filename, data_matrix):
        """
        Given a csv filename and a matrix of data (represented as a list of lists), creates
        a csv file and stores the data matrix within
        """
        with open(csv_filename, "w") as csv_file:  # create and open a csv file with the input filename
            csv_writer = csv.writer(csv_file, delimiter=",")
            for row in data_matrix:  # for every row in the data matrix
                csv_writer.writerow(list(row))  # write the row to memory

    @staticmethod
    def read_json(json_filename):
        """
        Given a json filename, reads the file from memory and returns the python data structure
        stored in the json file
        """
        with open(json_filename, "r") as json_data:  # open the json file
            return json.load(json_data)  # return the python data structure stored within

    @staticmethod
    def write_json(data_structure, json_filename):
        """
        Given a python data structure and a json filename, creates a json file and stores the
        data structure within
        """
        with open(json_filename, "w") as json_file:  # create and open a json file with the input filename
            json.dump(data_structure, json_file)  # write the python data structure to memory

