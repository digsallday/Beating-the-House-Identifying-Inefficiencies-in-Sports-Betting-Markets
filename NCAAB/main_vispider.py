from VegasInsiderSpider import DailyVISpider
from RepoGlobals import RepoGlobals
from VIGlobals import VIGlobals
from NCAAB import NCAABGlobals


START_DATE = "05-1-2018"  # specify the start date

END_DATE = "05-28-2018"  # specify the end date

# construct the target csv filename
TARGET_CSV = \
    NCAABGlobals.SPORT_NAME + \
    " " + VIGlobals.OVERALL_CSV_SUFFIX + \
    " (" + str(START_DATE) + ' - ' + str(END_DATE) + ").csv"

# initialize the ncaab spider
ncaab_spider = \
    DailyVISpider(
        sport_name=NCAABGlobals.SPORT_NAME,
        team_abbr=NCAABGlobals.TEAM_ABBR,
        target_csv=TARGET_CSV,
        webdriver_path=RepoGlobals.WEBDRIVER_PATH,
        branch_url=NCAABGlobals.VI_BRANCH_URL,
        read_csv=False,
        time_threshold=1,
        verbose=True,
        archive_mode=False
    )

ncaab_spider.deploy(START_DATE, END_DATE)  # deploy the ncaab spider
