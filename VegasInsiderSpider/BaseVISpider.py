from FileIO import FileIO
from VIGlobals import VIGlobals


class BaseVISpider:
    """
    BaseVISpider class that contains base attributes and methods shared by the WeeklyVISpider and DailyVISpider
    classes, that scrape the vegasinsider.com website in order to acquire sports betting data
    """
    def __init__(self, target_csv, webdriver_path, branch_url='', read_csv=False, time_threshold=1, verbose=True):
        """
        Constructor for the BaseVISpider class - initializes instances of the class and the attributes
        of the created object
        """
        self.target_csv = target_csv  # initialize the attributes of this object
        self.webdriver_path = webdriver_path
        self.base_url = 'http://www.vegasinsider.com/'
        self.branch_url = branch_url
        self.read_csv = read_csv
        self.time_threshold = time_threshold
        self.verbose = verbose

        # if the read_csv option is True, read the csv stored in the target_csv path
        if self.read_csv: self.csv_matrix = FileIO.read_csv(self.target_csv)
        else: self.csv_matrix = list([list(VIGlobals.OVERALL_CSV_HEADER), list()])  # otherwise initialize a new csv matrix

    def extract_moneyline(self, ml_table_row, team1_len, team2_len):
        """
        Given a row of data from the vegasinsider.com website for a particular game and the lengths of the
        abbreviated strings of the two team names, parses the appropriate strings in the row to extract and
        return the moneylines for the two teams competing in the game
        """
        away_ml, home_ml = ml_table_row[2], ml_table_row[3]  # access the appropriate strings

        # check if the first input length of team name abbreviation fits the moneyline string for
        # the away team
        if (away_ml[:team1_len].isalpha() and
                (self.is_numerical(away_ml[team1_len + 1:]) or
                         away_ml[team1_len:] == 'PK' or
                         away_ml[team1_len:] == '0') and
                home_ml[:team2_len].isalpha() and
                (self.is_numerical(home_ml[team2_len + 1:]) or
                         home_ml[team2_len:] == 'PK' or home_ml[team2_len:] == '0')):
            # if so, return the parsed strings containing only the moneylines for the away and home teams
            return away_ml[team1_len:], home_ml[team2_len:]
        # check if the second input length of team name abbreviation fits the moneyline string for
        # the away team
        elif away_ml[:team2_len].isalpha() and \
                (self.is_numerical(away_ml[team2_len + 1:]) or
                         away_ml[team2_len:] == 'PK' or
                         away_ml[team2_len:] == '0') and \
                home_ml[:team1_len].isalpha() and \
                (self.is_numerical(home_ml[team1_len + 1:]) or
                         home_ml[team1_len:] == 'PK' or home_ml[team1_len:] == '0'):
            # if so, return the parsed strings containing only the moneylines for the away and home teams
            return away_ml[team2_len:], home_ml[team1_len:]

    def extract_spreads(self, ps_table_row, team1_len, team2_len):
        """
        Given a row of data from the vegasinsider.com website for a particular game and the lengths of the
        abbreviated strings of the two team names, parses the appropriate strings in the row to extract and
        return the point spreads for the two teams competing in the game
        """
        # check if the appropriate strings in the input row are of the correct format - if not, return False
        if len(ps_table_row[4].split()) != 2 or len(ps_table_row[5].split()) != 2: return False

        away_ps, home_ps = ps_table_row[4].split()[0], ps_table_row[5].split()[0]  # access the appropriate strings

        # check if the first input length of team name abbreviation fits the point spread string for
        # the away team
        if (away_ps[:team1_len].isalpha() and
                (self.is_numerical(away_ps[team1_len + 1:]) or
                         away_ps[team1_len:] == 'PK' or
                         away_ps[team1_len:] == '0') and
                home_ps[:team2_len].isalpha() and
                (self.is_numerical(home_ps[team2_len + 1:]) or
                         home_ps[team2_len:] == 'PK' or
                         home_ps[team2_len:] == '0')):
            # if so, return the parsed strings containing only the point spread for the away and home teams
            return away_ps[team1_len:], home_ps[team2_len:]
        # check if the second input length of team name abbreviation fits the point spread string for
        # the away team
        elif away_ps[:team2_len].isalpha() and \
                (self.is_numerical(away_ps[team2_len + 1:]) or
                         away_ps[team2_len:] == 'PK' or
                         away_ps[team2_len:] == '0') and \
                home_ps[:team1_len].isalpha() and \
                (self.is_numerical(home_ps[team1_len + 1:]) or
                         home_ps[team1_len:] == 'PK' or
                         home_ps[team1_len:] == '0'):
            # if so, return the parsed strings containing only the point spread for the away and home teams
            return away_ps[team2_len:], home_ps[team1_len:]

    @staticmethod
    def determine_ml_desired_table_row(desired_table_rows):
        """
        Given a list of desired table rows within the correct time range after the time threshold has been
        accounted for, checks and returns the most recent input row with uncensored moneyline data
        """
        censor = 'XX'  # specify the string for censored rows
        # for every input row index in the chronologically descending order
        for row_index in range(len(desired_table_rows) - 1, -1, -1):
            uncensored = True  # initialize boolean to indicate if the row is censored or not
            row_elements = desired_table_rows[row_index]  # access the row
            fav_ml, dog_ml = row_elements[2], row_elements[3]  # access the moneyline strings
            # check if the moneyline is censored or not
            uncensored = uncensored and (censor not in fav_ml) and (censor not in dog_ml)
            if uncensored: return row_elements  # if the moneyline is uncensored, return it

    def determine_ps_desired_table_row(self, desired_table_rows):
        """
        Given a list of desired table rows within the correct time range after the time threshold has been
        accounted for, checks and returns the most recent input row with uncensored point spread data
        """
        censor = 'XX'  # specify the string for censored rows
        # for every input row index in the chronologically descending order
        for row_index in range(len(desired_table_rows) - 1, -1, -1):
            uncensored = True  # initialize boolean to indicate if the row is censored or not
            row_elements = desired_table_rows[row_index]  # access the row
            fav_ps, dog_ps = row_elements[4], row_elements[5]  # access the point spread strings
            fav_ps, dog_ps = fav_ps.split()[0], dog_ps.split()[0]
            # check if the point spread is censored or not
            uncensored = uncensored and (censor not in fav_ps) and (censor not in dog_ps)
            if uncensored: return row_elements  # if the point spread is uncensored, return it

    @staticmethod
    def compute_payout(moneyline):
        """
        Given the moneyline for a certain team participating in a certain game, computes and returns the
        payout corresponding to the input moneyline
        """
        # if the input moneyline is for an underdog...
        if float(moneyline) < 0: return -100.00 / float(moneyline)
        else: return float(moneyline) / 100.00  # ... vs if the input moneyline is for the favorite

    def is_before_game(self, table_row_elements, game_date, game_time):
        """
        Given a list of rows of game data published at different times and the date and time of the game,
        returns true if the data was published before the start of the game and False otherwise
        """
        # access the date and time of the published data
        row_date, row_time = table_row_elements[0], table_row_elements[1]
        game_date = self.rectify_date_format(game_date)  # parse the input game date into a better format
        # parse the row date information to extract the month and day of the published data
        row_month, row_day = [int(num) for num in row_date.split('/')]

        # more parsing to express the menth and day strings of the published data in the right format
        if row_month == 12 and int(game_date[4:6]) == 1:
            row_year = str(int(game_date[:4]) - 1)
            row_month, row_day = row_date.split('/')
        else:
            row_year = game_date[:4]
            row_month, row_day = row_date.split('/')

        # construct the date of the published data in the required format
        row_date = row_year + row_month + row_day

        # compare the dates of the published data and the game
        return self.compare_dates(row_date, row_time, game_date, game_time)

    def has_money_line(self, table_row_elements, team1_len, team2_len):
        """
        Given a row of data from the vegasinsider.com website for a particular game and the lengths of the
        abbreviated strings of the two team names, parses the appropriate strings in the row to determine
        whether the input row of published data contains the moneylines for the two teams competing in the game
        """
        away_ml, home_ml = table_row_elements[2], table_row_elements[3]  # access the appropriate strings

        # check if the first input length of team name abbreviation fits the moneyline string for
        # the away team
        if (away_ml[:team1_len].isalpha() and
                (self.is_numerical(away_ml[team1_len + 1:]) or
                         away_ml[team1_len:] == 'PK' or
                         away_ml[team1_len:] == '0') and
                home_ml[:team2_len].isalpha() and
                (self.is_numerical(home_ml[team2_len + 1:]) or
                         home_ml[team2_len:] == 'PK' or
                         home_ml[team2_len:] == '0')):
            return True  # if so, return True
        # check if the second input length of team name abbreviation fits the moneyline string for
        # the away team
        elif away_ml[:team2_len].isalpha() and \
                (self.is_numerical(away_ml[team2_len + 1:]) or
                         away_ml[team2_len:] == 'PK' or
                         away_ml[team2_len:] == '0') and \
                home_ml[:team1_len].isalpha() and \
                (self.is_numerical(home_ml[team1_len + 1:]) or
                         home_ml[team1_len:] == 'PK' or
                         home_ml[team1_len:] == '0'):
            return True  # if so, return True

        return False  # otherwise, return False

    def has_point_spread(self, table_row_elements, team1_len, team2_len):
        """
        Given a row of data from the vegasinsider.com website for a particular game and the lengths of the
        abbreviated strings of the two team names, parses the appropriate strings in the row to extract and
        return the point spreads for the two teams competing in the game
        """
        # check if the appropriate strings in the input row are of the correct format - if not, return False
        if len(table_row_elements[4].split()) != 2 or len(table_row_elements[5].split()) != 2: return False

        # access the appropriate strings
        away_pl, home_pl = table_row_elements[4].split()[0], table_row_elements[5].split()[0]

        # check if the first input length of team name abbreviation fits the point spread string for
        # the away team
        if (away_pl[:team1_len].isalpha() and
                (self.is_numerical(away_pl[team1_len + 1:]) or
                         away_pl[team1_len:] == 'PK' or
                         away_pl[team1_len:] == '0') and
                home_pl[:team2_len].isalpha() and
                (self.is_numerical(home_pl[team2_len + 1:]) or
                         home_pl[team2_len:] == 'PK' or
                         home_pl[team2_len:] == '0')):
            return True  # if so, return True
        # check if the second input length of team name abbreviation fits the point spread string for
        # the away team
        elif away_pl[:team2_len].isalpha() and \
                (self.is_numerical(away_pl[team2_len + 1:]) or
                         away_pl[team2_len:] == 'PK' or
                         away_pl[team2_len:] == '0') and \
                home_pl[:team1_len].isalpha() and \
                (self.is_numerical(home_pl[team1_len + 1:]) or
                         home_pl[team1_len:] == 'PK' or
                         home_pl[team1_len:] == '0'):
            return True  # if so, return True

        return False  # otherwise, return False

    @staticmethod
    def is_numerical(string):
        """
        Given a python string, returns True is the string is numerical and False otherwise
        """
        str_elements = string.split('.')  # split based on the decimal point

        for element in str_elements:  # for every element
            if not element.isnumeric(): return False  # if the element is not numerical, return False

        return True  # otherwise, return True since the string is numerical

    def determine_underdog_ml(self, table_row, away_team, home_team, team_abbr):
        """
        Given a row of published betting data, the names of the participating teams and a dictionary mapping
        team names to their abbreviations, returns True if the away team moneyline is for the favorite and
        False otherwise
        """
        fav_ml, dog_ml = table_row[2], table_row[3]  # access the moneyline strings

        # parse the moneyline string to extract the favorite team abbreviation, using the away
        # team abbreviation length
        if (fav_ml[:len(team_abbr[away_team])].isalpha() and (
                        self.is_numerical(fav_ml[len(team_abbr[away_team]) + 1:]) or fav_ml[len(
                        team_abbr[away_team]):] == 'PK' or fav_ml[len(team_abbr[away_team]):] == '0') and
                dog_ml[:len(team_abbr[home_team])].isalpha() and (
                        self.is_numerical(dog_ml[len(team_abbr[home_team]) + 1:]) or dog_ml[len(
                        team_abbr[home_team]):] == 'PK' or dog_ml[len(team_abbr[home_team]):] == '0')):
            fav_abbr = fav_ml[:len(team_abbr[away_team])]
            # if the favorite team abbreviation matches the home team abbreviation, return False
            if fav_abbr == team_abbr[home_team]: return False
            else: return True  # otherwise, return True
        # parse the moneyline string to extract the favorite team abbreviation, using the home
        # team abbreviation length
        elif fav_ml[:len(team_abbr[home_team])].isalpha() and (
                        self.is_numerical(fav_ml[len(team_abbr[home_team]) + 1:]) or fav_ml[len(
                        team_abbr[home_team]):] == 'PK' or fav_ml[len(team_abbr[home_team]):] == '0') and \
                dog_ml[:len(team_abbr[away_team])].isalpha() and (
                        self.is_numerical(dog_ml[len(team_abbr[away_team]) + 1:]) or dog_ml[len(
                        team_abbr[away_team]):] == 'PK' or dog_ml[len(team_abbr[away_team]):] == '0'):
            fav_abbr = fav_ml[:len(team_abbr[home_team])]
            # if the favorite team abbreviation matches the home team abbreviation, return False
            if fav_abbr == team_abbr[home_team]: return False
            else: return True  # otherwise, return True

    def determine_underdog_ps(self, table_row, away_team, home_team, team_abbr):
        """
        Given a row of published betting data, the names of the participating teams and a dictionary mapping
        team names to their abbreviations, returns True if the away team point spread is for the favorite and
        False otherwise
        """
        fav_ps, dog_ps = table_row[4].split()[0], table_row[5].split()[0]  # access the point spread strings

        # parse the point spread string to extract the favorite team abbreviation, using the away
        # team abbreviation length
        if (fav_ps[:len(team_abbr[away_team])].isalpha() and (
                        self.is_numerical(fav_ps[len(team_abbr[away_team]) + 1:]) or fav_ps[len(
                        team_abbr[away_team]):] == 'PK' or fav_ps[len(team_abbr[away_team]):] == '0') and
                dog_ps[:len(team_abbr[home_team])].isalpha() and (
                        self.is_numerical(dog_ps[len(team_abbr[home_team]) + 1:]) or dog_ps[len(
                        team_abbr[home_team]):] == 'PK' or dog_ps[len(team_abbr[home_team]):] == '0')):
            fav_abbr = fav_ps[:len(team_abbr[away_team])]
            # if the favorite team abbreviation matches the home team abbreviation, return False
            if fav_abbr == team_abbr[home_team]: return False
            else: return True  # otherwise, return True
        # parse the point spread string to extract the favorite team abbreviation, using the home
        # team abbreviation length
        elif fav_ps[:len(team_abbr[home_team])].isalpha() and (
                        self.is_numerical(fav_ps[len(team_abbr[home_team]) + 1:]) or fav_ps[len(
                        team_abbr[home_team]):] == 'PK' or fav_ps[len(team_abbr[home_team]):] == '0') and \
                dog_ps[:len(team_abbr[away_team])].isalpha() and (
                        self.is_numerical(dog_ps[len(team_abbr[away_team]) + 1:]) or dog_ps[len(
                        team_abbr[away_team]):] == 'PK' or dog_ps[len(team_abbr[away_team]):] == '0'):
            fav_abbr = fav_ps[:len(team_abbr[home_team])]
            # if the favorite team abbreviation matches the home team abbreviation, return False
            if fav_abbr == team_abbr[home_team]: return False
            else: return True  # otherwise, return True

    def determine_underdog_consensus(self, underdog_mls, underdog_pss):
        """
        Given two lists of binaries where True indicates underdog and False indicates favorite, returns True
        if the majority voting is True and False otherwise
        """
        # compute the number of True elements
        num_true = sum([int(element) for element in underdog_mls if element != None]) + \
                   sum([int(element) for element in underdog_pss if element != None])

        # if the number of True elements is more than 50 percent, return True
        if num_true >= int((len(underdog_mls) + len(underdog_pss)) / 2): return True
        else: return False  # otherwise, return False

    @staticmethod
    def handle_moneyline_pk(payout):
        """
        Given a moneyline string, handles the PK case and returns the corrected moneyline string
        """
        if payout == 'PK': payout = str(100)  # if the moneyline string contains the PK case, return 100 as a string
        return payout  # otherwise, return the input moneyline string

    @staticmethod
    def handle_spread_pk(spread):
        """
        Given a point spread string, handles the PK case and returns the corrected point spread string
        """
        if spread == 'PK': spread = str(0)  # if the point spread string contains the PK case, return 0 as a string
        return spread  # otherwise, return the input point spread string

    def rewind_time(self, original_date, original_time):
        """
        Given a date and time, rewinds the time by the number of hours specified by the time_threshold
        attribute and returns the updated date and time
        """
        rewound_date, rewound_time = '', ''  # initialize empty strings for the rewound date and time
        original_month, original_day = original_date.split('/')  # retrieve the original month and day
        original_hour, original_min_meridiem = original_time.split(':')  # retrieve the hour, minute and meridiem
        # separate the original minute and meridiem
        original_min, original_meridiem = \
            original_min_meridiem[:len(original_min_meridiem) - 2], \
            original_min_meridiem[len(original_min_meridiem) - 2:]

        if int(original_hour) == 12:  # if the input hour is 12
            rewound_meridiem = self.flip_meridiem(original_meridiem)  # flip the meridiem
            if rewound_meridiem == 'am':  # if the flipped meridiem is am
                rewound_date = original_date  # the original date is the rewound date
            elif rewound_meridiem == 'pm':  # if the flipped meridiem is pm
                if int(original_day) == 1:  # if it is the first day of the month
                    if int(original_month) == 1:  # if it is the first month of the year
                        rewound_month = str('12')  # set the rewound month to December
                    else:  # otherwise, decrement the month string
                        rewound_month = str(int(original_month) - 1)
                    # choose the last day of the rewound month
                    rewound_day = str(VIGlobals.NUM_DAYS[VIGlobals.NUM_TO_MONTHS[int(rewound_month)]])
                else:  # otherwise, simply decrement the original day
                    rewound_day = str(int(original_day) - 1)
                    rewound_month = original_month  # the rewound month is the original month
                if len(rewound_day) == 1:  # if the rewound day string contains a single digit
                    rewound_day = '0' + rewound_day  # prepend a 0 to the string in compliance with the format
                if len(rewound_month) == 1:  # if the rewound month contains a single digit
                    rewound_month = '0' + rewound_month  # prepend a 0 to the string in compliance with the format
                rewound_date = rewound_month + '/' + rewound_day  # construct the rewound date string
            rewound_hour = str(int(original_hour) - self.get_time_threshold())  # rewind the hour
        else:  # if the input hour is not 12
            rewound_date = original_date  # rewound date and meridiem stays constant
            rewound_meridiem = original_meridiem
            if int(original_hour) == 1:  # if the original hour is 1
                rewound_hour = '12'  # the rewound hour must be 12
            else:  # otherwise, simply rewind by the number of hours specified by the time_threshold attribute
                rewound_hour = str(int(original_hour) - self.get_time_threshold())

        rewound_min = original_min  # the rewound minute is simply the original minute
        rewound_time = rewound_hour + ':' + rewound_min + rewound_meridiem  # construct the rewound time string

        return rewound_date, rewound_time  # return the rewound date and time strings

    @staticmethod
    def flip_meridiem(meridiem):
        """
        Given a meridiem string, returns a string containing the opposite meridiem
        """
        if meridiem == 'pm': return 'am'  # if the string is "pm", return "am"
        return 'pm'  # otherwise, return "pm"

    def is_within_time_period(self, row_date, row_time, game_date, game_time):
        """
        Given the date and time of published betting data and the date and time of the game, returns True
        if the rewound date and time is chronologically before and the game date and time is chronologically
        after the published data date and time and False otherwise
        """
        game_month, game_day = [int(num) for num in game_date.split('/')]  # extract the game month and day
        game_hour, game_min_meridiem = game_time.split(':')  # extract the game hour and minute and meridiem
        # extract the game minute and meridiem
        game_min, game_meridiem = \
            game_min_meridiem[:len(game_min_meridiem) - 2], \
            game_min_meridiem[len(game_min_meridiem) - 2:]

        # construct the rewound date and time
        rewound_date, rewound_time = self.rewind_time(game_date, game_time)

        # extract the row month and day
        row_month, row_day = [int(num) for num in row_date.split('/')]
        # extract the rewound month and day
        rewound_month, rewound_day = [int(num) for num in rewound_date.split('/')]

        row_hour, row_min_meridiem = row_time.split(':')  # extract the row hour and min and meridiem
        # extract the row minute and meridiem
        row_min, row_meridiem = \
            row_min_meridiem[:len(row_min_meridiem) - 2], \
            row_min_meridiem[len(row_min_meridiem) - 2:]
        row_hour, row_min = int(row_hour), int(row_min)  # extract the row hour and minute

        # extract the rewound hour and minute and meridiem
        rewound_hour, rewound_min_meridiem = rewound_time.split(':')
        # extract the rewound minute and meridiem
        rewound_min, rewound_meridiem = \
            rewound_min_meridiem[:len(rewound_min_meridiem) - 2], \
            rewound_min_meridiem[len(rewound_min_meridiem) - 2:]
        rewound_hour, rewound_min = int(rewound_hour), int(rewound_min)  # extract the rewound hour and minute

        # check if rewound date and time is before row date and time
        if int(row_month) < int(rewound_month):  # if the row month is before the rewound month
            rewound_is_before = False  # rewound date and time is not before
        elif int(row_month) > int(rewound_month):  # if the row month is after the rewound month
            rewound_is_before = True  # rewound date and time is before
        else:  # otherwise
            if int(row_day) < int(rewound_day):  # if the row day is before the rewound day
                rewound_is_before = False  # rewound date and time is not before
            elif int(row_day) > int(rewound_day):  # if the row day is after the rewound day
                rewound_is_before = True  # rewound date and time is before
            else:  # otherwise
                # if the row meridiem is am but the rewound meridiem is pm
                if row_meridiem == 'am' and rewound_meridiem == 'pm':
                    rewound_is_before = False  # the rewound date and time is not before
                # if the row meridiem is pm but the rewound meridiem is am
                elif row_meridiem == 'pm' and rewound_meridiem == 'am':
                    rewound_is_before = True  # the rewound date and time is before
                else:  # otherwise
                    mod_row_hour = int(row_hour) % 12  # get the mod row hour
                    mod_rewound_hour = int(rewound_hour) % 12  # get the mod rewound hour
                    # if the mod row hour is before the mod rewound hour
                    if int(mod_row_hour) < int(mod_rewound_hour):
                        rewound_is_before = False  # the rewound date and time is before
                    # if the mod row hour is after the mod rewound hour
                    elif int(mod_row_hour) > int(mod_rewound_hour):
                        rewound_is_before = True  # the rewound date and time is before
                    else:  # otherwise
                        if int(row_min) < int(rewound_min):  # if the row minute is before the rewound minute
                            rewound_is_before = False  # the rewound date and time is before
                        else:  # otherwise
                            rewound_is_before = True  # otherwise, the rewound date and time is after

        # check if original game date and time is after row date and time
        if int(game_month) < int(row_month):  # if the game month is before the row month
            game_is_after = False  # the game date and time is not after
        elif int(game_month) > int(row_month):  # if the game month is after the row month
            game_is_after = True  # the game date and time is after
        else:  # otherwise
            if int(game_day) < int(row_day):  # if the game day is before the row day
                game_is_after = False  # the game date and time is not after
            elif int(game_day) > int(row_day):  # if the game day is after the row day
                game_is_after = True  # the game date and time is after
            else:  # otherwise
                # if the game meridiem is am and the row meridiem is pm
                if game_meridiem == 'am' and row_meridiem == 'pm':
                    game_is_after = False  # the game date and time is not after
                # if the game meridiem is pm and the row meridiem is am
                elif game_meridiem == 'pm' and row_meridiem == 'am':
                    game_is_after = True  # the game date and time is after
                else:  # otherwise
                    mod_game_hour = int(game_hour) % 12  # compute the mod game hour
                    mod_row_hour = int(row_hour) % 12  # compute the mod row hour
                    if int(mod_game_hour) < int(mod_row_hour):  # if the mod game hour is before the mod row hour
                        game_is_after = False  # the game date and time is not after
                    elif int(mod_game_hour) > int(mod_row_hour):  # if the mod game hour is after the mod row hour
                        game_is_after = True  # the game date and time is after
                    else:  # otherwise
                        if int(game_min) < int(row_min):  # if the game minute is before the row minute
                            game_is_after = False  # the game date and time is not after
                        else:  # otherwise
                            game_is_after = True  # the game date and time is after

        # return True if the rewound date and time is before and the game date and time is after and
        # False otherwise
        return rewound_is_before and game_is_after

    @staticmethod
    def compare_dates(row_date, row_time, game_date, game_time):
        """
        Given the published betting data date and time and the game date and time, returns True if the
        published data is chronologically before the game and False otherwise
        """
        # extract the row year, month and day
        row_year, row_month, row_day = int(row_date[:4]), int(row_date[4:6]), int(row_date[6:])
        # extract the game year, month and day
        game_year, game_month, game_day = int(game_date[:4]), int(game_date[4:6]), int(game_date[6:])

        # extract the row hour and min and row meridiem
        row_hhmin, row_meridiem = row_time[:len(row_time) - 2], row_time[len(row_time) - 2:]
        game_hhmin, game_meridiem = game_time.split()  # extract the game hour and min and game meridiem
        game_meridiem = game_meridiem.lower()

        # extract the row hour and the row minute
        row_hour, row_min = [int(num) for num in row_hhmin.split(':')]
        game_hour, game_min = [int(num) for num in game_hhmin.split(':')]  # extract the game hour and minute

        # if the row year is before the game year, return True
        if row_year < game_year:
            return True
        elif row_year > game_year:  # if the row year is after the game year, return False
            return False
        else:  # otherwise
            if row_month < game_month:  # if the row month is before the game month, return True
                return True
            elif row_month > game_month:  # if the row month is after the game month, return False
                return False
            else:  # otherwise
                if row_day < game_day:  # if the row day is before the game day, return True
                    return True
                elif row_day > game_day:  # if the row day is after the game day, return False
                    return False
                else:  # otherwise
                    # if the row meridiem is am and the game meridiem is pm, return True
                    if row_meridiem == 'am' and game_meridiem == 'pm':
                        return True
                    # if the row meridiem is pm and the game meridiem is am, return False
                    elif row_meridiem == 'pm' and game_meridiem == 'am':
                        return False
                    else:  # otherwise
                        # if the row hour is before the game hour (account for the first hour after midnight)
                        # return True
                        if row_hour < game_hour or (row_hour == 12 and game_hour < row_hour):
                            return True
                        # if the row hour is after the game hour (account for the first hour after midnight)
                        # return False
                        elif row_hour > game_hour or (row_hour == 12 and game_hour > row_hour):
                            return False
                        else:  # otherwise
                            # if the row minute is before or equal to the game minute, return True
                            if row_min <= game_min:
                                return True
                            else:  # otherwise, return False
                                return False

    @staticmethod
    def rectify_date_format(footballdb_datestring):
        """
        Given the footballdb date string, reformats and returns the same date string as yymmdd
        """
        correct_datestring = ''  # initialize the  reformatted date string as an empty string

        date_pieces = footballdb_datestring.split(', ')  # split based on a comma followed by a space

        year = date_pieces[len(date_pieces) - 1]  # extract the year, month and day
        month, day = date_pieces[1].split(' ')
        month = str(VIGlobals.MONTHS_TO_NUM[month])

        if len(month) == 1: month = '0' + str(month)  # handle edge cases

        if len(day) == 1: day = '0' + str(day)

        correct_datestring += year + month + day  # construct the reformatted date as yymmdd

        return correct_datestring  # return the reformatted date string

    @staticmethod
    def rectify_date_format2(footballdb_datestring):
        """
        Given the footballdb date string, reformats and returns the same date string as mm/dd
        """
        correct_datestring = ''  # initialize the  reformatted date string as an empty string

        date_pieces = footballdb_datestring.split(', ')  # split based on a comma followed by a space

        month, day = date_pieces[1].split(' ')  # extract the month and day
        month = str(VIGlobals.MONTHS_TO_NUM[month])

        if len(month) == 1: month = '0' + str(month)  # handle edge cases

        if len(day) == 1: day = '0' + str(day)

        correct_datestring += month + '/' + day  # construct the reformatted date as mm/dd

        return correct_datestring  # return the reformatted date string

    @staticmethod
    def rectify_time_format(game_time):
        """
        Given an game time string, changes the format to hh:mm<meridiem> and returns the new string
        """
        # extract the game hour-minute and the meridiem
        game_hhmin, game_meridiem = game_time.split()
        game_meridiem = game_meridiem.lower()  # lowercase the meridiem
        game_hour, game_min = game_hhmin.split(':')  # extract the game hour and minute

        # construct the game time string using the correct format
        rectified_game_time = game_hour + ':' + game_min + game_meridiem

        return rectified_game_time  # return the correctly formatted time string

    def append_to_csv_matrix(self, submatrix):
        """
        Given a submatrix, concatenates the submatrix vertically to the current csv matrix
        """
        csv_matrix = self.get_csv_matrix()  # get the current csv matrix
        csv_matrix += list(submatrix)  # concatenate the submatrix vertically
        self.set_csv_matrix(csv_matrix)  # store the new csv matrix

    def display(self, message):
        """
        Given a message string, prints the message if the verbose option is turned on
        """
        if self.get_verbose():  # if the verbose boolean is set to true
            print(str(message))  # print the input message

    def get_target_csv(self):
        """
        Return the target csv
        """
        return self.target_csv  # return the target csv

    def get_webdriver_path(self):
        """
        Return the webdriver path
        """
        return self.webdriver_path  # return the webdriver path

    def get_base_url(self):
        """
        Return the base url
        """
        return self.base_url  # return the base url

    def get_branch_url(self):
        """
        Return the branch url
        """
        return self.branch_url  # return the branch url

    def get_read_csv(self):
        """
        Return the read csv attribute
        """
        return self.read_csv  # return the read csv attribute

    def get_time_threshold(self):
        """
        Return the time threshold attribute
        """
        return self.time_threshold  # return the time threshold attribute

    def get_verbose(self):
        """
        Return the verbose option
        """
        return self.verbose  # return the verbose option

    def get_csv_matrix(self):
        """
        Return the csv matrix
        """
        return self.csv_matrix  # return the csv matrix

    def set_target_csv(self, target_csv):
        """
        Given a new target csv name, sets the current target csv name as the new target csv name
        """
        self.target_csv = target_csv  # set the current target csv name as the new target csv name

    def set_webdriver_path(self, webdriver_path):
        """
        Given a new webdriver path, sets the current webdriver path as the new webdriver path
        """
        self.webdriver_path = webdriver_path  # set the current webdriver path as the new webdriver path

    def set_branch_url(self, branch_url):
        """
        Given a new branch url, sets the current branch url as the new branch url
        """
        self.branch_url = branch_url  # set the current branch url as the new branch url

    def set_read_csv(self, read_csv):
        """
        Given a new read csv boolean, sets the current read csv boolean as the new current read csv boolean
        """
        self.read_csv = read_csv  # set the current read csv boolean as the new current read csv boolean

    def set_time_threshold(self, time_threshold):
        """
        Given a new time threshold, sets the current time threshold as the new time threshold
        """
        self.time_threshold = time_threshold  # set the current time threshold as the new time threshold

    def set_verbose(self, verbose):
        """
        Given a new verbose option, sets the current verbose option as the new verbose option
        """
        self.verbose = verbose  # set the current verbose option as the new verbose option

    def set_csv_matrix(self, csv_matrix):
        """
        Given a new csv matrix, sets the current csv matrix as the new csv matrix
        """
        self.csv_matrix = csv_matrix  # set the current csv matrix as the new csv matrix
