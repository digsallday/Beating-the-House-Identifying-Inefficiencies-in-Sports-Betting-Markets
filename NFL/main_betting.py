from NFL.NFLGlobals import NFLGlobals
from BettingMachine import BettingMachine
from WinPercentageCalculator import WPGlobals


TIME_PERIOD = "Aggregate"  # specify the time period

WEIGHT_FN_SUFFIX = "x"  # specify the suffix for the weight function string

# create the string representation for the weight function
WEIGHT_FN_STR = WPGlobals.WEIGHT_FUNCTION_PREFIX + WEIGHT_FN_SUFFIX

EPSILON = 50  # specify the epsilon value

EV_THRESHOLD = 0  # specify the EV threshold value

nfl_betting_machine = \
    BettingMachine(
        sport_name=NFLGlobals.SPORT_NAME,
        time_period=TIME_PERIOD,
        weight_fn_str=WEIGHT_FN_STR,
        verbose=True
    )  # initialize the nfl betting machine

num_arbitrage = nfl_betting_machine.compute_arbitrage()  # compute number of games with arbitrage
num_games = BettingMachine.compute_num_games(nfl_betting_machine.get_ev_csv())  # compute total number of games

# run the betting algorithm
nfl_betting_machine.run(EPSILON, EV_THRESHOLD)

print("Number of Arbitrage Games: " + str(num_arbitrage) + "\n")  # display the arbitrage stats
print("Number of Total Games: " + str(num_games) + "\n")
print("Percentage of Arbitrage Games (%): " + str(num_arbitrage / float(num_games) * 100) + "\n")
