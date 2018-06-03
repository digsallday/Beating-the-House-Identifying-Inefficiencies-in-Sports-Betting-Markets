from FileIO import FileIO
from RepoGlobals import RepoGlobals
from NFL.NFLGlobals import NFLGlobals
from KillerSportsSpider import KSSpider
from KillerSportsSpider import KSGlobals
from VegasInsiderSpider import VIGlobals


START_GAME_INDEX = 0  # specify the starting game index

# read the spreads data matrix
DATA_MATRIX = FileIO.read_csv(" ".join([NFLGlobals.SPORT_NAME, VIGlobals.SPREADS_CSV_SUFFIX, "(Aggregate).csv"]))

# initialize the target csv
TARGET_CSV = " ".join([NFLGlobals.SPORT_NAME, KSGlobals.FINAL_KS_CSV_PREFIX, "(Aggregate).csv"])

nfl_spider = \
    KSSpider(
        target_csv=TARGET_CSV,
        webdriver_path=RepoGlobals.WEBDRIVER_PATH,
        branch_url=NFLGlobals.KS_BRANCH_URL,
        read_csv=False,
        query_timeout=15,
        ntrials=5,
        verbose=True
    )  # initialize the nfl ks spider

nfl_spider.deploy(DATA_MATRIX, START_GAME_INDEX)  # deploy the nfl ks spider
