from FileIO import FileIO
from EVGlobals import EVGlobals
from WinPercentageCalculator import WPGlobals


class EVCalculator:
    """
    EVCalculator class that computes the expected values (ev) of the teams involved in a game, given
    their respective win percentages
    """
    def __init__(self, sport_name, time_period, weight_fn_str, verbose=True):
        """
        Constructor for the EVCalculator class - initializes instances of the class and the attributes
        of the created object
        """
        self.sport_name = sport_name  # initialize the attributes of this object
        self.time_period = time_period
        self.weight_fn_str = weight_fn_str
        self.verbose = verbose

        self.final_ks_csv = \
            FileIO.read_csv(
                " ".join(list([
                    self.get_sport_name(),
                    WPGlobals.FINAL_KS_CSV_SUFFIX,
                    "(" + ", ".join(list([str(self.get_time_period()), self.get_weight_fn_str()])) + ").csv"
                ]))
            )  # read the ks csv containing all the spreads

    def compute_ev(self):
        """
        Computes the expected values of all teams participating in games in the final killersport csv and
        writes the resulting csv to memory
        """
        ev_csv_filename = \
            " ".join(
                list([
                    self.get_sport_name(),
                    EVGlobals.EV_CSV_SUFFIX,
                    "(" + ", ".join(list([str(self.get_time_period()), self.get_weight_fn_str()])) + ").csv"
                ])
            )  # specify the ev csv filename

        ev_csv = list([EVGlobals.EV_CSV_HEADER, list()])  # initialize the matrix for the ev csv

        final_ks_csv = self.get_final_ks_csv()  # get the final killersports csv

        for row_index in range(2, len(final_ks_csv), 3):  # for every game in the final killersports csv matrix
            fav_row = list(final_ks_csv[row_index])  # get the favorite, underdog and spacer rows
            dog_row = list(final_ks_csv[row_index + 1])
            spacer_row = list(final_ks_csv[row_index + 2])

            fav_payout = float(fav_row[7])  # get the favorite and underdog payouts
            dog_payout = float(dog_row[7])

            fav_win_pct = float(fav_row[8])  # get the favorite and underdog win percentages
            dog_win_pct = float(dog_row[8])

            fav_ev = fav_payout * fav_win_pct - (1 - fav_win_pct)  # compute the favorite and underdog expected values
            dog_ev = dog_payout * dog_win_pct - (1 - dog_win_pct)

            # append the computed expected values to the end of the favorite and underdog rows
            fav_row.append(str(fav_ev))
            dog_row.append(str(dog_ev))

            ev_csv.append(fav_row)  # add the new favorite, underdog and spacer rows
            ev_csv.append(dog_row)
            ev_csv.append(spacer_row)

        FileIO.write_csv(ev_csv_filename, ev_csv)  # write the resulting ev csv to memory

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

    def get_final_ks_csv(self):
        """
        Returns the final killersports csv
        """
        return self.final_ks_csv  # return the final killersports csv

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

    def set_final_ks_csv(self, final_ks_csv):
        """
        Given a new final killersport csv, sets the current final killersport csv as the new final killersport csv
        """
        self.final_ks_csv = final_ks_csv  # set the current final killersport csv as the new final killersport csv
