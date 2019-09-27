from DB import DB
from Judger import Judger
from config import DATABASES_HOST
from config import DATABASES_USER
from config import DATABASES_PWD
from config import DATABASES_DB
from config import logger


def main():
    task_set = {}
    OJ_DB = DB(DATABASES_HOST, DATABASES_USER, DATABASES_PWD, DATABASES_DB, task_set)
    OJ_DB.run()
    judger = Judger()
    while not OJ_DB.task_set.empty():
        task = OJ_DB.task_set.get()
        # logger.debug(task)
        language = task[0]
        code = task[1]
        spj = task[2]
        time_limit = task[3]
        memory_limit = task[4]
        SID = task[5]
        problem_id = task[6]
        judger.run(SID, code, language, problem_id)

main()
