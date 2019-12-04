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

# OJ_JAVA_TIME_BONUS = 2
# OJ_JAVA_MEMORY_BONUS = 512


# 当前用户组的UID，使用这个是为了避免用root启动
SYSTEM_UID = 1000
DOCKER_VERSION = 'judge:v4'

# 修改数据库的配置 不需要多说
DATABASES_HOST = 'localhost'
DATABASES_USER = 'lanran'
DATABASES_PWD = 'lanran'
DATABASES_DB = 'jol'

BACKEND_IP = '10.20.71.60:1235'
TOKEN = '123456'

CONFIG_PATH = os.path.abspath(os.path.dirname(__file__))
Project_PATH = os.path.split(os.path.split(CONFIG_PATH)[0])[0]
SERVICE_PATH = os.path.join(Project_PATH, 'judger')
DATA_PATH = os.path.join(SERVICE_PATH, 'data')
USER_CODES_FOLDER = os.path.join(SERVICE_PATH, 'userCodes')
TMP_PATH = os.path.join(SERVICE_PATH, 'tmp')
RUN_CODE_PY = os.path.join(os.path.join(SERVICE_PATH, 'service'), 'Runner.py')
LOG_FOLDER = os.path.join(SERVICE_PATH, 'Log')
LOG_FILE = os.path.join(LOG_FOLDER, f'{str(datetime.date.today())}.log')

FILE_TYPE = ['.c', '.cpp', '.PAS', '.java', '.py', '.py', '.kt']

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

class LIMIT(Enum):
    JAVA_TIME_BONUS = 2
    JAVA_SPACE_BONUS = 512
    PYTHON_TIME_BONUS = 2
    PYTHON_SPACE_BONUS = 512
    KT_TIME_BONUS = 2
    KT_SAPCE_BONUS = 512
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
