from Bootstrap.bootstrap import read_json, write_csv


SPORT_NAME = "NFL"  # specify the name of the sport

WEIGHT_FUNCTION = "1"  # specify the weight function

# specify directory name where the target csv is to be saved
DIRECTORY_NAME = SPORT_NAME + " Bootstrap Samples (f(x) = " + WEIGHT_FUNCTION + ")"

JSON_PREFIX = SPORT_NAME + " Bootstrap Samples "  # specify the prefix to the json data files

CSV_PREFIX = SPORT_NAME + " Bootstrap Summary "  # specify the prefix to the csv name

# initialize the heading to the summary csv
summary_csv = list([list(["Sample Index", "Epsilon", "EV Threshold", "ROI", "Number of Bets"])])

print("Reading statistics of bootstrap runs...\n")

# read the json data files
rois = read_json(DIRECTORY_NAME + "/" + JSON_PREFIX + "(Optimal ROIs).json")

betting_sample_sizes = read_json(DIRECTORY_NAME + "/" + JSON_PREFIX + "(Optimal Betting Sample Sizes).json")

parameters = read_json(DIRECTORY_NAME + "/" + JSON_PREFIX + "(Optimal Parameters).json")

print("Statistics successfully loaded!\n")
print("Creating summary csv...\n")

# for every sample in the dictionaries
for sample_index in range(len(rois.keys())):
    epsilon, ev_threshold = parameters[sample_index]  # unpack the betting algorithm parameter values
    # append the summary csv row
    summary_csv.append(
        list([
            sample_index,
            epsilon,
            ev_threshold,
            rois[sample_index],
            betting_sample_sizes[sample_index]
        ])
    )

print("Summary csv successfully created!\n")
print("Writing summary csv to memory...\n")

# store the summary csv
write_csv(DIRECTORY_NAME + "/" + CSV_PREFIX + "(f(x) = " + WEIGHT_FUNCTION + ").csv", summary_csv)

print("Summary csv successfully stored in memory!\n")
print("Summary csv can be accessed at \'" + DIRECTORY_NAME + "/" + CSV_PREFIX + "(f(x) = " + WEIGHT_FUNCTION + ").csv" + "\n")

