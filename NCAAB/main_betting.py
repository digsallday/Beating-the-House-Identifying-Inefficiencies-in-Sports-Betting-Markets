from BettingMachine import BettingMachine
from NCAAB.NCAABGlobals import NCAABGlobals
from WinPercentageCalculator import WPGlobals


TIME_PERIOD = "Aggregate"  # specify the time period

WEIGHT_FN_SUFFIX = "x"  # specify the suffix for the weight function string

# create the string representation for the weight function
WEIGHT_FN_STR = WPGlobals.WEIGHT_FUNCTION_PREFIX + WEIGHT_FN_SUFFIX

EPSILON = 50  # specify the epsilon value

EV_THRESHOLD = 0  # specify the EV threshold value

ncaab_betting_machine = \
    BettingMachine(
        sport_name=NCAABGlobals.SPORT_NAME,
        time_period=TIME_PERIOD,
        weight_fn_str=WEIGHT_FN_STR,
        verbose=True
    )  # initialize the ncaab betting machine

# run the betting algorithm
ncaab_betting_machine.run(EPSILON, EV_THRESHOLD)
