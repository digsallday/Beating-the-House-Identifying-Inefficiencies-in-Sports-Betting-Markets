class WNBAGlobals:
    """
    Class containing global variables for the WNBA package
    """

    SPORT_NAME = "WNBA"  # sport name

    VI_BRANCH_URL = "wnba/scoreboard/scores.cfm"  # branch url for wnba

    KS_BRANCH_URL = "wnba/query"  # killersports.com branch url for wnba

    # dictionary mapping wnba team names to their respective abbreviations
    TEAM_ABBR = \
        {
            "Atlanta Dream": "ATL",
            "Chicago Sky": "CHI",
            "Connecticut Sun": "CONN",
            "Indiana Fever": "IND",
            "New York Liberty": "NEW",
            "Washington Mystics": "WAS",
            "Dallas Wings": "DAL",
            "Los Angeles Sparks": "LOS",
            "Minnesota Lynx": "MIN",
            "Phoenix Mercury": "PHO",
            "San Antonio Stars": "SA",
            "Seattle Storm": "SEA",
            "Tulsa Shock": "TUL"
        }
