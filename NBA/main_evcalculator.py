from NBA.NBAGlobals import NBAGlobals
from EVCalculator import EVCalculator
from WinPercentageCalculator import WPGlobals


TIME_PERIOD = "Aggregate"  # specify the time period

WEIGHT_FN_SUFFIX = "x"  #

# create the string representation for the weight function
WEIGHT_FN_STR = WPGlobals.WEIGHT_FUNCTION_PREFIX + WEIGHT_FN_SUFFIX

nba_evcalculator = \
    EVCalculator(
        sport_name=NBAGlobals.SPORT_NAME,
        time_period=TIME_PERIOD,
        weight_fn_str=WEIGHT_FN_STR,
        verbose=True
    )  # initialize the nba ev calculator

# compute the expected values of all teams for all games using the nba ev calculator
nba_evcalculator.compute_ev()
