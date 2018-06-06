class EVGlobals:
    """
    Class containing global variables for the EVGlobals package
    """

    # header for the ev csv
    EV_CSV_HEADER = \
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
            'EV'
        ])

    # suffix for the ev csv filename
    EV_CSV_SUFFIX = "EV Data"
