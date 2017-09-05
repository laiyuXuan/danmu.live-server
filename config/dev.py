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
# qq
QQ_SEARCH_URL = "https://v.qq.com/x/search/?q={}&stag=7&smartbox_ab="
QQ_GET_DANMU_ID_URL = "https://bullet.video.qq.com/fcgi-bin/target/regist?otype=json&cid={}&lid=&g_tk=&vid={}"
QQ_GET_DANMU_URL = "https://mfm.video.qq.com/danmu?otype=json&target_id={}&count={}"
#iqiyi
#                      http://cmts.iqiyi.com/bullet/11/00/350341100_300_1.z?rn=0.8241726098805287&business=danmu&is_iqiyi=true&is_video_page=true&tvid=350341100&albumid=350341100&categoryid=1&qypid=01010021010000000000
IQIYI_SEARCH_MOVIE_URL = "http://so.iqiyi.com/so/q_{}_ctg_电影_t_0_page_1_p_1_qc_0_rd__site__m_1_bitrate_?af=true"
IQIYI_SEARCH_EPISODE_URL = "http://so.iqiyi.com/so/q_{}_ctg_电视剧_t_0_page_1_p_1_qc_0_rd__site_iqiyi_m_1_bitrate_?af=true"
IQIYI_GET_DANMU_URL = "http://cmts.iqiyi.com/bullet/{}/{}/{}_300_{}.z?rn={}&business=danmu&is_iqiyi=true&is_video_page=true&tvid={}&albumid={}&categoryid={}&qypid=01010021010000000000"
IQIYI_GET_TV_INFO_URL = ""
# douban
DOUBAN_SEARCH_MOVICE_URL = "https://api.douban.com/v2/movie/search?q={}"

# keys
BILIBILI_APPKEY = "f3bb208b3d081dc8"
BILIBILI_SECRET = "1c15888dc316e05a15fdd0a02ed6584f"