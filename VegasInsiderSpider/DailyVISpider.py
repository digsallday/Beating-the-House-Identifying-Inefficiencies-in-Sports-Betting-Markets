import traceback
from FileIO import FileIO
from selenium import webdriver
from VIGlobals import VIGlobals
from BaseVISpider import BaseVISpider


class DailyVISpider(BaseVISpider):
    """
    DailyVISpider class that inherits base attributes and methods from the BaseVISpider class and that scrapes
    the vegasinsider.com website in order to acquire betting data for sports which follow a daily schedule.
    """
    def __init__(self, sport_name, team_abbr, target_csv, webdriver_path, branch_url='', read_csv=False,
                 time_threshold=1, verbose=True, archive_mode=False):
        """
        Constructor for the DailyVISpider class - initializes instances of the class and the attributes
        of the created object
        """
        self.sport_name = sport_name  # initialize the attributes of this object
        self.team_abbr = team_abbr
        self.archive_mode = archive_mode

        # initialize the super class
        super(DailyVISpider, self)\
            .__init__(
                target_csv,
                webdriver_path,
                branch_url,
                read_csv,
                time_threshold,
                verbose
        )

    def deploy(self, start_date, end_date):
        """
        Given the start and end date of the season which requires scraping, deploys a spider that visits the
        vegasinsider.com website to acquire the betting data for the specified sport for the specified dates
        (end date exclusive) and stores all relevant data to memory
        """
        # specify the different csv file names
        moneylines_csv_filename = \
            self.get_sport_name() + \
            " " + VIGlobals.MONEYLINE_CSV_SUFFIX + \
            " (" + str(start_date) + ' - ' + str(end_date) + ").csv"

        moneylines_times_csv_filename = \
            self.get_sport_name() + \
            " " + VIGlobals.MONEYLINE_TIMES_CSV_SUFFIX + \
            " (" + str(start_date) + ' - ' + str(end_date) + ").csv"

        spreads_csv_filename = \
            self.get_sport_name() + \
            " " + VIGlobals.SPREADS_CSV_SUFFIX + \
            " (" + str(start_date) + ' - ' + str(end_date) + ").csv"

        spreads_times_csv_filename = \
            self.get_sport_name() + \
            " " + VIGlobals.SPREADS_TIMES_CSV_SUFFIX + \
            " (" + str(start_date) + ' - ' + str(end_date) + ").csv"

        # initialize all data matrices
        moneylines_matrix = list()
        ml_time_column = list([VIGlobals.MONEYLINE_TIMES_CSV_HEADER])

        spreads_matrix = list()
        ps_time_column = list([VIGlobals.SPREADS_TIMES_CSV_HEADER])

        final_data_matrix = list([VIGlobals.OVERALL_CSV_HEADER, list()])

        casinos = list()  # initialize an empty list to store the casino names as they appear

        url_date = start_date  # initialize the url date

        # while the current date being scraped is not the end date
        while not self.compare_dates2(url_date, end_date):
            # construct the url for the current date
            url = self.get_base_url() + self.get_branch_url() + "/game_date/" + str(url_date)
            print(url)
            driver = webdriver.Chrome(self.get_webdriver_path())
            driver.get(url)  # visit the website

            try:
                # retrieve the list of game tables
                game_tables = driver.find_elements_by_xpath('.//td[@class="sportPicksBorder"]')
                if len(game_tables) == 0:  # if there are no games listed on the current date
                    self.display(" ".join(list(["No Games Scheduled on", url_date])))
                    self.display("\n")
                    url_date = self.advance_date(url_date)  # iterate over to the next date
                    driver.close()  # close the main driver
                    continue  # carry over to the next iteration
                self.display(len(game_tables))
            except Exception as exception:
                self.display(" ".join(list(["No Games Scheduled on", url_date])))
                self.display("\n")
                # traceback.print_exc()
                url_date = self.advance_date(url_date)  # iterate over to the next date
                driver.close()  # close the main driver
                continue  # carry over to the next iteration

            for game_table_index in range(len(game_tables)):  # for every game table
                try:
                    # initialize the moneylines, spreads and final data lists
                    away_moneylines, home_moneylines = list([]), list([])
                    away_spreads, home_spreads = list([]), list([])
                    final_data_upper_row, final_data_lower_row = list([]), list([])

                    # create a new auxiliary Chromedriver
                    game_driver = webdriver.Chrome(self.get_webdriver_path())
                    game_driver.get(url)  # visit the website

                    # retrieve the game tables once more
                    new_game_tables = game_driver.find_elements_by_xpath('.//td[@class="sportPicksBorder"]')
                    game_table = new_game_tables[game_table_index]  # retrieve the current game table

                    # parse through the web elements to retrieve the away team and home team scores
                    away_score_row, home_score_row = game_table.find_elements_by_xpath('.//tr[@class="tanBg"]')
                    away_score = [str(web_element.text) for web_element in away_score_row.
                        find_elements_by_xpath('.//td[@class="sportPicksBorderL2"]')][-1]
                    home_score = [str(web_element.text) for web_element in home_score_row.
                        find_elements_by_xpath('.//td[@class="sportPicksBorderL"]')][-1]

                    # parse through the web elements to find and click the line movement link
                    line_movement_row = game_table.find_elements_by_xpath('.//td[@align="left"]')[-1]
                    line_movement_link = line_movement_row.find_element_by_xpath('.//a[@class="white"]')
                    line_movement_link.click()

                    # if the archive mode is enabled
                    if self.get_archive_mode():
                        # redirect to archive.org
                        game_driver.get('https://web.archive.org/web/' + str(game_driver.current_url))

                    # retrieve the information tables
                    info_tables = game_driver.find_element_by_xpath('.//div[@class="SLTables1"]').\
                        find_elements_by_xpath('.//table[@cellspacing=0]')

                    # retrieve the game title and datetime
                    game_title, game_datetime = info_tables[0], info_tables[1]

                    # retrieve the away team name and the home team name
                    away_team, home_team = [str(team_name) for team_name in
                                            str(game_title.find_element_by_xpath('.//font').text).split(' @ ')]

                    self.display(" ".join(list([away_team, away_score])))  # display the away team name and score
                    self.display(" ".join(list([home_team, home_score])))  # display the home team name and score

                    # parse the game date and time
                    game_date, game_time = \
                        [
                            str(game_info.text)
                            for game_info in game_datetime.find_elements_by_xpath('.//td[@valign="top"]')
                        ]

                    game_date, game_time = " ".join(game_date.split()[2:]), " ".join(game_time.split()[2:])

                    # display the game date and time
                    self.display(" ".join(list([game_date, game_time])))
                    self.display('\n')

                    # initialize empty lists to hold the underdog moneylines and point spreads
                    underdog_mls = list([])
                    underdog_pss = list([])

                    for info_table in info_tables[2:]:  # for every information table
                        # grab the casino name
                        casino_name = info_table.find_element_by_xpath('.//tr[@class="component_head"]').text
                        casino_name = casino_name[:len(casino_name) - 15]
                        self.display(casino_name)  # print the casino name

                        # if it is the first date and the first game table
                        if url_date == start_date and game_table_index == 0:
                            casinos.append(casino_name)  # store the casino name

                        # retrieve a list of the table rows
                        table_rows = \
                            info_table \
                                .find_element_by_xpath('.//table[@class="rt_railbox_border2"]') \
                                .find_elements_by_xpath('.//tr')

                        # initialize the list of desired table rows for both moneylines and point spreads
                        ml_desired_table_rows = list([])
                        ps_desired_table_rows = list([])

                        # for every table row
                        for table_row in table_rows[2:]:
                            # retrieve the table row elements
                            table_row_elements = [str(table_row_element.text) for table_row_element in
                                                  table_row.find_elements_by_css_selector('td.bg2')]

                            # if the betting data was published before the start of the game and has the moneyline
                            if self.is_before_game(table_row_elements, game_date, game_time) and \
                                    self.has_money_line(
                                        table_row_elements,
                                        len(self.get_team_abbr()[away_team]),
                                        len(self.get_team_abbr()[home_team])
                                    ):
                                # add it to the list of desired rows
                                ml_desired_table_rows.append(table_row_elements)
                            # if the betting data was published before the start of game and has the point spread
                            if self.is_before_game(table_row_elements, game_date, game_time) and \
                                    self.has_point_spread(
                                        table_row_elements,
                                        len(self.get_team_abbr()[away_team]),
                                        len(self.get_team_abbr()[home_team])
                                    ):
                                # add it to the list of desired rows
                                ps_desired_table_rows.append(table_row_elements)

                        # if there are no desired rows, set the away and home moneylines to null strings
                        if len(ml_desired_table_rows) == 0:
                            away_moneyline = str('')
                            home_moneyline = str('')
                        else:  # otherwise
                            # select the most recent moneyline row
                            ml_desired_table_row = self.determine_ml_desired_table_row(ml_desired_table_rows)

                            underdog_ml = \
                                self.determine_underdog_ml(
                                    ml_desired_table_row,
                                    away_team,
                                    home_team,
                                    self.get_team_abbr()
                                )
                            underdog_mls.append(underdog_ml)  # check which team is the underdog

                            # display the most recent moneyline row before the game, taking the time
                            # threshold into account
                            self.display(" ".join(list(["Money Line Row:", str(ml_desired_table_row)])))

                            # extract the moneylines from this row
                            first_ml, second_ml = self.extract_moneyline(ml_desired_table_row,
                                                                         len(self.get_team_abbr()[away_team]),
                                                                         len(self.get_team_abbr()[home_team]))

                            # assign the correct moneyline to the correct team
                            if underdog_ml:
                                away_moneyline = self.handle_moneyline_pk(first_ml)
                                home_moneyline = self.handle_moneyline_pk(second_ml)
                            else:
                                away_moneyline = self.handle_moneyline_pk(second_ml)
                                home_moneyline = self.handle_moneyline_pk(first_ml)

                            if not self.is_within_time_period(ml_desired_table_row[0], ml_desired_table_row[1],
                                                              self.rectify_date_format2(game_date),
                                                              self.rectify_time_format(game_time)):
                                away_moneyline = str('')
                                home_moneyline = str('')

                            # store the moneyline times
                            ml_time_column.append(list([str(game_time), str(ml_desired_table_row[1])]))

                        # if there are no desired rows, set the away and home point spreads to null strings
                        if len(ps_desired_table_rows) == 0:
                            away_point_spread = str('')
                            home_point_spread = str('')
                        else:  # otherwise
                            # select the most recent point spread row
                            ps_desired_table_row = self.determine_ps_desired_table_row(ps_desired_table_rows)

                            underdog_ps = \
                                self.determine_underdog_ps(
                                    ps_desired_table_row,
                                    away_team,
                                    home_team,
                                    self.get_team_abbr()
                                )
                            underdog_pss.append(underdog_ps)  # check which team is the underdog

                            # display the most recent point spread row before the game, taking the time
                            # threshold into account
                            self.display(" ".join(list(["Point Spread Row:", str(ps_desired_table_row)])))

                            # extract the point spreads from this row
                            first_ps, second_ps = \
                                self.extract_spreads(
                                    ps_desired_table_row,
                                    len(self.get_team_abbr()[away_team]),
                                    len(self.get_team_abbr()[home_team])
                                )

                            # assign the correct point spread to the correct team
                            if underdog_ps:
                                away_point_spread = self.handle_spread_pk(first_ps)
                                home_point_spread = self.handle_spread_pk(second_ps)
                            else:
                                away_point_spread = self.handle_spread_pk(second_ps)
                                home_point_spread = self.handle_spread_pk(first_ps)

                            if not self.is_within_time_period(
                                    ps_desired_table_row[0],
                                    ps_desired_table_row[1],
                                    self.rectify_date_format2(game_date),
                                    self.rectify_time_format(game_time)
                            ):
                                away_point_spread = str('')
                                home_point_spread = str('')

                            # store the point spread times
                            ps_time_column.append(list([str(game_time), str(ps_desired_table_row[1])]))

                        # display the away and home moneylines and point spreads
                        self.display(" ".join(list(["Away Moneyline:", away_moneyline])))
                        self.display(" ".join(list(["Home Moneyline:", home_moneyline])))
                        self.display(" ".join(list(["Away Point Spread:", away_point_spread])))
                        self.display(" ".join(list(["Home Point Spread:", home_point_spread])))
                        self.display("\n")

                        # store the away and home moneylines and point spreads
                        away_moneylines.append(away_moneyline)
                        home_moneylines.append(home_moneyline)

                        away_spreads.append(away_point_spread)
                        home_spreads.append(home_point_spread)

                    # if this is the first moneyline row
                    if len(moneylines_matrix) == 0:
                        # add the moneyline heading first
                        moneylines_matrix.append(list(VIGlobals.MONEYLINE_CSV_HEADER) + casinos)
                        moneylines_matrix.append(list())

                    # if this is the first point spread row
                    if len(spreads_matrix) == 0:
                        # add the point spread heading first
                        spreads_matrix.append(list(VIGlobals.SPREADS_CSV_HEADER) + casinos)
                        spreads_matrix.append(list())

                    # print the list of away and home moneylines and point spreads
                    self.display("\n")
                    self.display(" ".join(list(["Away Moneylines:", str(away_moneylines)])))
                    self.display(" ".join(list(["Home Moneylines:", str(home_moneylines)])))
                    self.display(" ".join(list(["Away Point Spreads:", str(away_spreads)])))
                    self.display(" ".join(list(["Home Point Spreads:", str(home_spreads)])))
                    self.display("\n")

                    # determine the best moneyline for both teams
                    desired_max_away_moneyline = \
                        max([
                            float(moneyline)
                            for moneyline in away_moneylines
                            if moneyline != ''
                        ])
                    desired_max_home_moneyline = \
                        max([
                            float(moneyline)
                            for moneyline in home_moneylines
                            if moneyline != ''
                        ])

                    # determine the away and home payouts corresponding to the best moneylines
                    desired_away_moneyline_payout = self.compute_payout(desired_max_away_moneyline)
                    desired_home_moneyline_payout = self.compute_payout(desired_max_home_moneyline)

                    # determine the range of point spreads for both teams
                    desired_min_away_point_spread = \
                        min([
                            float(point_spread)
                            for point_spread in away_spreads
                            if point_spread != ''
                        ])
                    desired_max_away_point_spread = \
                        max([
                            float(point_spread)
                            for point_spread in away_spreads
                            if point_spread != ''
                        ])

                    desired_min_home_point_spread = \
                        min([
                            float(point_spread)
                            for point_spread in home_spreads
                            if point_spread != ''
                        ])
                    desired_max_home_point_spread = \
                        max([
                            float(point_spread)
                            for point_spread in home_spreads
                            if point_spread != ''
                        ])

                    # determine the underdog according to both moneylines and point spreads
                    underdog_consensus = self.determine_underdog_consensus(underdog_mls, underdog_pss)

                    # store the data appropriately depending on which team is the underdog
                    if underdog_consensus:
                        payouts_upper_row = \
                            list([self.rectify_date_format(game_date), away_team, '(Favorite)']) + away_moneylines
                        payouts_lower_row = list(['', home_team, '(Underdog)']) + home_moneylines

                        point_spreads_upper_row = \
                            list([self.rectify_date_format(game_date), away_team, '(Favorite)']) + away_spreads
                        point_spreads_lower_row = list(['', home_team, '(Underdog)']) + home_spreads

                        final_data_upper_row += \
                            list([
                                self.rectify_date_format(game_date),
                                away_team,
                                '(Favorite)',
                                away_score,
                                str(desired_min_away_point_spread),
                                str(desired_max_away_point_spread),
                                str(desired_max_away_moneyline),
                                str(desired_away_moneyline_payout)
                            ])
                        final_data_lower_row += \
                            list([
                                '',
                                home_team,
                                '(Underdog)',
                                home_score,
                                str(desired_min_home_point_spread),
                                str(desired_max_home_point_spread),
                                str(desired_max_home_moneyline),
                                str(desired_home_moneyline_payout)
                            ])
                    else:
                        payouts_upper_row = \
                            list([self.rectify_date_format(game_date), home_team, '(Favorite)']) + home_moneylines
                        payouts_lower_row = list(['', away_team, '(Underdog)']) + away_moneylines

                        point_spreads_upper_row = \
                            list([self.rectify_date_format(game_date), home_team, '(Favorite)']) + home_spreads
                        point_spreads_lower_row = list(['', away_team, '(Underdog)']) + away_spreads

                        final_data_upper_row += \
                            list([
                                self.rectify_date_format(game_date),
                                home_team,
                                '(Favorite)',
                                home_score,
                                str(desired_min_home_point_spread),
                                str(desired_max_home_point_spread),
                                str(desired_max_home_moneyline),
                                str(desired_home_moneyline_payout)
                            ])

                        final_data_lower_row += \
                            list([
                                '',
                                away_team,
                                '(Underdog)',
                                away_score,
                                str(desired_min_away_point_spread),
                                str(desired_max_away_point_spread),
                                str(desired_max_away_moneyline),
                                str(desired_away_moneyline_payout)
                            ])

                    # store the moneylines row for this game
                    moneylines_matrix.append(payouts_upper_row)
                    moneylines_matrix.append(payouts_lower_row)
                    moneylines_matrix.append(list())

                    # store the point spreads row for this game
                    spreads_matrix.append(point_spreads_upper_row)
                    spreads_matrix.append(point_spreads_lower_row)
                    spreads_matrix.append(list())

                    # store the overall data row for this game
                    final_data_matrix.append(final_data_upper_row)
                    final_data_matrix.append(final_data_lower_row)
                    final_data_matrix.append(list())

                    # close the auxiliary driver
                    game_driver.close()

                except Exception as e:  # if an exception occurs
                    self.display("Something bad has happened!\n")  # print an error message
                    traceback.print_exc()  # print traceback
                    game_driver.close()  # close the auxiliary driver and retry

            driver.close()  # close the main Chromedriver

            url_date = self.advance_date(url_date)  # carry on to the next date

        self.append_to_csv_matrix(final_data_matrix)  # add the scraped data to the stored csv matrix attribute

        # write all relevant data to memory as csv files
        FileIO.write_csv(moneylines_csv_filename, moneylines_matrix)
        FileIO.write_csv(moneylines_times_csv_filename, ml_time_column)

        FileIO.write_csv(spreads_csv_filename, spreads_matrix)
        FileIO.write_csv(spreads_times_csv_filename, ps_time_column)

        FileIO.write_csv(self.get_target_csv(), self.get_csv_matrix())

    @staticmethod
    def advance_date(current_date):
        """
        Given the current date, advances and returns the next date
        """
        # extract the month, day and year strings
        month, day, year = [int(num) for num in current_date.split('-')]
        months = list(VIGlobals.MONTHS_TO_NUM.keys())  # get a list of the months
        month_ids = list(VIGlobals.MONTHS_TO_NUM.values())  # get a list of month numbers

        # if it is the last day of the month
        if day == VIGlobals.NUM_DAYS[months[month_ids.index(month)]]:
            next_day = str('01')  # the next day is 01
            if month == 12:  # if it is the last month of the year
                next_month = str('01')  # the next month is 01
                next_year = str(year + 1)  # and the next year is the current year plus 1
            else:  # otherwise
                next_month = str(month + 1)  # the next month is the current month plus 1
                next_year = str(year)  # the year stays the same
        else:  # otherwise
            next_day = str(day + 1)  # advance to the next day
            next_month = str(month)  # month and year stays constant
            next_year = str(year)

        # construct the next date
        next_date = next_month + '-' + next_day + '-' + next_year

        return next_date  # return the next date

    @staticmethod
    def compare_dates2(date1, date2):
        """
        Given two dates, returns True if the two dates are equal and False otherwise
        """
        # parse the two date strings to retrieve the day, month and year
        day1, month1, year1 = [int(element) for element in date1.split('-')]
        day2, month2, year2 = [int(element) for element in date2.split('-')]

        if year1 == year2:  # if the two years are equal
            if month1 == month2:  # if the two months are equal
                if day1 == day2:  # if the two days are equal
                    return True  # the two dates are equal and so return True

        return False  # otherwise, return False

    def get_sport_name(self):
        """
        Returns the current sport name
        """
        return self.sport_name  # return the sport name

    def get_team_abbr(self):
        """
        Returns the current team abbreviation dictionary
        """
        return self.team_abbr  # return the team abbreviation dictionary

    def get_archive_mode(self):
        """
        Returns the current archive mode option
        """
        return self.archive_mode  # return the archive mode option

    def set_sport_name(self, sport_name):
        """
        Given a new sport name, sets the current sport name as the new sport name
        """
        self.sport_name = sport_name  # set the current sport name as the new sport name

    def set_team_abbr(self, team_abbr):
        """
        Given a new team abbreviation dictionary, sets the current team abbreviation dictionary as the new
        team abbreviation dictionary
        """
        self.team_abbr = team_abbr  # set the current team abbreviation dictionary as the new one

    def set_archive_mode(self, archive_mode):
        """
        Given a new archive mode option, sets the current archive mode option as the new archive mode option
        """
        self.archive_mode = archive_mode  # set the  current archive mode option as the new one
