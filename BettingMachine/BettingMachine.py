from FileIO import FileIO
from BMGlobals import BMGlobals
from EVCalculator.EVGlobals import EVGlobals


class BettingMachine:
    """
    BettingMachine class that applies the betting algorithm to a given list of games and writes the computed
    cumulative and percent returns on investment to memory
    """
    def __init__(self, sport_name, time_period, weight_fn_str, verbose=True):
        """
        Constructor for the BettingMachine class - initializes instances of the class and the attributes
        of the created object
        """
        self.sport_name = sport_name  # initialize the attributes of this object
        self.time_period = time_period
        self.weight_fn_str = weight_fn_str
        self.verbose = verbose

        self.ev_csv = \
            FileIO.read_csv(
                " ".join(list([
                    self.get_sport_name(),
                    EVGlobals.EV_CSV_SUFFIX,
                    "(" + ", ".join(list([str(self.get_time_period()), self.get_weight_fn_str()])) + ").csv"
                ]))
            )  # read the ev csv containing all the expected values

    def run(self, epsilon, ev_threshold):
        """
        Given the values of epsilon and ev threshold, runs the betting algorithm on each of the games in the
        expected value csv and writes the results to the memory
        """
        results_csv_filename = \
            " ".join(
                list([
                    self.get_sport_name(),
                    BMGlobals.RESULTS_CSV_SUFFIX,
                    "(" + ", ".join(list([str(self.get_time_period()), self.get_weight_fn_str()])) + ").csv"
                ])
            )  # specify the results csv filename

        ev_csv = self.get_ev_csv()

        results_csv = list([BMGlobals.RESULTS_CSV_HEADER, list()])

        total = 0  # initialize stats for this run of the betting algorithm
        total_bet_on = 0
        correct = 0
        wrong = 0

        double_pos = 0

        winning_returns = 0.00
        losing_returns = 0.00

        theoretical_ev = 0.00

        for row_index in range(2, len(ev_csv), 3):  # for every game in the bootstrap ev_csv

            total += 1  # keep count of the number of games

            fav_row = list(ev_csv[row_index])  # get the favorite row
            dog_row = list(ev_csv[row_index + 1])  # get the underdog row
            spacer_row = list(ev_csv[row_index + 2])  # get the space row

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
                if (fav_win_pct <= (0.5 - epsilon / 100) or fav_win_pct >= (0.5 + epsilon / 100)):
                    if fav_ev > 0 and dog_ev > 0:  # check if both ev are positive
                        double_pos += 1  # and update appropriate counter
                    total_bet_on += 1  # update counters
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
                    if fav_ev > ev_threshold / 1000:  # if the ev is greater than the threshold
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
                    if dog_ev > ev_threshold / 1000:  # if the ev is greater than the threshold
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

            fav_row.append(winning_returns + losing_returns)  # record the overall winnings
            dog_row.append(winning_returns + losing_returns)

            results_csv.append(fav_row)  # add the favorite, underdog and spacer rows to the results csv
            results_csv.append(dog_row)
            results_csv.append(spacer_row)

        FileIO.write_csv(results_csv_filename, results_csv)  # write the results csv to memory

    def compute_arbitrage(self):
        """
        Computes and returns the number of games where arbitrage is present
        """
        num_arbitrage = 0  # initialize the number of game with arbitrage to zero

        ev_csv = self.get_ev_csv()  # get the ev csv

        for row_idx in range(2, len(ev_csv), 3):  # for every game
            fav_row = list(ev_csv[row_idx])  # get the favorite and underdog rows
            dog_row = list(ev_csv[row_idx + 1])

            fav_moneyline = float(fav_row[6])  # get the favorite and underdog moneylines
            dog_moneyline = float(dog_row[6])

            # check if arbitrage exists and update counter accordingly
            num_arbitrage += int(abs(dog_moneyline) > abs(fav_moneyline))

        return num_arbitrage  # return the number of games with arbitrage

    @staticmethod
    def compute_num_games(data):
        """
        Given a data set represented as a list of lists, computes and returns the number
        of games in the data set
        """
        return int((len(data) - 2) / 3)  # return the number of games

    def display(self, message):
        """
        Given a message string, prints the message if the verbose option is turned on
        """
        if self.get_verbose():  # if the verbose boolean is set to true
            print(str(message))  # print the input message

    def get_sport_name(self):
        """
        Returns the sport name
        """
        return self.sport_name  # return the sport name

    def get_time_period(self):
        """
        Returns the time period
        """
        return self.time_period  # return the time period

    def get_weight_fn_str(self):
        """
        Returns the weight function string
        """
        return self.weight_fn_str  # return the weight function string

    def get_verbose(self):
        """
        Returns the verbose option
        """
        return self.verbose  # return the verbose option

    def get_ev_csv(self):
        """
        Returns the expected value csv
        """
        return self.ev_csv  # return the expected value csv

    def set_sport_name(self, sport_name):
        """
        Given a new sport name, sets the current sport name as the new sport name
        """
        self.sport_name = sport_name  # set the current sport name as the new sport name

    def set_time_period(self, time_period):
        """
        Given a new time period, sets the current time period as the new time period
        """
        self.time_period = time_period  # set the current time period as the new time period

    def set_weight_fn_str(self, weight_fn_str):
        """
        Given a new weight function string, sets the current weight function string as the new weight
        function string
        """
        # set the current weight function string as the new weight function string
        self.weight_fn_str = weight_fn_str

    def set_verbose(self, verbose):
        """
        Given a new verbose option, sets the current verbose option as the new verbose option
        """
        self.verbose = verbose  # set the current verbose option as the new verbose option

    def set_ev_csv(self, ev_csv):
        """
        Given a new expected value csv, sets the current expected value csv as the new expected value csv
        """
        self.ev_csv = ev_csv  # set the current expected value csv as the new expected value csv
