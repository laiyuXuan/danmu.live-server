DEBUG = True

REDIS_URL = 'redis://:@localhost:6379/0'

ORIGIN = 'http://127.0.0.1:8887'

DANMU_FILE_PATH = 'static/danmu/'

# urls
# acplay
ACPLAY_API_URL = "http://acplay.net/api/v1/match?hash=0&length=5&duration=0&fileName="
# bilibili
BILIBILI_DANMU_URL = "http://comment.bilibili.com/{0}.xml"
BILIBILI_SEARCH_URL_PGC = "https://search.bilibili.com/pgc?keyword="
BILIBILI_SEARCH_URL_MOVIE = "https://search.bilibili.com/all?page=1&order=totalrank&duration=4&tids_1=23&keyword="
BILIBILI_SEARCH_URL_EPISODE_ENDED = "https://search.bilibili.com/all?keyword={0}&page=1&order=totalrank&tids_1=11&tids_2=34"
BILIBILI_SEARCH_URL_EPISODE_SHOWING = "https://search.bilibili.com/all?keyword={0}&page=1&order=totalrank&tids_1=11&tids_2=15"
BILIBILI_VIDEO_INFO_URL = "https://interface.bilibili.com/playurl?cid={}&from=miniplay&player=1&quality=2&type=mp4"

# douban
DOUBAN_SEARCH_MOVICE_URL = "https://api.douban.com/v2/movie/search?q={}"

# keys
BILIBILI_APPKEY = "f3bb208b3d081dc8"
BILIBILI_SECRET = "1c15888dc316e05a15fdd0a02ed6584f"