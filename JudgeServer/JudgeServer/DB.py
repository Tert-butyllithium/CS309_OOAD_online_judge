import threading
import queue
import pymysql


class DB(object):
    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def search_one(self, solution_id):
        database = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.pwd,
            db=self.db
        )
        cursor = database.cursor()
        cursor.execute(
            'select * from source_code sc join solution s on sc.solution_id = s.solution_id join problem p on s.problem_id = p.problem_id where s.solution_id = %s;' % str(
                solution_id))
        data = cursor.fetchone()
        # (codes, language_config, problem_id, TL, ML, SPJ)
        database.close()
        return (data[1], data[9], data[3], data[30], data[31], data[26])
        # for i in range(0, len(data)):
        #     print(str(i) + " " + str(data[i]))

    def search_submission(self):
        database = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.pwd,
            db=self.db
        )
        cursor = database.cursor()
        cursor.execute(
            'select * from solution s where s.result = 0;')
        data = cursor.fetchall()
        # Only store the solution id of the tasks have not been judged
        list = []
        for i in range(0, len(data)):
            list.append(data[i][0])
        return list

    def run(self):
        if self.task_set.empty():
            self.search_submission()
