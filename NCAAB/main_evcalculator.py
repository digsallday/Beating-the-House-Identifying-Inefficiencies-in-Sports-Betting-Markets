from EVCalculator import EVCalculator
from NCAAB.NCAABGlobals import NCAABGlobals
from WinPercentageCalculator import WPGlobals


TIME_PERIOD = "Aggregate"  # specify the time period

WEIGHT_FN_SUFFIX = "x"  #

# create the string representation for the weight function
WEIGHT_FN_STR = WPGlobals.WEIGHT_FUNCTION_PREFIX + WEIGHT_FN_SUFFIX

ncaab_evcalculator = \
    EVCalculator(
        sport_name=NCAABGlobals.SPORT_NAME,
        time_period=TIME_PERIOD,
        weight_fn_str=WEIGHT_FN_STR,
        verbose=True
    )  # initialize the ncaab ev calculator

# compute the expected values of all teams for all games using the ncaab ev calculator
ncaab_evcalculator.compute_ev()
