import os
import logzero
from logzero import logger
import logging
import datetime
from enum import Enum, unique
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
Project_PATH = '/home/lumia/CS309_OOAD_online_judge'
# Project_PATH = '/home/isc-/Desktop/CS309_OOAD_online_judge'
# DATA_PATH = '/home/judge/data'
DATA_PATH = '/home/lumia/CS309_OOAD_online_judge/judger/data'

FILE_TYPE = ['.c', '.cpp', '.PAS', '.java', '.py', '.py', '.kt']
SERVICE_PATH = f'{Project_PATH}/judger'
USER_CODES_FOLDER = f'{SERVICE_PATH}/userCodes'
RUN_CODE_PY = f'{SERVICE_PATH}/service/Runner.py'

# 封装logger，这里不需要修改
LOG_FILE = f'{SERVICE_PATH}/Log/{str(datetime.date.today())}.log'
if not os.path.exists(LOG_FILE):
    log_file = open(LOG_FILE, 'w')
    log_file.close()
logzero.logfile(LOG_FILE, loglevel=logging.DEBUG)


@unique
class OJ_RESULT(Enum):
    WT0 = 0
    WA1 = 1
    CI = 2
    RI = 3
    AC = 4
    PE = 5
    WA = 6
    TL = 7
    ML = 8
    OL = 9
    RE = 10
    CE = 11
    CO = 12
    
@unique
class LANGUAGE(Enum):
    C = 0
    CPP = 1
    PASCAL = 2
    JAVA = 3
    PY2 = 4
    PY3 = 5
    KOTLIN = 6


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
