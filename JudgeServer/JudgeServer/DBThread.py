import threading
import queue
import pymysql


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
        for task in data:
            # print(task)
            # language, code, spj, time, memory, SID
            self.task_list.put((task[7], task[18], task[26], task[30], task[31], task[2]))
        database.close()

    def run(self):
        if self.task_list.empty():
            self.search_submission()
        # else:
        while not self.task_list.empty():
            task = self.task_list.get()
            language = task[0]
            code = task[1]
            spj = task[2]
            time_limit = task[3]
            memory_limit = task[4]
            SID = task[5]
#             judge

