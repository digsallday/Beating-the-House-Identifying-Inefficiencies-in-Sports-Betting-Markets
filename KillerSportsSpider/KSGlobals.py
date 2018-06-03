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

    # prefix for final ks csv filename
    FINAL_KS_CSV_PREFIX = "KS Data"

    # header for final killersports csv
    FINAL_KS_CSV_HEADER = \
        list([
            'Date',
            'Teams',
            'Favorite/Underdog'
        ]) + CASINOS
