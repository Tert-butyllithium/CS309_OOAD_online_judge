import os
import logzero
from logzero import logger
import logging
import datetime

FILE_TYPE = ['.c', '.cpp', '.PAS', '.java', '.py', '.py', '.kt']
Project_PATH = '/home/isc-/Desktop/CS309_OOAD_online_judge/'      #把这行改成这个repos的路径

USER_CODES_FOLDER = Project_PATH + 'userCodes/'
RUN_CODE_PY = Project_PATH + 'JudgeServer/JudgeServer/Running_Code.py'


# 修改数据库的配置 不需要多说
DATABASES_HOST = 'localhost'
DATABASES_USER = 'root'
DATABASES_PWD = ''
DATABASES_DB = 'db_test'

# 封装logger，这里不需要修改
LOG_FILE = Project_PATH + 'JudgeServer/Log/' + str(datetime.date.today()) + '.log'
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

# 当前用户组的UID，使用这个是为了避免用root启动
SYSTEM_UID = 1000

OJ_JAVA_TIME_BONUS = 2
OJ_JAVA_MEMORY_BONUS = 512
