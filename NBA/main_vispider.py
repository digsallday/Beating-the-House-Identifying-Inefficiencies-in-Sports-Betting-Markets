from VegasInsiderSpider import DailyVISpider
from RepoGlobals import RepoGlobals
from VIGlobals import VIGlobals
from NBA import NBAGlobals


START_DATE = "05-1-2018"  # specify the start date

END_DATE = "05-28-2018"  # specify the end date

# construct the target csv filename
TARGET_CSV = \
    NBAGlobals.SPORT_NAME + \
    " " + VIGlobals.OVERALL_CSV_SUFFIX + \
    " (" + str(START_DATE) + ' - ' + str(END_DATE) + ").csv"

# initialize the nba spider
nba_spider = \
    DailyVISpider(
        sport_name=NBAGlobals.SPORT_NAME,
        team_abbr=NBAGlobals.TEAM_ABBR,
        target_csv=TARGET_CSV,
        webdriver_path=RepoGlobals.WEBDRIVER_PATH,
        branch_url=NBAGlobals.VI_BRANCH_URL,
        read_csv=False,
        time_threshold=1,
        verbose=True,
        archive_mode=False
    )

nba_spider.deploy(START_DATE, END_DATE)  # deploy the nba spider
