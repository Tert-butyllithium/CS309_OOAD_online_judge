import time

import pymysql
from config import logger
from config import IP
from config import OJ_CE


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

        logger.debug(
            'select * from source_code sc join solution s on sc.solution_id = s.solution_id join problem p on s.problem_id = p.problem_id where s.solution_id = %s;' % str(
                 solution_id))
        cursor.execute(
             'select * from source_code sc join solution s on sc.solution_id = s.solution_id join problem p on s.problem_id = p.problem_id where s.solution_id = %s;' % str(
                solution_id))

        logger.debug(solution_id)
        data = cursor.fetchone()
        if data == None:
            logger.debug('Fail to query database. Delay 200ms')
            time.sleep(0.2)
            cursor.execute('select * from source_code sc join solution s on sc.solution_id = s.solution_id join problem p on s.problem_id = p.problem_id where s.solution_id = %s;' % str(solution_id))

        database.close()
        # (codes, language_config, problem_id, time_limit, memory_limit)
        logger.debug(data)
        return (data[1], data[9], data[3], data[30], data[31], data[26])

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

    def write_DB(self, result, solution_id):
        database = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.pwd,
            db=self.db
        )
        cursor = database.cursor()
        sql = 'update solution set time = %s, memory = %s, result = %s , judger = "%s" where solution_id = %s;' % (
            result['time'], result['memory'], result['result'], str(IP), solution_id)
        logger.debug(sql)
        database.ping(reconnect=True)
        try:
            cursor.execute(sql)
            database.commit()
        except:
            logger.error("Fail to execute command \'%s\' to database" % sql)
        if result['error'] != '':
            table_name = 'compileinfo' if result['result'] == OJ_CE else 'runtimeinfo'
            # sql = f"insert into {table_name} (solution_id, error) values ({solution_id},\'{result['error']}\')"
            sql = 'insert into %s (solution_id, error) values (%s, \'%s\');' % (
            table_name, solution_id, result['error'])
            logger.debug(sql)
            database.ping(reconnect=True)
            try:
                cursor = database.cursor()
                cursor.execute(sql)
                database.commit()
            except:
                logger.error("Fail to execute command \'%s\' to database" % sql)
        cursor.close()
        database.close()
