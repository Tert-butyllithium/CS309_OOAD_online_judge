import DBThread
from config import DATABASES_HOST
from config import DATABASES_USER
from config import DATABASES_PWD
from config import DATABASES_DB
from config import logger


def main():
    OJ_DB = DBThread(DATABASES_HOST, DATABASES_USER, DATABASES_PWD, DATABASES_DB)
    OJ_DB.run()

main()
