import pymysql
import docker
import threading
import time
import queue


class TimeoutThread(threading.Thread):
    def __init__(self, timeout):
        super().__init__()
        self.timeout = timeout
        self.isCancel = False

    def setCancel(self):
        self.isCancel = True

    def run(self):
        print("守护线程开始")
        try:
            time.sleep(self.timeout)
            if not self.isCancel:
                # 超时，需要杀死，这里代码还没有实现
                raise NameError('TLE')
            else:
                print(self.isCancel)
        except InterruptedError:
            print("interrupted")


class TaskThread(threading.Thread):
    def __init__(self, timeout_thread):
        super().__init__()
        self.timeout_thread = timeout_thread
        self.timeout_thread.start()

    def run(self):
        try:
            # 这里的2是假设我的代码会在两秒内完成，用来替代真实步骤
            time.sleep(2)
            client = docker.from_env()
            # 新建一个container，参数是镜像，这里是随便的一个
            client.containers.create("registry.cn-hangzhou.aliyuncs.com/onlinejudge/judge_server")
            self.timeout_thread.setCancel()
        except InterruptedError:
            print("interrupted")


class DBThread(threading.Thread):
    def __init__(self, host, user, pwd, db):
        super(DBThread, self).__init__()
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.task_list = queue.Queue()

    def search_submission(self):
        database = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.pwd,
            db=self.db
        )
        cursor = database.cursor()
        cursor.execute(
            "select * from solution s join source_code sc on s.solution_id = sc.solution_id join problem p on s.problem_id = p.problem_id where s.result = 0")
        data = cursor.fetchall()
        for task in data and self.task_list.qsize() < 21:
            self.task_list.put((task[7], task[18], task[26], task[30], task[31]))

    # def run(self):
    #     while True:
    #         if self.task_list.empty():
    #             self.search_submission()
    #         else:
    #             for task in self.task_list:


class JudgeServerClient(object):
    def judge(self, src, language_config, max_cpu_time, max_memory, test_case_id=None, test_case=None, spj_version=None,
              spj_config=None, spj_compile_config=None, spj_src=None, output=False):
        if not (test_case or test_case_id) or (test_case and test_case_id):
            raise ValueError("invalid parameter")

        data = {

        }


def main():
    OJ_DB = DBThread('localhost', 'root', 'yaojing01040075', 'db_test')

# main()
