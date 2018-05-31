from VegasInsiderSpider import DailyVISpider
from RepoGlobals import RepoGlobals
from VIGlobals import VIGlobals
from WNBA import WNBAGlobals


START_DATE = "05-1-2018"  # specify the start date

END_DATE = "05-28-2018"  # specify the end date

# construct the target csv filename
TARGET_CSV = \
    WNBAGlobals.SPORT_NAME + \
    " " + VIGlobals.OVERALL_CSV_SUFFIX + \
    " (" + str(START_DATE) + ' - ' + str(END_DATE) + ").csv"

# initialize the wnba spider
wnba_spider = \
    DailyVISpider(
        sport_name=WNBAGlobals.SPORT_NAME,
        team_abbr=WNBAGlobals.TEAM_ABBR,
        target_csv=TARGET_CSV,
        webdriver_path=RepoGlobals.WEBDRIVER_PATH,
        branch_url=WNBAGlobals.VI_BRANCH_URL,
        read_csv=False,
        time_threshold=1,
        verbose=True,
        archive_mode=False
    )

wnba_spider.deploy(START_DATE, END_DATE)  # deploy the wnba spider
