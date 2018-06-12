from shutil import copyfile
from collections import Counter
from Bootstrap.bootstrap import *


def extract_params(subdir):
    """
    Given the name of a subdirectory represented as a string, parses the string to extract and
    return the list of weight function, the number of iterations and the sample size in that order
    """
    params = []  # initialize an empty list to store the parameter values
    comma_separated = subdir.split(",")  # split the subdirectory name based on commas

    for index in range(len(comma_separated) - 1):  # for all except the last comma separated element
        params.append(comma_separated[index].split(" = ")[1])  # retrieve the parameter value
    # account for the id number
    params.append(comma_separated[-1].split(" = ")[1][:len(comma_separated[-1].split(" = ")[1]) - 1])

    return params  # return the list of parameter


SPORT_NAME = "NFL"  # specify the name of the sport

WEIGHT_FUNCTION = "1"  # specify the weight function

# specify the prefix to the directory
DIRECTORY_PREFIX = str(SPORT_NAME) + " Bootstrap Samples (f(x) = " + str(WEIGHT_FUNCTION)

# extract the list of subdirectories
subdirs_list = [name for name in os.listdir(".") if os.path.isdir(name) and name.startswith(DIRECTORY_PREFIX)]

dest_directory = DIRECTORY_PREFIX + ")"  # specify the target subdirectory

os.mkdir(dest_directory)  # create the target subdirectory

overall_sample_index = 0  # initialize the overall sample index

csv_prefix = SPORT_NAME + " Bootstrap Sample "  # specify the prefix to the csv name

# initialize data structures to hold overall rois, sample sizes and parameter values
overall_rois, overall_sample_sizes, overall_params = dict(), dict(), dict()

for subdir in subdirs_list:  # for every subdirectory

    print("Consolidating " + subdir + "...\n")

    weight_fn, num_iter, sample_size = extract_params(subdir)  # extract the bootstrap parameters

    # specify the prefix to the json data files
    json_prefix = SPORT_NAME + " " + str(num_iter) + " Bootstrap Samples ("

    print("Reading stats for current subdirectory...\n")

    # read the json data files
    current_rois = {int(key): float(value) for key, value in dict(read_json("./" + subdir + "/" + json_prefix + "Optimal ROIs).json")).items()}
    current_sample_sizes = {int(key): int(value) for key, value in dict(read_json("./" + subdir + "/" + json_prefix + "Optimal Betting Sample Sizes).json")).items()}
    current_params = {int(key): tuple((float(val) for val in tuple(value))) for key, value in dict(read_json("./" + subdir + "/" + json_prefix + "Optimal Parameters).json")).items()}

    print("Stats for current subdirectory have been successfully loaded\n")

    # for every sample in the subdirectory
    for current_sample_index in range(len(current_rois.keys())):

        print("Overall Sample Index:", overall_sample_index, "\n")
        print("Current Sample Index:", current_sample_index, "\n")
        print("Updating stats for current sample...\n")

        # record the data for the current sample
        overall_rois[overall_sample_index] = current_rois[current_sample_index]
        overall_sample_sizes[overall_sample_index] = current_sample_sizes[current_sample_index]
        overall_params[overall_sample_index] = current_params[current_sample_index]

        print("Stats for current sample have been successfully updated!\n")
        print("Transferring current sample csv to target directory...\n")

        # create the source and destination csv filenames
        src_csv = subdir + "/" + csv_prefix + str(current_sample_index) + ".csv"
        dest_csv = dest_directory + "/" + csv_prefix + str(overall_sample_index) + ".csv"

        copyfile(src_csv, dest_csv)  # copy the current sample csv to the target subdirectory

        print("Current sample csv has been successfully transferred!\n")
        print("Proceeding to next sample...\n")

        overall_sample_index += 1  # update the overall sample index counter

    print("Consolidating " + subdir + " complete!\n")

print("All bootstrap runs have been consolidated!\n")

print("Writing consolidated stats to memory...\n")

counts = Counter(overall_params.values())  # create a counter for the estimated parameters

# store the overall data into json files
write_json(dest_directory + "/" + SPORT_NAME + " Bootstrap Samples (Optimal Parameters).json", str(dict(overall_params)))
write_json(dest_directory + "/" + SPORT_NAME + " Bootstrap Samples (Optimal Betting Sample Sizes).json", str(dict(overall_sample_sizes)))
write_json(dest_directory + "/" + SPORT_NAME + " Bootstrap Samples (Optimal ROIs).json", str(overall_rois))
write_json(dest_directory + "/" + SPORT_NAME + " Bootstrap Samples (Estimated Parameters Counts).json", str(dict(counts)))

print("Consolidation successful! Exiting...\n")

