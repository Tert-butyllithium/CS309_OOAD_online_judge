import threading
from DB import DB
from Judger import Judger
from config import DATABASES_HOST
from config import DATABASES_USER
from config import DATABASES_PWD
from config import DATABASES_DB
from config import logger
from config import OJ_JAVA_TIME_BONUS
from config import OJ_JAVA_MEMORY_BONUS
import queue
import os

queue_lock = threading.Lock()


class Judger_Client(object):
    def __init__(self):
        self.task_queue = queue.Queue()
        self.judger = Judger()

    def new_task(self, solution_id):
        global queue_lock
        queue_lock.acquire()
        self.task_queue.put(solution_id)
        queue_lock.release()

    def run(self):
        judging_thread = threading.Thread(target=self.judger_thread)
        judging_thread.start()

    def judger_thread(self):
        while True:
            if not self.task_queue.empty():
                os.system('docker rm $(docker ps -qf status=exited)')
                OJ_DB = DB(DATABASES_HOST, DATABASES_USER, DATABASES_PWD, DATABASES_DB)
                queue_lock.acquire()
                solution_id = self.task_queue.get()
                queue_lock.release()
                task_info = OJ_DB.search_one(solution_id)
                logger.info('_____________________START____________________________')
                logger.info('Searching solution_id: %s' % solution_id)

                # Bonus for java
                if task_info[1] == 3:
                    result = self.judger.run(task_info[0], task_info[1], task_info[2],
                                             task_info[3] + OJ_JAVA_TIME_BONUS,
                                             task_info[4] + OJ_JAVA_MEMORY_BONUS * 1024 * 1024,
                                             task_info[5])
                else:
                    result = self.judger.run(task_info[0], task_info[1], task_info[2],
                                             task_info[3],
                                             task_info[4],
                                             task_info[5])
                logger.debug('Searching end with the result \'%s\'' % result)
                OJ_DB.write_DB(result, solution_id)
                logger.info('______________________END_____________________________')
            else:
                OJ_DB = DB(DATABASES_HOST, DATABASES_USER, DATABASES_PWD, DATABASES_DB)
                list = OJ_DB.search_submission()
                queue_lock.acquire()
                for i in range(0, len(list)):
                    self.task_queue.put(list[i])
                queue_lock.release()


def main():
    # solution_i
    jc = Judger_Client()
    jc.run()
    # jc.new_task(1)


main()
