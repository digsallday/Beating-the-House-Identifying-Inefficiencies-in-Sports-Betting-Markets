class WPGlobals:
    """
    Class containing global variables for the WPGlobals package
    """

    # prefix for the weight function strings
    WEIGHT_FUNCTION_PREFIX = "f(x) = "

    # header for the final killersports csv
    FINAL_KS_CSV_HEADER = \
        list([
            'Date',
            'Teams',
            'Favorite/Underdog',
            'Score',
            'Spread Min',
            'Spread Max',
            'Moneyline',
            'Payout',
            'Win Percentage'
        ])

    # suffix for the final killersports csv filename
    FINAL_KS_CSV_SUFFIX = "Final KS Data"
