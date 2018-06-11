from EVCalculator import EVCalculator
from NCAAF.NCAAFGlobals import NCAAFGlobals
from WinPercentageCalculator import WPGlobals


TIME_PERIOD = "Aggregate"  # specify the time period

WEIGHT_FN_SUFFIX = "x"  # specify the suffix for the weight function string

# create the string representation for the weight function
WEIGHT_FN_STR = WPGlobals.WEIGHT_FUNCTION_PREFIX + WEIGHT_FN_SUFFIX

ncaaf_evcalculator = \
    EVCalculator(
        sport_name=NCAAFGlobals.SPORT_NAME,
        time_period=TIME_PERIOD,
        weight_fn_str=WEIGHT_FN_STR,
        verbose=True
    )  # initialize the ncaaf ev calculator

# compute the expected values of all teams for all games using the ncaaf ev calculator
ncaaf_evcalculator.compute_ev()
