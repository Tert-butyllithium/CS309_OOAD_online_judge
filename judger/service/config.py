import os
import logzero
from logzero import logger
import logging
import datetime
import hashlib
import socket

# restful api使用的时候需要带上的东西
# original_token = 'TESTING_TOKEN'

OJ_JAVA_TIME_BONUS = 2
OJ_JAVA_MEMORY_BONUS = 512


# 当前用户组的UID，使用这个是为了避免用root启动
SYSTEM_UID = 1000

# 修改数据库的配置 不需要多说
DATABASES_HOST = 'localhost'
DATABASES_USER = 'lanran'
DATABASES_PWD = 'lanran'
DATABASES_DB = 'jol'

# 把这行改成这个repos的路径
Project_PATH = '/home/lumia/CS309_OOAD_online_judge/'

# Project_PATH = '/home/isc-/Desktop/CS309_OOAD_online_judge/'


FILE_TYPE = ['.c', '.cpp', '.PAS', '.java', '.py', '.py', '.kt']
SERVICE_PATH = Project_PATH + 'judger/'
USER_CODES_FOLDER = SERVICE_PATH + 'userCodes/'
RUN_CODE_PY = SERVICE_PATH + 'service/Runner.py'

# 封装logger，这里不需要修改
LOG_FILE = SERVICE_PATH + 'Log/' + str(datetime.date.today()) + '.log'
if not os.path.exists(LOG_FILE):
    log_file = open(LOG_FILE, 'w')
    log_file.close()
logzero.logfile(LOG_FILE, loglevel=logging.DEBUG)

OJ_WT0 = 0
OJ_WT1 = 1
OJ_CI = 2
OJ_RI = 3
OJ_AC = 4
OJ_PE = 5
OJ_WA = 6
OJ_TL = 7
OJ_ML = 8
OJ_OL = 9
OJ_RE = 10
OJ_CE = 11
OJ_CO = 12


# sha256 = hashlib.sha256()
# sha256.update(original_token.encode('utf-8'))
# token = sha256.hexdigest()


def get_host_ip():
    ip = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except socket.error as e:
        logger.error(e)
    if ip is None:
        raise Exception('Failed to get local host IP address.')
    return ip


IP = get_host_ip()
