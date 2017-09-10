MOVIE = 0
EPISODE = 1
ANIMATED_EPISODE = 2

# redis keys
PREFIX_MOVIVE_NAME_2_DANMU = "movie:name:{}"
PREFIX_MOVIVE_NAME_YEAR_2_DANMU = "movie:name:year:{}:{}"
PREFIX_MOVIVE_NAME_YEAR_2_RAW_DANMU = "movie:name:year:{}:{}:raw"
PREFIX_NOT_FOUND_DANMU_LIST = "danmu:notfound:list"
PREFIX_FILE_HASH_HEADTAIL = "file:hash:headtail:{}"
PREFIX_FILE_HASH_BODY = "file:hash:body:{}"
