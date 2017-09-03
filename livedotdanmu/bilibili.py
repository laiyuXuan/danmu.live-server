import hashlib
import json
import re

import requests
from bs4 import BeautifulSoup, Tag

from livedotdanmu import const, app
from livedotdanmu.model.play import Play
from livedotdanmu.utils import strings, https

PREFIX_PARTITION = 'part-'

VIDEO_LINK_PREFIX = "https://www.bilibili.com"


def match(play: Play):
    if play.type == const.MOVIE:
        cid = search_movie(play.name)
    elif play.type == const.EPISODE:
        cid = search_episode(play)
    else:
        print('reach a todo block')
        cid = None
    if cid is None:
        return None
    if cid.startswith(PREFIX_PARTITION):
        return get_danmu_for_partitions(cid)
    print('danmu url :{}'.format(app.config['BILIBILI_DANMU_URL'].format(cid)))
    r = requests.get(app.config['BILIBILI_DANMU_URL'].format(cid))
    return format_danmu(r.text)


def get_danmu_for_partitions(htmlText):
    htmlText.replace(PREFIX_PARTITION)

    soup = BeautifulSoup(htmlText, 'lxml')
    options = soup.select('div.player-wrapper')[0].find_all('option')
    # 国粤 or 粤国
    if options.__len__() == 2 and (
                (options[0].contents.__contains__('国') and options.contents.__contains__('粤'))
            or (options[0].contents.__contains__('粤') and options.contents.__contains__('国'))
    ):
        # TODO: only one of the two danmu is returned, should be fixed later
        return format_danmu(requests.get(str.format(app.config['BILIBILI_DANMU_URL'], options[0]['cid'])).text)
    else:
        allContents = ''.join(map(lambda o: o.contents, options))
        if allContents.__contains__('粤') and allContents.__contains__('国'):
            # have 2 different sound track
            return get_danmu_for_diff_sound_track_and_parted(soup)
        else:
            # have been parted
            return get_danmu_for_parted(soup)


def get_danmu_for_parted(soup: BeautifulSoup):
    options = soup.select('div.player-wrapper')[0].find_all('option')
    cids = list(map(lambda o: o['cid'], options))
    return combine_danmu(cids)


def combine_danmu(cids):
    allDanmu = get_danmu_by_cid(cids[0])
    for idx, cid in enumerate(cids):
        if idx == 0:
            continue
        vinfo: BeautifulSoup = get_video_info_by_api(cid)
        if vinfo is None:
            continue
        partLength = float(vinfo.find_all('timelength')[0].text) / 1000
        danmu = get_danmu_by_cid(cid)
        if danmu is None:
            continue
        danmakus = danmu['danmaku']
        for danmaku in danmakus:
            danmaku['time'] = float(danmaku['time']) + partLength
        allDanmu['danmaku'].extend(danmakus)
    return allDanmu


def get_danmu_for_diff_sound_track_and_parted(soup: BeautifulSoup):
    # 1.there could be 2 scenario: ABABAB and AAABBB, so im gonna deal with these separately
    # 2.only half of the danmaku would be returned TODO: need to improve this later
    options = soup.select('div.player-wrapper')[0].find_all('option')
    # case ABABAB
    if is_ABABAB(options):
        cids = list(map(lambda o: o['cid'], options[::2]))
        return combine_danmu(cids)
    # case AAABBB
    elif is_AAABBB(options):
        cids = list(map(lambda o: o['cid'], options[:int(options.__len__() / 2)]))
        return combine_danmu(cids)
    else:
        print('unexpected scenario for get_danmu_for_diff_sound_track_and_parted, returning none...')
        return None


def search_movie(keyword):
    link = try_pgc_search(keyword)
    if not link is None:
        print('found a url for movie %s : %s' % (keyword, link))
        return get_cid(link)
    link = try_movie_search(keyword)
    if not link is None:
        print('found a url for movie %s : %s' % (keyword, link))
        return get_cid(link)
    return None


def search_episode(play: Play):
    result = get_episode_link(play, app.config['BILIBILI_SEARCH_URL_EPISODE_ENDED'])
    if not result is None:
        return get_episode_cid(result, play)
    result = get_episode_link(play, app.config['BILIBILI_SEARCH_URL_EPISODE_SHOWING'])
    if not result is None:
        return get_episode_cid(result, play)
    return None


def get_episode_link(play: Play, searchUrl):
    seasonZH = strings.build_season_zh(play)
    r = requests.get(str.format(searchUrl, play.name + seasonZH))
    if r.status_code != 200:
        print('bad request when searching episode on bilibili :%s' % (r.text))
        return None
    soup = BeautifulSoup(r.text, 'lxml')
    video_matrix = soup.select(".video.matrix")
    if video_matrix is None or video_matrix.__len__() == 0:
        print('no matched when searching episode on bilibili for play %s' % (play.name + seasonZH))
        return None
    for video in video_matrix:
        title: str = video.find_all('a')[0]['title']
        if title.__contains__(play.name) and title.__contains__(seasonZH):
            return 'http:' + video.find_all('a')[0]['href']
    print('no matched when searching episode on bilibili for play %s' % (play.name + seasonZH))
    return None


def get_episode_cid(url, play: Play):
    r = requests.get(url)
    if r.status_code != 200:
        print('bad request when getting episode cid on bilibili %s' % (url))
        return None
    soup = BeautifulSoup(r.text, 'lxml')
    options = soup.select('div.player-wrapper')[0].find_all('option')
    # TODO: save other episodes' danmu to db
    print('found a cid on bilibili for {} {} {}'.format(play.name, play.season, play.episode))
    return options[play.episode - 1]['cid']


def try_pgc_search(keyword):
    r = requests.get(app.config['BILIBILI_SEARCH_URL_PGC'] + keyword)
    if r.status_code != 200:
        return
    soup = BeautifulSoup(r.text, "lxml")
    movie_item = soup.select(".movie-item")
    if movie_item.__len__() == 0:
        return
    return soup.select(".movie-item .left-img")[0]["href"]


def get_cid(link):
    try:
        url = "https:" + link
        print(url)
        r = requests.get(
            url,
            headers=https.fake_headers('www.bilibili.com'))
        if r.status_code != 200:
            return
        pattern = "cid\=\"(.+?)\""
        cid = re.findall(pattern, r.text, False)
        if cid.__len__() != 0:
            return cid[0]
        soup = BeautifulSoup(r.text, 'lxml')
        options = soup.select('div.player-wrapper')[0].find_all('option')
        if options.__len__() == 1:
            return options[0]['cid']
        return PREFIX_PARTITION + r.text
    except requests.exceptions.ConnectionError:
        print("something went wrong...")
        return None


def try_movie_search(keyword, year):
    r = requests.get(app.config['BILIBILI_SEARCH_URL_MOVIE'] + keyword)
    if r.status_code != 200:
        return None
    soup = BeautifulSoup(r.text, "lxml")
    video_matrix = soup.select(".video.matrix")
    if video_matrix.__len__() == 0:
        return None
    videoDiv = video_matrix[0].select(".title")[0]
    if not videoDiv['title'].__contains__(keyword):
        return None
    foundYear = strings.extract_year(videoDiv['title'])
    if not year is None and not foundYear is None and year != foundYear:
        return None
    return video_matrix[0].select(".title")[0]["href"]


def format_danmu(response):
    danmus = []
    soup = BeautifulSoup(response, 'lxml')
    danmuTags = soup.findAll('d')
    if danmuTags.__len__() == 0:
        return
    for tag in danmuTags:
        text = tag.contents[0] if tag.contents.__len__() > 0 else ''
        infos = str.split(tag['p'], ',')
        if infos[1] == '4':
            type = 'bottom'
        elif infos[1] == '5':
            type = 'top'
        else:
            type = 'right'
        one_danmu = {
            'author': 'beta',
            'time': infos[0],
            'text': text,
            'color': '#' + hex(int(infos[3])).replace('0x', ''),
            'type': type
        }
        danmus.append(one_danmu)

    result = {
        'code': 1,
        'danmaku': danmus
    }
    return result


def get_danmu_by_cid(id):
    r = requests.get(str.format(app.config['BILIBILI_DANMU_URL'], id))
    return format_danmu(r.text)


def get_video_info_by_api(cid):
    url: str = app.config['BILIBILI_VIDEO_INFO_URL'].format(cid)
    params = url.split('?')[1]
    sign = hashlib.md5((params + app.config['BILIBILI_SECRET']).encode('utf-8')).hexdigest()
    r = requests.get(url + '&sign=' + sign)
    if r.status_code != 200:
        return None
    return BeautifulSoup(r.text, 'lxml')


def is_AAABBB(options:list):
    firstHalf = ''.join(map(lambda o : o.text, options[:int(options.__len__() / 2)]))
    if ((firstHalf.__contains__('粤') and not firstHalf.__contains__('国')) or ( firstHalf.__contains__('国') and not firstHalf.__contains__('粤'))):
        return True
    return False


def is_ABABAB(options:list):
    evenHalf = ''.join(map(lambda o: o.text, options[::2]))
    if evenHalf.__contains__('国') and not evenHalf.__contains__('粤') or (
        evenHalf.__contains__('粤') and not evenHalf.__contains__('国')
    ):
        return True
    return False

