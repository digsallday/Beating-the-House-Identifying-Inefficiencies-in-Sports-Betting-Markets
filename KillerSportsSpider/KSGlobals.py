class KSGlobals:
    """
    Class containing global variables for the KSGlobals package
    """

    # global list of casino names
    CASINOS = \
        list([
            'ATLANTIS',
            'CAESARS',
            'CAL NEVA',
            'GOLDEN NUGGET',
            'HILTON',
            'IMPERIAL',
            'LEROYS',
            'LVSC',
            'M RESORT',
            'MIRAGE',
            'PALMS',
            'PEPPERMILL',
            'STATIONS',
            'STRATOSPHERE',
            'VENETIAN'
        ])

    # suffix for the killersports csv filename
    KS_CSV_SUFFIX = "KS Data"

    # header for the killersports csv
    KS_CSV_HEADER = \
        list([
            'Date',
            'Teams',
            'Favorite/Underdog'
        ]) + CASINOS
