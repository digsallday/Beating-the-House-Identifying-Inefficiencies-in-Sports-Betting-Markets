from FileIO import FileIO
from RepoGlobals import RepoGlobals
from KillerSportsSpider import KSSpider
from KillerSportsSpider import KSGlobals
from VegasInsiderSpider import VIGlobals
from NCAAB.NCAABGlobals import NCAABGlobals


START_GAME_INDEX = 0  # specify the starting game index

# read the spreads data matrix
DATA_MATRIX = FileIO.read_csv(" ".join([NCAABGlobals.SPORT_NAME, VIGlobals.SPREADS_CSV_SUFFIX, "(Aggregate).csv"]))

# initialize the target csv
TARGET_CSV = " ".join([NCAABGlobals.SPORT_NAME, KSGlobals.KS_CSV_SUFFIX, "(Aggregate).csv"])

ncaab_spider = \
    KSSpider(
        target_csv=TARGET_CSV,
        webdriver_path=RepoGlobals.WEBDRIVER_PATH,
        branch_url=NCAABGlobals.KS_BRANCH_URL,
        read_csv=False,
        query_timeout=15,
        ntrials=5,
        verbose=True
    )  # initialize the nba ks spider

ncaab_spider.deploy(DATA_MATRIX, START_GAME_INDEX)  # deploy the ncaab ks spider
