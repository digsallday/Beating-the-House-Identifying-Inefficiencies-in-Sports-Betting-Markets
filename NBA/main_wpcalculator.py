from NBA.NBAGlobals import NBAGlobals
from WinPercentageCalculator import WPGlobals, WeightFunctions, WinPercentageCalculator


TIME_PERIOD = "Aggregate"  # specify the time period

COEFFICIENTS = list([0, 1])  # specify the coefficients for the weight function

WEIGHT_FUNCTION = WeightFunctions.polynomial  # specify the type of weight function

WEIGHT_FN_STR = WPGlobals.WEIGHT_FUNCTION_PREFIX + "x"  # create the string representation for the weight function

nba_wpcalculator = \
    WinPercentageCalculator(
        sport_name=NBAGlobals.SPORT_NAME,
        time_period=TIME_PERIOD,
        verbose=True
    )  # initialize the nba win percentage calculator

# compute the win percentages for all games using the nba win percentage calculator
nba_wpcalculator.compute_win_percentages(WEIGHT_FUNCTION, COEFFICIENTS, WEIGHT_FN_STR)
