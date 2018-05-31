from VegasInsiderSpider import WeeklyVISpider
from RepoGlobals import RepoGlobals
from VIGlobals import VIGlobals
from NFL import NFLGlobals


YEAR = 2017  # specify the year

DISALLOWED_WEEK_INDICES = list(range(1, NFLGlobals.WEEKS_COUNT + 1))  # specify the forbidden week indices

# construct the target csv filename
TARGET_CSV = NFLGlobals.SPORT_NAME + " " + VIGlobals.OVERALL_CSV_SUFFIX + " (" + str(YEAR) + ").csv"

# initialize the nfl spider
nfl_spider = \
    WeeklyVISpider(
        sport_name=NFLGlobals.SPORT_NAME,
        weeks_count=NFLGlobals.WEEKS_COUNT,
        team_abbr=NFLGlobals.TEAM_ABBR,
        target_csv=TARGET_CSV,
        webdriver_path=RepoGlobals.WEBDRIVER_PATH,
        branch_url=NFLGlobals.VI_BRANCH_URL,
        read_csv=False,
        time_threshold=1,
        verbose=True,
        archive_mode=False
    )

nfl_spider.deploy(YEAR, DISALLOWED_WEEK_INDICES)  # deploy the nfl spider
