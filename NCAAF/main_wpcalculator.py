from NCAAF.NCAAFGlobals import NCAAFGlobals
from WinPercentageCalculator import WPGlobals, WeightFunctions, WinPercentageCalculator


TIME_PERIOD = "Aggregate"  # specify the time period

COEFFICIENTS = list([0, 1])  # specify the coefficients for the weight function

WEIGHT_FUNCTION = WeightFunctions.polynomial  # specify the type of weight function

WEIGHT_FN_STR = WPGlobals.WEIGHT_FUNCTION_PREFIX + "x"  # create the string representation for the weight function

ncaaf_wpcalculator = \
    WinPercentageCalculator(
        sport_name=NCAAFGlobals.SPORT_NAME,
        time_period=TIME_PERIOD,
        verbose=True
    )  # initialize the ncaaf win percentage calculator

# compute the win percentages for all games using the ncaaf win percentage calculator
ncaaf_wpcalculator.compute_win_percentages(WEIGHT_FUNCTION, COEFFICIENTS, WEIGHT_FN_STR)
