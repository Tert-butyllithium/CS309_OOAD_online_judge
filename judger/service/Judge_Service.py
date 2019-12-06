import threading
from DB import DB
from Judger import Judger
from config import DATABASES_HOST
from config import DATABASES_USER
from config import DATABASES_PWD
from config import DATABASES_DB
from config import logger
import multiprocessing as mp
# from config import OJ_JAVA_TIME_BONUS
# from config import OJ_JAVA_MEMORY_BONUS
from config import BACKEND_IP
from config import TOKEN
from config import PROCESS_NUM
import requests
import queue
import os
import time

# queue_lock = threading.Lock()

pro_num = PROCESS_NUM
pool = mp.Pool(pro_num)
running_task = set()

class JudgeService(object):
    def __init__(self):
        self.task_queue = queue.Queue()
        self.judger = Judger()
        self.running = False
        self.OJ_DB = DB(DATABASES_HOST, DATABASES_USER,
                        DATABASES_PWD, DATABASES_DB)

    def new_task(self, solution_id):
        # global queue_lock
        # queue_lock.acquire()
        self.task_queue.put(solution_id)
        # queue_lock.release()

    def run(self):
        self.running = True
        judging_thread = threading.Thread(target=self.judger_thread)
        judging_thread.start()

    def judger_thread(self):
        last_search_time = time.time()
        while True:
            if len(running_task) != pro_num:

                if not self.task_queue.empty():
                    # queue_lock.acquire()
                    solution_id = self.task_queue.get()
                    if solution_id in running_task:
                        continue
                    else:
                        running_task.add(solution_id)
                    # queue_lock.release()
                    task_info = self.OJ_DB.search_one(solution_id)
                    logger.info(
                        f'_____________________START__{solution_id}__________________________')
                    logger.info('Searching solution_id: %s' % solution_id)
                    pool.apply_async(self.judger.run, (task_info[0], task_info[1],
                                                            task_info[2], task_info[3],
                                                            task_info[4], task_info[5], str(solution_id),), callback=process_end)
                elif time.time() - last_search_time >= 5:
                    list_ = self.OJ_DB.search_submission()
                    # queue_lock.acquire()
                    for i in range(0, len(list_)):
                        if list_[i] in running_task:
                            continue
                        self.task_queue.put(list_[i])
                    # queue_lock.release()
                    last_search_time = time.time()

    # def run_process(self):

    def notify_backend(self, solution_id):
        request_url = f'http://{BACKEND_IP}/api/finishjudge'
        para = {
            'solution_id': solution_id,
            'token': TOKEN
        }
        requests.post(request_url, json=para)


js = JudgeService()


def process_end(param):
    result, solution_id = param
    logger.info('Searching end with the result \'%s\'' % result)
    js.notify_backend(solution_id)
    js.OJ_DB.write_DB(result, solution_id)
    running_task.remove(solution_id)
    logger.info(f'______________________END_{solution_id}____________________________')
