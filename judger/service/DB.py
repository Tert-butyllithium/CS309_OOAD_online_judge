import time

import pymysql
from config import logger
from config import IP
from config import OJ_RESULT
from config import LIMIT
from config import LANGUAGE


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
        logger.info(
            'select * from source_code sc join solution s on sc.solution_id = s.solution_id join problem p on s.problem_id = p.problem_id where s.solution_id = %s;' % str(
                 solution_id))
        cursor.execute(
             'select * from source_code sc join solution s on sc.solution_id = s.solution_id join problem p on s.problem_id = p.problem_id where s.solution_id = %s;' % str(
                solution_id))

        logger.info(solution_id)
        data = cursor.fetchone()
        if data is None:
            logger.info('Fail to query database. Delay 200ms')
            time.sleep(0.2)
            cursor.execute('select * from source_code sc join solution s on sc.solution_id = s.solution_id join problem p on s.problem_id = p.problem_id where s.solution_id = %s;' % str(solution_id))
            data = cursor.fetchone()

        # database.close()
        # code, language_config, problem, time, memory, spj
        res = [data[1], int(data[9]), data[3], data[30], int(data[31]), int(data[26])]
        problem_id =  data[3]
        logger.info(f'Search TL and ML')
        sql = f'select * from extra_time_space where problem = {problem_id}'
        database.ping(reconnect=True)
        cursor = database.cursor()
        cursor.execute(sql)
        data = cursor.fetchone()
        if data is not None:
            res[3] += int(data[1])
            res[4] += int(data[2])
        else:
            if res[1] == LANGUAGE.JAVA.value:
                res[3] += LIMIT.JAVA_TIME_BONUS.value
                res[4] += LIMIT.JAVA_SPACE_BONUS.value
            elif res[1] == LANGUAGE.PY2.value:
                res[3] += LIMIT.PYTHON_TIME_BONUS.value
                res[4] += LIMIT.PYTHON_SPACE_BONUS.value
            elif res[1] == LANGUAGE.PY3.value:
                res[3] += LIMIT.PYTHON_TIME_BONUS.value
                res[4] += LIMIT.PYTHON_SPACE_BONUS.value
            elif res[1] == LANGUAGE.KOTLIN.value:
                res[3] += LIMIT.KT_TIME_BONUS.value
                res[4] += LIMIT.KT_SAPCE_BONUS.value

        # (codes, language_config, problem_id, time_limit, memory_limit)
        # logger.debug(data)
        return res #(data[1], data[9], data[3], data[30], data[31], data[26])

    def search_submission(self):
        database = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.pwd,
            db=self.db
        )
        cursor = database.cursor()
        cursor.execute('select * from solution s where s.result = 0;')
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
        logger.info(sql)
        database.ping(reconnect=True)
        try:
            cursor.execute(sql)
            database.commit()
        except:
            logger.error("Fail to execute command \'%s\' to database" % sql)
        if result['error'] != '':
            table_name = 'compileinfo' if result['result'] == OJ_RESULT.CE.value else 'runtimeinfo'
            result['error'] = result['error'].replace('\'', '\\\'')
            sql = f"insert into {table_name} (solution_id, error) values ({solution_id}, \'{result['error']}\') ON DUPLICATE KEY update solution_id={solution_id}, error=\'{result['error']}\';"
            logger.info(sql)
            database.ping(reconnect=True)
            try:
                cursor = database.cursor()
                cursor.execute(sql)
                database.commit()
            except Exception as e:
                logger.error(f"Fail to execute command \'{sql}\' to database for : {e}")
        cursor.close()
        database.close()
