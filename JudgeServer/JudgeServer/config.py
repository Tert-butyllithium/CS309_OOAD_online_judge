import os
import logzero
from logzero import logger
import logging
import datetime

FILE_TYPE = ['.c', '.cpp', '.PAS', '.java', '.py', '.py', '.kt']
Project_PATH = '/home/isc-/Desktop/CS309_OOAD_online_judge/'
# Project_PATH = 'D:/Codes/CS309_OOAD_online_judge/'
USER_CODES_FOLDER = Project_PATH + 'userCodes/'
RUN_CODE_PY = Project_PATH + 'JudgeServer/JudgeServer/Running_Code.py'

DATABASES_HOST = 'localhost'
DATABASES_USER = 'root'
DATABASES_PWD = 'yaojing01040075'
DATABASES_DB = 'db_test'

# 封装logger
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

SYSTEM_UID = 1000

OJ_JAVA_TIME_BONUS = 2
OJ_JAVA_MEMORY_BONUS = 512
