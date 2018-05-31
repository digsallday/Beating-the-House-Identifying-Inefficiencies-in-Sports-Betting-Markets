class VIGlobals:
    """
    Class containing global variables for the VegasInsiderSpider package
    """

    # dictionary mapping months to their respective month numbers
    MONTHS_TO_NUM = \
        {
            "January": 1,
            "February": 2,
            "March": 3,
            "April": 4,
            "May": 5,
            "June": 6,
            "July": 7,
            "August": 8,
            "September": 9,
            "October": 10,
            "November": 11,
            "December": 12
        }

    # dictionary mapping month numbers to their respective months
    NUM_TO_MONTHS = \
        {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December"
        }

    # dictionary mapping months to the number of days in the month
    NUM_DAYS = \
        {
            "January": 31,
            "February": 28,
            "March": 31,
            "April": 30,
            "May": 31,
            "June": 30,
            "July": 31,
            "August": 31,
            "September": 30,
            "October": 31,
            "November": 30,
            "December": 31
        }

    # suffix for overall csv filename
    OVERALL_CSV_SUFFIX = "Vegas Data"

    # header for overall csv
    OVERALL_CSV_HEADER = \
        list([
            'Date',
            'Teams',
            'Favorite/Underdog',
            'Score',
            'Spread Min',
            'Spread Max',
            'Moneyline',
            'Payout'
        ])

    # suffix for moneylines csv filename
    MONEYLINE_CSV_SUFFIX = "Vegas Moneyline"

    # header for moneylines csv
    MONEYLINE_CSV_HEADER = \
        list([
            'Date',
            'Teams',
            'Favorite/Underdog'
        ])

    # suffix for moneyline times csv filename
    MONEYLINE_TIMES_CSV_SUFFIX = "Vegas Moneyline Times"

    # header for moneyline times csv
    MONEYLINE_TIMES_CSV_HEADER = \
        list([
            'Game Time',
            'Money Line Time'
        ])

    # suffix for point spreads csv filename
    SPREADS_CSV_SUFFIX = "Vegas Spreads"

    # header for spreads csv
    SPREADS_CSV_HEADER = \
        list([
            'Date',
            'Teams',
            'Favorite/Underdog'
        ])

    # suffix for point spread times csv filename
    SPREADS_TIMES_CSV_SUFFIX = "Vegas Spreads Times"

    # header for spread times csv
    SPREADS_TIMES_CSV_HEADER = \
        list([
            'Game Time',
            'Point Spread Time'
        ])
