from WNBA.WNBAGlobals import WNBAGlobals
from WinPercentageCalculator import WPGlobals, WeightFunctions, WinPercentageCalculator


TIME_PERIOD = "Aggregate"  # specify the time period

COEFFICIENTS = list([0, 1])  # specify the coefficients for the weight function

WEIGHT_FUNCTION = WeightFunctions.polynomial  # specify the type of weight function

WEIGHT_FN_STR = WPGlobals.WEIGHT_FUNCTION_PREFIX + "x"  # create the string representation for the weight function

wnba_wpcalculator = \
    WinPercentageCalculator(
        sport_name=WNBAGlobals.SPORT_NAME,
        time_period=TIME_PERIOD,
        verbose=True
    )  # initialize the wnba win percentage calculator

# compute the win percentages for all games using the wnba win percentage calculator
wnba_wpcalculator.compute_win_percentages(WEIGHT_FUNCTION, COEFFICIENTS, WEIGHT_FN_STR)
