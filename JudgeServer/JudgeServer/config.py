import os
import logzero
from logzero import logger
import logging
import datetime

FILE_TYPE = ['.c', '.cpp', '.PAS', '.java', '.py', '.py', '.kt']
Project_PATH = '/home/isc-/桌面/CS309_OOAD_online_judge/'
# Project_PATH = 'D:/Codes/CS309_OOAD_online_judge/'
USER_CODES = Project_PATH + 'userCodes/'

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
