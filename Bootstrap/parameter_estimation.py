import csv
from math import ceil
from pprint import pprint
from time import time, sleep
from Bootstrap.bootstrap import *
from collections import Counter


t_0 = time()  # start the timer

SPORT_NAME = "NFL"  # specify the name of the sport

WEIGHT_FUNCTION = "x"  # specify the weight function

# specify the name of the file
DATA_FILENAME = SPORT_NAME + " EV Data (Aggregate (f(x) = " + WEIGHT_FUNCTION + ")).csv"

SAMPLE_COUNT = 1000  # specify the number of bootstrap samples

csv_matrix = []  # initialize the matrix
with open(DATA_FILENAME, "r") as csv_file:  # open the file
    csv_reader = csv.reader(csv_file, delimiter=",")  # read the file
    for row in csv_reader:  # for every row, i.e. data field
        csv_matrix.append(list(row))  # append it to the matrix

SAMPLE_SIZE = compute_num_games(csv_matrix)  # compute the number of games

positive_ev = list()  # initialize an empty list to store the ev values
for row_index in range(2, len(csv_matrix), 3):
    fav_row = csv_matrix[row_index]  # access the favorite row
    dog_row = csv_matrix[row_index + 1]  # access the dog row

    positive_ev.append(float(fav_row[-1]))  # append the ev values for both the favorite and dog rows
    positive_ev.append(float(dog_row[-1]))

# compute the ev upper bound as the 95th percentile of all ev values
ev_upper_bound = compute_nth_percentile(positive_ev, 95)

print("Computed EV Upper Bound:", str(ev_upper_bound), "\n")

best_rois = dict()  # initialize the necessary data structures to store the data

best_sample_sizes = dict()

estimated_parameters = dict()

print("Bootstrapping...\n")

# create the bootstrap samples
samples = bootstrap(csv_matrix, sample_size=SAMPLE_SIZE, num_iter=SAMPLE_COUNT)

# create the name of the directory
directory_name = write_bootstrap_samples(samples, WEIGHT_FUNCTION, SAMPLE_COUNT, SAMPLE_SIZE, SPORT_NAME)

print("Bootstrapping Complete...\n")

# for every bootstrap sample created
for sample_index, sample in samples.items():

    t_s0 = time()

    print("Sample Index:", sample_index)

    threshold = range(0, int(ceil(ev_upper_bound * 1000)), 1)  # produce the range of threshold values

    eps = range(0, 51, 1)  # produce the range of epsilon values

    betting_sample_size = dict()  # initialize data structures to store stats

    profits = dict()

    objective_function_values = dict()

    cumulative_returns = []

    roi = []

    for e in eps:  # for every epsilon value
        for t in threshold:  # for every ev threshold value
            edge = 0  # initialize stats for this run of the betting algorithm

            total = 0
            total_bet_on = 0
            correct = 0
            wrong = 0

            double_pos = 0

            winning_returns = 0.00
            losing_returns = 0.00

            theoretical_ev = 0.00

            for row_index in range(2, len(sample), 3):  # for every game in the bootstrap sample

                total += 1  # keep count of the number of games

                fav_row = list(sample[row_index])  # get the favorite row
                dog_row = list(sample[row_index + 1])  # get the underdog row
                spacer_row = list(sample[row_index + 2])  # get the space row

                fav_ev = float(fav_row[9])  # get the favorite team ev
                dog_ev = float(dog_row[9])  # get the underdog team ev

                fav_score = float(fav_row[3])  # get the final game score for the favorite team
                dog_score = float(dog_row[3])  # get the final game score for the underdog team

                fav_payout = float(fav_row[7])  # get the payout for the favorite team
                dog_payout = float(dog_row[7])  # get the payout for the underdog team

                fav_win_pct = float(fav_row[8])  # get the win percentage for the favorite team
                dog_win_pct = float(dog_row[8])  # get the win percentage for the underdog

                if fav_score > dog_score:  # if the favorite score is higher than the underdog score
                    fav_row.append('W')  # "W" for the favorite
                    dog_row.append('L')  # "L" for the underdog
                elif fav_score < dog_score:  # if the underdog score is higher than the favorite score
                    fav_row.append('L')  # "L" for the favorite
                    dog_row.append('W')  # "W" for the underdog
                elif fav_score == dog_score:  # if the scores are tied
                    fav_row.append('T')  # "T" for both teams
                    dog_row.append('T')

                # check if the ev values are not both negative
                if (fav_ev > 0 and dog_ev < 0) or (fav_ev < 0 and dog_ev > 0) or (fav_ev > 0 and dog_ev > 0):
                    # check if the win percentages are outside the epsilon bounds
                    if (fav_win_pct <= (0.5 - e / 100) or fav_win_pct >= (0.5 + e / 100)):
                        if fav_ev > 0 and dog_ev > 0:  # check if both ev are positive
                            double_pos += 1  # and update appropriate counter
                        edge += 1  # update counters
                        total_bet_on += 1
                        # if the favorite win percentage is higher than that of the underdog
                        if fav_win_pct > dog_win_pct:
                            theoretical_ev += fav_ev  # update the theoretical ev
                            if fav_score > dog_score:  # if the favorite won the game
                                correct += 1  # update correct bet counter
                                winning_returns += fav_payout  # update positive returns
                                fav_row.append(fav_payout)  # record the winnings from this bet
                                dog_row.append(fav_payout)
                            elif fav_score < dog_score:  # if the underdog won the game
                                wrong += 1  # update incorrect bet counter
                                losing_returns -= 1  # update losing returns
                                fav_row.append(str('-1'))  # record the losses from this bet
                                dog_row.append(str('-1'))
                        # if the underdog win percentage is higher than that of the favorite
                        elif fav_win_pct < dog_win_pct:
                            theoretical_ev += dog_ev  # update the theoretical ev
                            if dog_score > fav_score:  # if the underdog won the game
                                correct += 1  # update the correct bet counter
                                winning_returns += dog_payout  # update positive returns
                                fav_row.append(dog_payout)  # record the winnings from this bet
                                dog_row.append(dog_payout)
                            elif dog_score < fav_score:  # if the favorite won the game
                                wrong += 1  # update the incorrect bet counter
                                losing_returns -= 1  # update losing returns
                                fav_row.append(str('-1'))  # record the losses from this bet
                                dog_row.append(str('-1'))
                    elif fav_ev > dog_ev:  # if the favorite ev is higher than the underdog ev
                        if fav_ev > t / 1000:  # if the ev is greater than the threshold
                            total_bet_on += 1  # update the total number of bets placed
                            theoretical_ev += fav_ev  # update theoretical ev
                            if fav_score > dog_score:  # if the favorite won the game
                                correct += 1  # update the correct bet counter
                                winning_returns += fav_payout  # update positive returns
                                fav_row.append(fav_payout)  # record the winnings from this bet
                                dog_row.append(fav_payout)
                            elif fav_score < dog_score:  # if the underdog won the game
                                wrong += 1  # update the incorrect bet counter
                                losing_returns -= 1  # update losing returns
                                fav_row.append(str('-1'))  # record the losses from this bet
                                dog_row.append(str('-1'))
                    elif fav_ev < dog_ev:  # if the underdog ev is higher than the favorite ev
                        if dog_ev > t / 1000:  # if the ev is greater than the threshold
                            total_bet_on += 1  # update the total number of bets placed
                            theoretical_ev += dog_ev  # update theoretical ev
                            if dog_score > fav_score:  # if the underdog won the game
                                correct += 1  # update the correct bet counter
                                winning_returns += dog_payout  # update positive returns
                                fav_row.append(dog_payout)  # record the winnings from this bet
                                dog_row.append(dog_payout)
                            elif dog_score < fav_score:  # if the favorite won the game
                                wrong += 1  # update the incorrect bet counter
                                losing_returns -= 1  # update losing returns
                                fav_row.append(str('-1'))  # record the losses from this bet
                                dog_row.append(str('-1'))
                if len(fav_row) == 11 and len(dog_row) == 11:
                    fav_row.append(str('0'))  # record 0 if a bet was not placed
                    dog_row.append(str('0'))

                # elif fav_ev > 0 and dog_ev > 0:
                #     double_pos += 1
                #     if fav_score > dog_score:
                #         if fav_ev > threshold:
                #             theoretical_ev += fav_ev + dog_ev
                #             total_bet_on += 2
                #             #correct += 1
                #             winning_returns += fav_payout
                #             losing_returns -= 1
                #     elif fav_score < dog_score:
                #         if dog_ev > threshold:
                #             theoretical_ev += fav_ev + dog_ev
                #             total_bet_on += 2
                #             #wrong += 1
                #             winning_returns += dog_payout
                #             losing_returns -= 1
                fav_row.append(winning_returns + losing_returns)  # record the overall winnings
                dog_row.append(winning_returns + losing_returns)

                # record ROI until this point
                if total_bet_on == 0:
                    roi.append(float(0))
                else:
                    roi.append((winning_returns + losing_returns) / total_bet_on * 100)

                # record the cumulative returns
                cumulative_returns.append(winning_returns + losing_returns)

            # construct the parameter key using epsilon and ev threshold values
            param_key = tuple((e / 100, t / 1000))

            # record the roi percentage for this setting of parameter values
            profits[param_key] = ((winning_returns + losing_returns) / total_bet_on * 100)

            # record the total number of games bet on
            betting_sample_size[param_key] = total_bet_on

            # compute and record the objective function value
            # objective function = roi * number of bets placed
            objective_function_values[param_key] = profits[param_key] * betting_sample_size[param_key]

            # print('Threshold:', t/1000)
            # print('\n')
            # print('Epsilon:', e/100)
            # print('\n')
            # print('Total Number of Games:', total)
            # print('\n')
            # print('Total Number of Games Bet On:', total_bet_on)
            # print('\n')
            # print('Total Number of Correct Bets:', correct)
            # print('\n')
            # print('Total Number of Wrong Bets:', wrong)
            # print('\n')
            # print('Total Number of Tied Bets:', total_bet_on - (correct + wrong))
            # print('\n')
            # print('Total Winning Returns:', winning_returns)
            # print('\n')
            # print('Total Losing Returns:', losing_returns)
            # print('\n')
            # print('Aggregate Returns:', winning_returns + losing_returns)
            # print('\n')
            # print('Aggregate Returns (%):', (winning_returns + losing_returns) / total_bet_on * 100)
            # print('\n')
            # print('Theoretical Returns:', theoretical_ev)
            # print('\n')
            # print('Theoretical Returns (%):', theoretical_ev / total_bet_on * 100)
            # print('\n')
            # print('Double Positive Games:', double_pos)
            # print('\n')
            #
            # print(edge)
            #

    # print(profits)

    # print(profits.values())

    # print("Betting Sample Size:", betting_sample_size)
    #
    # print("Maximum ROI:", max(profits.values()))

    max_obj_val = max(objective_function_values.values())  # compute optimal objective function value
    for et in objective_function_values.keys():  # for every pair of parameter values
        # if the corresponding objective function value is optimal
        if objective_function_values[et] == max_obj_val:
            epsilon_val, ev_val = et  # unpack the parameter values

            print("Optimal Epsilon:", epsilon_val)
            print("Optimal EV:", ev_val)
            print("Optimal Betting Sample Size:", betting_sample_size[et])
            print("Optimal ROI:", profits[et])

            estimated_parameters[sample_index] = et  # recorded the optimal parameter setting
            best_rois[sample_index] = profits[et]  # record the optimal roi
            best_sample_sizes[sample_index] = betting_sample_size[et]  # record the optimal number of bets

            t_s1 = time()

            print("Time taken for grid search:", t_s1 - t_s0, "s\n")

            break

counts = Counter(estimated_parameters.values())  # compute counts for each parameter setting

pprint(counts)

# write overall stats to json files
write_json(directory_name + "/" + SPORT_NAME + " " + str(SAMPLE_COUNT) + " Bootstrap Samples (Optimal Parameters).json", str(dict(estimated_parameters)))
write_json(directory_name + "/" + SPORT_NAME + " " + str(SAMPLE_COUNT) + " Bootstrap Samples (Optimal Betting Sample Sizes).json", str(best_sample_sizes))
write_json(directory_name + "/" + SPORT_NAME + " " + str(SAMPLE_COUNT) + " Bootstrap Samples (Optimal ROIs).json", str(best_rois))
write_json(directory_name + "/" + SPORT_NAME + " " + str(SAMPLE_COUNT) + " Bootstrap Samples (Estimated Parameters Counts).json", str(dict(counts)))

t_1 = time()  # stop the timer

print('\n')
print('Time Taken: ' + str(t_1 - t_0))  # output program execution time
print('\n')

