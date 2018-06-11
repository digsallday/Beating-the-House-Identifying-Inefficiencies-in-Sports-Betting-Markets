class BMGlobals:
    """
    Class containing global variables for the BettingMachine package
    """

    # header for the results csv
    RESULTS_CSV_HEADER = \
        list([
            'Date',
            'Teams',
            'Favorite/Underdog',
            'Score',
            'Spread Min',
            'Spread Max',
            'Moneyline',
            'Payout',
            'Win Percentage',
            'EV',
            'Win/Loss',
            'Current Game Returns',
            'Cumulative Returns'
        ])

    # suffix for the results csv filename
    RESULTS_CSV_SUFFIX = "Results"
