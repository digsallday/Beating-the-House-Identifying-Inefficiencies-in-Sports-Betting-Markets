from FileIO import FileIO
from KSGlobals import KSGlobals
import traceback
from time import sleep
from pprint import pprint
from selenium import webdriver


class KSSpider:
    """
    KSSpider class that scrapes the killersports.com website in order to acquire win percentages based
    on point spreads
    """
    def __init__(self, target_csv, webdriver_path, branch_url='', read_csv=False, query_timeout=15, ntrials=5,
                 verbose=True):
        """
        Constructor for the KSSpider class - initializes instances of the class and the attributes of
        the created object
        """
        self.target_csv = target_csv  # initialize the attributes of this object
        self.webdriver_path = webdriver_path
        self.base_url = 'http://killersports.com/'
        self.branch_url = branch_url
        self.read_csv = read_csv

        # if the read_csv option is True, read the csv stored in the target_csv path
        if self.read_csv: self.csv_matrix = FileIO.read_csv(self.get_target_csv())
        # otherwise initialize a new csv matrix
        else: self.csv_matrix = list([KSGlobals.FINAL_KS_CSV_HEADER, list()])

        self.query_timeout = query_timeout
        self.ntrials = ntrials
        self.verbose = verbose

    def deploy(self, data_matrix, start_game_index):
        """
        Given the data matrix of games and the starting game index, deploys a spider that visits the
        killersports.com website to acquire the win percentage for each of the two teams playing each
        match and stores all relevant data to memory
        """
        new_data_matrix = self.get_csv_matrix()  # get the current csv matrix

        # for every game
        for game_index in range(start_game_index, len(data_matrix), 3):
            dates = self.extract_dates(new_data_matrix)  # get a list of past dates

            # if the current game was not held in a past date
            if data_matrix[game_index][0] not in dates or game_index == start_game_index:
                fav_spreads_map = dict({})  # reinitialize the data structures
                dog_spreads_map = dict({})

            self.display(dates)  # display the dates and game index
            self.display(game_index)

            fav_row = list(data_matrix[game_index])  # extract the favorite, underdog and spacer row
            dog_row = list(data_matrix[game_index + 1])
            spacer_row = list(data_matrix[game_index + 2])

            current_date = fav_row[0]  # get the date for the current game

            self.display(current_date)
            self.display(fav_row)
            self.display('\n')

            # for every spread in the favorite row
            for spread_index in range(3, len(fav_row)):
                if len(fav_row[spread_index]) > 0:  # if the point spread is not a null string
                    self.display('Favorite')
                    current_spread = float(fav_row[spread_index])  # get the current spread
                    if current_spread not in fav_spreads_map.keys():  # if the win to loss stats are not available
                        driver = webdriver.Chrome(self.get_webdriver_path())  # create a Chrome webdriver
                        url = self.get_base_url() + self.get_branch_url()  # construct the url
                        for trial_idx in range(self.get_ntrials()):  # try the specified number of times
                            try:
                                driver.get(url)  # visit the killersports website

                                sleep(self.get_query_timeout())  # sleep for the specified number of seconds

                                # build the search query
                                query = self.create_exact_query(current_date, current_spread)

                                self.display(query)

                                # find the query box and type in the query
                                text_field = driver.find_element_by_id('sdql')
                                text_field.send_keys(query)

                                # find the query submit button and click it
                                button = driver.find_element_by_name('submit')
                                button.click()

                                # retrieve the win-loss-tie stats for the given point spread
                                su_element = driver.find_element_by_xpath\
                                    ('/html/body/div[@id="content"]/table/tbody/tr[2]/td/table/tbody/tr[1]/td[1]')

                                su_text = str(su_element.text)  # convert the web element to text
                                # parse the text to extract the win-loss-tie stats
                                wlt = [int(num) for num in su_text.split()[0].split('-')]

                                driver.close()  # close the Chrome webdriver

                                sample_size = wlt[0] + wlt[1]  # compute the sample size

                                # include the win-loss-tie stats for the current spread in the favorite row
                                fav_row[spread_index] = fav_row[spread_index] + ';' + str(wlt[0]) + '-' + str(
                                    wlt[1]) + '-' + str(sample_size)

                                # store the win-loss-tie stats for the current spread for both the favorite
                                # and the underdog teams
                                fav_spreads_map[current_spread] = tuple((int(wlt[0]), int(wlt[1])))
                                dog_spreads_map[-current_spread] = tuple((int(wlt[1]), int(wlt[0])))

                                break  # no more trials are required

                            except Exception as e:  # in the case of an Exception
                                self.display('\n')
                                # self.display(fav_row)
                                self.display(traceback.print_exc())
                                self.display('Exception encountered: No games of desired spread found in sample!')
                                self.display('Setting data to null and exiting...')
                                self.display('\n')

                                # if all trials have been exhausted
                                if trial_idx == self.get_ntrials() - 1:
                                    # store the win-loss-tie stats as 0-0-0
                                    fav_row[spread_index] = fav_row[spread_index] + ';' + str('0-0-0')
                                    # dog_row[spread_index] = dog_row[spread_index] + ';' + str('0-0-0')
                                    fav_spreads_map[current_spread] = tuple((0, 0))
                                    dog_spreads_map[-current_spread] = tuple((0, 0))
                                    driver.close()  # close the Chrome webdriver
                    else:  # if the current spread stats have already been scraped
                        # use the stored win-loss-tie stats for current spread
                        fav_win_count, fav_loss_count = fav_spreads_map[current_spread]
                        sample_size = fav_win_count + fav_loss_count
                        fav_row[spread_index] = fav_row[spread_index] + ';' + str(fav_win_count) + '-' + \
                                                str(fav_loss_count) + '-' + str(sample_size)
                        # dog_row[spread_index] = dog_row[spread_index] + ';' + str(fav_loss_count) + '-' + \
                        #                         str(fav_win_count) + '-' + str(sample_size)

                self.display(fav_row)
                self.display(dog_row)
                self.display(spacer_row)
                self.pdisplay(fav_spreads_map)
                self.pdisplay(dog_spreads_map)
                self.display('\n')

            # for every spread in the underdog row
            for spread_index in range(3, len(dog_row)):
                if len(dog_row[spread_index]) > 0:  # if the point spread is not a null string
                    self.display('Underdog')
                    current_spread = float(dog_row[spread_index])  # get the current spread
                    if current_spread not in dog_spreads_map.keys():  # if the win to loss stats are not available
                        driver = webdriver.Chrome(self.get_webdriver_path())  # create a Chrome webdriver
                        url = self.get_base_url() + self.get_branch_url()  # construct the url
                        for trial_idx in range(self.get_ntrials()):  # try the specified number of times
                            try:
                                driver.get(url)  # visit the killersports website

                                sleep(self.get_query_timeout())  # sleep for the specified number of seconds

                                # build the search query
                                query = self.create_exact_query(current_date, current_spread)

                                self.display(query)

                                # find the query box and type in the query
                                text_field = driver.find_element_by_id('sdql')
                                text_field.send_keys(query)

                                # find the query submit button and click it
                                button = driver.find_element_by_name('submit')
                                button.click()

                                # retrieve the win-loss-tie stats for the given point spread
                                su_element = driver.find_element_by_xpath \
                                    ('/html/body/div[@id="content"]/table/tbody/tr[2]/td/table/tbody/tr[1]/td[1]')

                                su_text = str(su_element.text)  # convert the web element to text
                                # parse the text to extract the win-loss-tie stats
                                wlt = [int(num) for num in su_text.split()[0].split('-')]

                                driver.close()  # close the Chrome webdriver

                                sample_size = wlt[0] + wlt[1]  # compute the sample size

                                # fav_row[spread_index] = fav_row[spread_index] + ';' + str(wlt[0]) + '-' +
                                # str(wlt[1]) + '-' + str(sample_size)

                                # include the win-loss-tie stats for the current spread in the underdog row
                                dog_row[spread_index] = dog_row[spread_index] + ';' + str(wlt[0]) + '-' + str(
                                    wlt[1]) + '-' + str(sample_size)

                                # store the win-loss-tie stats for the current spread for both the favorite
                                # and the underdog teams
                                fav_spreads_map[-current_spread] = tuple((int(wlt[1]), int(wlt[0])))
                                dog_spreads_map[current_spread] = tuple((int(wlt[0]), int(wlt[1])))

                                break  # no more trials are required

                            except Exception as e:  # in the case of an Exception
                                self.display('\n')
                                # self.display(dog_row)
                                self.display(traceback.print_exc())
                                self.display('Exception encountered: No games of desired spread found in sample!')
                                self.display('Setting data to null and exiting...')
                                self.display('\n')

                                # if all trials have been exhausted
                                if trial_idx == self.get_ntrials() - 1:
                                    # fav_row[spread_index] = fav_row[spread_index] + ';' + str('0-0-0')

                                    # store the win-loss-tie stats as 0-0-0
                                    dog_row[spread_index] = dog_row[spread_index] + ';' + str('0-0-0')
                                    fav_spreads_map[-current_spread] = tuple((0, 0))
                                    dog_spreads_map[current_spread] = tuple((0, 0))
                                    driver.close()  # close the Chrome webdriver
                    else:  # if the current spread stats have already been scraped
                        # use the stored win-loss-tie stats for current spread
                        dog_win_count, dog_loss_count = dog_spreads_map[current_spread]
                        sample_size = dog_win_count + dog_loss_count
                        # fav_row[spread_index] = fav_row[spread_index] + ';' + str(fav_win_count) + '-' + \
                        #                         str(fav_loss_count) + '-' + str(sample_size)
                        dog_row[spread_index] = dog_row[spread_index] + ';' + str(dog_win_count) + '-' + \
                                                str(dog_loss_count) + '-' + str(sample_size)

                self.display(fav_row)
                self.display(dog_row)
                self.display(spacer_row)
                self.pdisplay(fav_spreads_map)
                self.pdisplay(dog_spreads_map)
                self.display('\n')

            new_data_matrix.append(fav_row)  # store the modified favorite, underdog and spacer rows
            new_data_matrix.append(dog_row)
            new_data_matrix.append(spacer_row)

            self.set_csv_matrix(new_data_matrix)  # set the new csv matrix as the current csv matrix
            FileIO.write_csv(self.get_csv_matrix(), self.get_target_csv())  # store the current csv matrix

    @staticmethod
    def extract_dates(data_matrix):
        """
        Given a data matrix of games, returns a list of the dates that the games were played on
        """
        dates = list()  # initialize an empty list
        if len(data_matrix) > 2:  # if there are games in the data matrix
            for idx in range(2, len(data_matrix), 3):  # for every game
                dates.append(data_matrix[idx][0])  # add the date to the list
        return dates  # return the list of dates

    @staticmethod
    def create_exact_query(date, spread):
        """
        Given the date of a game and the exact point spread, constructs the query required to obtain
        the win percentage from the killersports.com website
        """
        return 't:line=' + str(spread) + ' and date<' + str(date)  # create and return the query

    @staticmethod
    def create_ranged_query(date, minline, maxline):
        """
        Given the date of a game and the minimum and maximum point spread, constructs the ranged query
        required to obtain the win percentage from the killersports.com website
        """
        return str(minline) + '<=t:line<=' + str(maxline) + ' and date<' + str(date)  # create and return the query

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

    def pdisplay(self, message):
        """
        Given a message string, pretty-prints the message if the verbose option is turned on
        """
        if self.get_verbose():  # if the verbose boolean is set to true
            pprint(str(message))  # pretty-print the input message

    def get_target_csv(self):
        """
        Returns the target csv
        """
        return self.target_csv  # return the target csv

    def get_webdriver_path(self):
        """
        Returns the webdriver path
        """
        return self.webdriver_path  # return the webdriver path

    def get_base_url(self):
        """
        Returns the base url
        """
        return self.base_url  # return the base url

    def get_branch_url(self):
        """
        Returns the branch url
        """
        return self.branch_url  # return the branch url

    def get_read_csv(self):
        """
        Returns the read csv option
        """
        return self.read_csv  # return the read csv option

    def get_csv_matrix(self):
        """
        Returns the csv matrix
        """
        return self.csv_matrix  # return the csv matrix

    def get_query_timeout(self):
        """
        Returns the query timeout
        """
        return self.query_timeout  # return the query timeout

    def get_ntrials(self):
        """
        Returns the number of trials
        """
        return self.ntrials  # return the number of trials

    def get_verbose(self):
        """
        Returns the verbose option
        """
        return self.verbose  # return the verbose option

    def set_target_csv(self, target_csv):
        """
        Given a new target csv, sets the current target csv as the new target csv
        """
        self.target_csv = target_csv  # set the current target csv as the new target csv

    def set_webdriver_path(self, webdriver_path):
        """
        Given a new webdriver path, sets the current webdriver path as the new webdriver path
        """
        self.webdriver_path = webdriver_path  # set the current webdriver path as the new webdriver path

    def set_branch_url(self, branch_url):
        """
        Given a new branch url, sets the current read csv option as the new branch url
        """
        self.branch_url = branch_url  # set the current branch url as the new branch url

    def set_read_csv_file(self, read_csv):
        """
        Given a new read csv option, sets the current read csv option as the new read csv option
        """
        self.read_csv = read_csv  # set the current read csv option as the new read csv option

    def set_csv_matrix(self, csv_matrix):
        """
        Given a new csv matrix, sets the current csv matrix as the new csv matrix
        """
        self.csv_matrix = csv_matrix  # set the current csv matrix as the new csv matrix

    def set_query_timeout(self, query_timeout):
        """
        Given a new query timeout, sets the current query timeout as the new query timeout
        """
        self.query_timeout = query_timeout  # set the current query timeout as the new query timeout

    def set_ntrials(self, ntrials):
        """
        Given a new number of trials, sets the current number of trials as the new number of trials
        """
        self.ntrials = ntrials  # set the current number of trials as the new number of trials

    def set_verbose(self, verbose):
        """
        Given a new verbose option, sets the current verbose option as the new verbose option
        """
        self.verbose = verbose  # set the current verbose option as the new verbose option
