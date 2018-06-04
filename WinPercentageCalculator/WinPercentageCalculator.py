from FileIO import FileIO
from WPGlobals import WPGlobals
from VegasInsiderSpider import VIGlobals
from KillerSportsSpider import KSGlobals


class WinPercentageCalculator:
    """
    WinPercentageCalculator class that computes the win percentages of the teams involved in a game,
    given the win-loss-tie statistics of all the spreads involved
    """
    def __init__(self, sport_name, time_period, verbose=True):
        """
        Constructor for the WinPercentageCalculator class - initializes instances of the class and the
        attributes of the created object
        """
        self.sport_name = sport_name  # initialize the attributes of this object
        self.time_period = time_period
        self.verbose = verbose

        self.overall_csv = \
            FileIO.read_csv(
                self.sport_name + " " + VIGlobals.OVERALL_CSV_SUFFIX + " (" + str(self.time_period) + ").csv"
            )  # read the overall csv

        self.ks_csv = \
            FileIO.read_csv(
                self.sport_name + " " + KSGlobals.KS_CSV_SUFFIX + " (" + str(self.time_period) + ").csv"
            )  # read the ks csv containing all the spreads

    def compute_win_percentages(self, weight_function, coefficients, weight_fn_str):
        """
        Given a weight function type (identity, polynomial or exponential), the coefficients of the weight
        function and the string representation of the weight function, computes the win percentages of all
        games in the overall csv and writes the resulting csv to memory
        """
        target_csv_name = \
            " ".join(list([
                self.get_sport_name(),
                WPGlobals.FINAL_KS_CSV_SUFFIX,
                "(" + ", ".join(list([str(self.get_time_period()), weight_fn_str])) + ").csv"
            ]))  # construct the name of the target csv

        overall_csv = self.get_overall_csv()  # get the overall and the killersports csv
        ks_csv = self.get_ks_csv()

        target_csv = list([WPGlobals.FINAL_KS_CSV_HEADER])  # initialize the target csv data matrix

        for idx in range(1, len(overall_csv)):  # for all rows in the overall csv
            target_csv.append(list(overall_csv[idx]))  # add a duplicate row to the target csv

        for row_idx in range(2, len(ks_csv), 3):  # for every game
            # retrieve the favorite, underdog and spacer rows from the killersports csv
            fav_ks_row = ks_csv[row_idx]
            dog_ks_row = ks_csv[row_idx + 1]
            ks_spacer_row = ks_csv[row_idx + 2]

            preprocessed_fav_ks_row = list()  # initialize the new favorite and underdog rows
            preprocessed_dog_ks_row = list()

            fav_spread_map = dict({})  # initialize the favorite and underdog spread maps
            dog_spread_map = dict({})

            self.display(row_idx)
            self.display(fav_ks_row)
            self.display(dog_ks_row)
            self.display(ks_spacer_row)

            for element_idx in range(3, len(fav_ks_row)):  # for every spread in the favorite row
                # retrieve the spread element from both the favorite and underdog rows
                fav_ks_element, dog_ks_element = fav_ks_row[element_idx], dog_ks_row[element_idx]
                # if the elements are not null strings
                if fav_ks_row[element_idx] != '' and dog_ks_row[element_idx] != '':
                    fav_spread, fav_wlt = fav_ks_element.split(';')  # separate the spread from the win-loss-tie stats
                    dog_spread, dog_wlt = dog_ks_element.split(';')
                    # if the favorite and underdog spreads are equal
                    if abs(float(fav_spread)) == abs(float(dog_spread)):
                        preprocessed_fav_ks_row.append(fav_ks_element)  # add the spread element to the rows
                        preprocessed_dog_ks_row.append(dog_ks_element)

            # for every spread element in the preprocessed row
            for element_idx in range(len(preprocessed_fav_ks_row)):
                fav_ks_element, dog_ks_element = preprocessed_fav_ks_row[element_idx], preprocessed_dog_ks_row[
                    element_idx]  # retrieve the spread element from both the favorite and underdog rows
                fav_spread, fav_wlt = fav_ks_element.split(';')  # separate the spread from the win-loss-tie stats
                dog_spread, dog_wlt = dog_ks_element.split(';')

                # parse out the win-loss-tie stats separately
                fav_wlt = [float(element) for element in fav_wlt.split('-')]
                dog_wlt = [float(element) for element in dog_wlt.split('-')]

                if fav_wlt[2] == 0:  # if the win-loss-tie data is non-existent
                    fav_win_pct = 0.50  # assume equal chances of winning
                    dog_win_pct = 0.50
                else:  # otherwise
                    fav_win_pct = fav_wlt[0] / fav_wlt[2]  # compute the win percentage
                    dog_win_pct = dog_wlt[0] / dog_wlt[2]

                # populate spread map
                # if the spread is not already in the favorite spread map
                if float(fav_spread) not in fav_spread_map.keys():
                    fav_spread_map[float(fav_spread)] = tuple((1, fav_win_pct))  # add the spread and the pair
                else:  # otherwise
                    current_fav_freq = fav_spread_map[float(fav_spread)][0]  # get the current pair
                    fav_spread_map[float(fav_spread)] = tuple((current_fav_freq + 1, fav_win_pct))  # update the pair

                # if the spread is not already in the underdog spread map
                if float(dog_spread) not in dog_spread_map.keys():
                    dog_spread_map[float(dog_spread)] = tuple((1, dog_win_pct))  # add the spread and the pair
                else:  # otherwise
                    current_dog_freq = dog_spread_map[float(dog_spread)][0]  # get the current pair
                    dog_spread_map[float(dog_spread)] = tuple((current_dog_freq + 1, dog_win_pct))  # update the pair

            if len(fav_spread_map.keys()) != 0:  # if there are elements in the maps
                # compute the win percentages for the favorite and the underdog
                final_fav_win_pct = \
                    WinPercentageCalculator.compute_weighted_mean(fav_spread_map, weight_function, coefficients)
                final_dog_win_pct = \
                    WinPercentageCalculator.compute_weighted_mean(dog_spread_map, weight_function, coefficients)

                target_csv[row_idx].append(str(final_fav_win_pct))  # append the two win percentages to the row
                target_csv[row_idx + 1].append(str(final_dog_win_pct))
            else:  # otherwise display the rows thus far
                self.display(row_idx)
                self.display(fav_ks_row)
                self.display(dog_ks_row)
                self.display(ks_spacer_row)
                self.display('\n')

        FileIO.write_csv(target_csv, target_csv_name)  # store the target csv to memory

    @staticmethod
    def compute_weighted_mean(data_map, weight_function, coefficients):
        """
        Given a map of spreads mapping to pairs of number of occurrences and the corresponding win percentage,
        the type of weight function (identity, polynomial or exponential) and the coefficients of the weight
        function, computes and returns the weighted average of all the win percentages
        """
        weighted_sum = 0.0  # initialize the numerator to zero
        sum_of_weights = 0.0  # initialize the denominator to zero
        for key in data_map.keys():  # for every spread in the map
            freq, value = data_map[key]  # unpack the frequency and win percentage values
            weighted_sum += weight_function(freq, coefficients) * value  # add to the numerator
            sum_of_weights += weight_function(freq, coefficients)  # add to the denominator
        return float(weighted_sum) / sum_of_weights  # compute the weighted average

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

    def get_verbose(self):
        """
        Returns the verbose option
        """
        return self.verbose  # return the verbose option

    def get_overall_csv(self):
        """
        Returns the overall csv
        """
        return self.overall_csv  # return the overall csv

    def get_ks_csv(self):
        """
        Returns the killersports csv
        """
        return self.ks_csv  # return the killersports csv

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

    def set_verbose(self, verbose):
        """
        Given a new verbose option, sets the current verbose option as the new verbose option
        """
        self.verbose = verbose  # set the current verbose option as the new verbose option

    def set_overall_csv(self, overall_csv):
        """
        Given a new overall csv, sets the current overall csv as the new overall csv
        """
        self.overall_csv = overall_csv  # set the current overall csv as the new overall csv

    def set_ks_csv(self, ks_csv):
        """
        Given a new killersport csv, sets the current killersport csv as the new killersport csv
        """
        self.ks_csv = ks_csv  # set the current killersport csv as the new killersport csv
