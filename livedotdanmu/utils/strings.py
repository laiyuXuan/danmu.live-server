import re

def extract_zh(text):
    result = re.compile('[\u4e00-\u9fff]+', re.UNICODE).findall(text)
    return str.join('', result) if not result is None and result.__len__() > 0 else None