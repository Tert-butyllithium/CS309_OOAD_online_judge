import threading
from DB import DB
from Judger import Judger
from config import DATABASES_HOST
from config import DATABASES_USER
from config import DATABASES_PWD
from config import DATABASES_DB
from config import logger
# from config import OJ_JAVA_TIME_BONUS
# from config import OJ_JAVA_MEMORY_BONUS
from config import BACKEND_IP
from config import TOKEN
import requests
import queue
import os
import time

queue_lock = threading.Lock()


class JudgeService(object):
    def __init__(self):
        self.task_queue = queue.Queue()
        self.judger = Judger()
        self.running = False

    def new_task(self, solution_id):
        global queue_lock
        queue_lock.acquire()
        self.task_queue.put(solution_id)
        queue_lock.release()

    def run(self):
        self.running = True
        judging_thread = threading.Thread(target=self.judger_thread)
        judging_thread.start()

    def judger_thread(self):
        while True:
            if not self.task_queue.empty():
                # os.system('docker rm $(docker ps -qf status=exited)')
                OJ_DB = DB(DATABASES_HOST, DATABASES_USER, DATABASES_PWD, DATABASES_DB)
                queue_lock.acquire()
                solution_id = self.task_queue.get()
                queue_lock.release()
                task_info = OJ_DB.search_one(solution_id)
                logger.info('_____________________START____________________________')
                logger.info('Searching solution_id: %s' % solution_id)

                result = self.judger.run(task_info[0], task_info[1], task_info[2],
                                         task_info[3],
                                         task_info[4],
                                         task_info[5])
                logger.info('Searching end with the result \'%s\'' % result)
                self.notify_backend(solution_id)
                OJ_DB.write_DB(result, solution_id)
                logger.info('______________________END_____________________________')
            else:
                time.sleep(10)
                OJ_DB = DB(DATABASES_HOST, DATABASES_USER, DATABASES_PWD, DATABASES_DB)
                list_ = OJ_DB.search_submission()
                queue_lock.acquire()
                for i in range(0, len(list_)):
                    self.task_queue.put(list_[i])
                queue_lock.release()

    def notify_backend(self, solution_id):
        request_url = f'http://{BACKEND_IP}/api/finishjudge'
        para = {
            'solution_id': solution_id,
            'token': TOKEN
        }
        requests.post(request_url, json=para)
