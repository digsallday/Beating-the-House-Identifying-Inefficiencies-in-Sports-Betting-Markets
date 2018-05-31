from VegasInsiderSpider import WeeklyVISpider
from RepoGlobals import RepoGlobals
from VIGlobals import VIGlobals
from NCAAF import NCAAFGlobals


YEAR = 2017  # specify the year

DISALLOWED_WEEK_INDICES = list()  # specify the forbidden week indices

# construct the target csv filename
TARGET_CSV = NCAAFGlobals.SPORT_NAME + " " + VIGlobals.OVERALL_CSV_SUFFIX + " (" + str(YEAR) + ").csv"

# initialize the ncaaf spider
ncaaf_spider = \
    WeeklyVISpider(
        sport_name=NCAAFGlobals.SPORT_NAME,
        weeks_count=NCAAFGlobals.WEEKS_COUNT,
        team_abbr=NCAAFGlobals.TEAM_ABBR,
        target_csv=TARGET_CSV,
        webdriver_path=RepoGlobals.WEBDRIVER_PATH,
        branch_url=NCAAFGlobals.VI_BRANCH_URL,
        read_csv=False,
        time_threshold=1,
        verbose=True,
        archive_mode=False
    )

ncaaf_spider.deploy(YEAR, DISALLOWED_WEEK_INDICES)  # deploy the ncaaf spider
