import os
import sys
import time
from config import Project_PATH
from config import SERVICE_PATH
from config import FILE_TYPE
from config import USER_CODES_FOLDER
from config import logger
from config import OJ_RESULT
from config import LANGUAGE
from config import RUN_CODE_PY
# from Runner import DockerThread
from config import SYSTEM_UID
# from config import OJ_JAVA_TIME_BONUS
# from config import OJ_JAVA_MEMORY_BONUS
from config import DATA_PATH
from config import DOCKER_VERSION
from multiprocessing import Pool


class Judger(object):
    def __init__(self):
        pass

    def exec_cmd(self, cmd):
        r = os.popen(cmd)
        text = r.read()
        r.close()
        return text

    def output_Code(self, code, language_config, solution_id):
        solution_folder = os.path.join(USER_CODES_FOLDER, solution_id)
        if not os.path.exists(solution_folder):
            self.exec_cmd(f"mkdir {solution_folder}")
        file_name = os.path.join(
            solution_folder, f'Main{FILE_TYPE[language_config]}')
        with open(file_name, 'w+') as file:
            saved_stdout = sys.stdout
            sys.stdout = file
            print(code)
            sys.stdout = saved_stdout
            file.close()

    def compile(self, language_config, solution_id):
        def compile_Py(file, solution_folder):
            # f'{USER_CODES_FOLDER}/compile_result.log'
            compile_result_log = os.path.join(
                solution_folder, 'compile_result.log')
            command = f'python3 -m py_compile {file} 2> {compile_result_log}'
            logger.info(f"#{solution_id}#  COMPILE COMMAND: {command}")
            os.system(command)
            time.sleep(0.1)
            log_file = open(compile_result_log, 'r')
            compile_result = log_file.read()
            log_file.close()
            if compile_result:
                logger.info(f'#{solution_id}#  Compile error')
                return False, compile_result.replace(file, 'Main.py')
            return True, ''

        def compileC_CPP(file, solution_folder):
            # f'{USER_CODES_FOLDER}/compile_result.log'
            compile_result_log = os.path.join(
                solution_folder, 'compile_result.log')
            command = f'g++ {file} -O2 -o {solution_folder}/Main 2> {compile_result_log}'
            logger.info(f"#{solution_id}# COMPILE COMMAND: {command}")
            os.system(command)
            time.sleep(0.1)
            log_file = open(compile_result_log, 'r')
            compile_result = log_file.read()
            log_file.close()
            if not os.path.exists(f'{solution_folder}/Main'):
                logger.info(f'#{solution_id}# Compile error')
                return False, 'Compile terminate because time limit'

            if compile_result and 'error:' in compile_result:
                logger.info(f'#{solution_id}# Compile error')
                return False, compile_result.replace(file, 'Main.cpp')
            return True, ''

        def compile_JAVA(file, solution_folder):
            compile_result_log = os.path.join(
                solution_folder, 'compile_result.log')
            command = f'/usr/bin/javac {file} -d {solution_folder} -encoding UTF-8 2> {compile_result_log}'
            logger.info(f'#{solution_id}# COMPILING COMMAND: {command}')
            if os.system(command):
                logger.info(f"#{solution_id}# Compile error")
                time.sleep(0.1)
                with open(compile_result_log, 'r+') as logFile:
                    result = logFile.read()
                    logFile.close()
                    if result:
                        return False, result.replace(file, 'Main.java')
            return True, ''

        def compile_Kotlin(file, solution_folder):
            compile_result_log = os.path.join(
                solution_folder, 'compile_result.log')
            command = f'kotlinc {file} -include-runtime -jvm-target 1.8 -d {solution_folder}/Main.jar 2> {compile_result_log} '
            logger.info(f'#{solution_id}# COMPILING COMMAND: {command}')
            os.system(command)
            time.sleep(0.1)
            log_file = open(compile_result_log, 'r')
            compile_result = log_file.read()
            log_file.close()
            if compile_result:
                logger.info(f'#{solution_id}# Compile error')
                return False, compile_result.replace(file, 'Main.kt')
            return True, ''
        # /home/isc-/Desktop/CS309_OOAD_online_judge/userCodes/11712225/Main.cpp
        solution_folder = os.path.join(USER_CODES_FOLDER, solution_id)
        file = os.path.join(
            solution_folder, f'Main{FILE_TYPE[language_config]}')
        logger.info(f'#{solution_id}# COMPILING CODE: {file}')
        if language_config == LANGUAGE.C.value or language_config == LANGUAGE.CPP.value:
            return compileC_CPP(file, solution_folder)
        elif language_config == LANGUAGE.PASCAL.value:
            pass
        elif language_config == LANGUAGE.JAVA.value:
            return compile_JAVA(file, solution_folder)
        elif language_config == LANGUAGE.PY2.value or language_config == LANGUAGE.PY3.value:
            return compile_Py(file, solution_folder)
        elif language_config == LANGUAGE.KOTLIN.value:
            return compile_Kotlin(file, solution_folder)
        return True, ''

    def run_code(self, language_config, problem_id, time_limit, memory_limit, solution_id):
        solution_folder = os.path.join(USER_CODES_FOLDER, solution_id)
        problem_folder = os.path.join(DATA_PATH, str(problem_id))
        result = {
            'time': 0,
            'result': 0,
            'memory': 0,
            'error': ''
        }
        # output_folder = USER_CODES_FOLDER
        # prefix = f'docker run -u {str(SYSTEM_UID)}:{str(SYSTEM_UID)} -v {Project_PATH}:{Project_PATH} {DOCKER_VERSION}'
        prefix = ''
        docker_result_log = os.path.join(solution_folder, 'docker_result.log')
        code_file = ''
        if language_config == LANGUAGE.C.value or language_config == LANGUAGE.CPP.value:
            code_file = os.path.join(solution_folder, 'Main')
        elif language_config == LANGUAGE.JAVA.value:
            code_file = os.path.join(solution_folder, 'Main')
        elif language_config == LANGUAGE.PY2.value or language_config == LANGUAGE.PY3.value:
            code_file = os.path.join(solution_folder, 'Main.py')
        elif language_config == LANGUAGE.KOTLIN.value:
            code_file = os.path.join(solution_folder, 'Main.jar')
        docker_command = f'{prefix} python3 {RUN_CODE_PY} \'{code_file}\' \'{problem_folder}\' \'{solution_folder}\' {language_config} {time_limit} {memory_limit} \'{docker_result_log}\''

        logger.debug(f'#{solution_id}# DOCKER_COMMAND: {docker_command}')
        os.system(docker_command)
        testcase_cnt = 0
        for testfile in os.listdir(problem_folder):
            if not testfile.endswith('.in'):
                continue
            testcase_cnt += 1
        start_time = time.time()
        while not os.path.exists(docker_result_log) and time.time() - start_time < 2 * time_limit * testcase_cnt:
            logger.info(f"#{solution_id}# NOT EXISTS DOCKER_RESULT_LOG")
            time.sleep(1)
        if time.time() - start_time > time_limit * testcase_cnt:
            result['result'] = OJ_RESULT.TL.value
            result['time'] = time.time() - start_time
            return result
        time.sleep(0.1)
        file = open(docker_result_log, 'r')
        docker_result = eval(file.read())
        file.close()
        logger.info(f'#{solution_id}# docker_result: {docker_result}')
        result['time'] = docker_result['timeused']
        result['error'] = docker_result['error']
        result['memory'] = docker_result['memoryused']
        result['result'] = docker_result['result']
        return result

    def run(self, code, language_config, problem_id, time_limit, memory_limit, spj, solution_id):
        solution_folder = os.path.join(USER_CODES_FOLDER, solution_id)
        judge_result = {
            'time': 0,
            'memory': 0,
            'result': -1,
            'error': ''
        }
        self.output_Code(code, language_config, solution_id)
        compile_result, compile_error = self.compile(
            language_config, solution_id)
        if not compile_result:
            judge_result['result'] = OJ_RESULT.CE.value
            judge_result['error'] = compile_error
            os.system(f'rm -rf {solution_folder}/')
            return judge_result, int(solution_id)

        runtime_result = self.run_code(
            language_config, problem_id, time_limit, memory_limit, solution_id)
        judge_result['time'] = runtime_result['time']
        judge_result['result'] = runtime_result['result']
        judge_result['memory'] = runtime_result['memory']
        judge_result['error'] = runtime_result['error']
        if judge_result['result'] == OJ_RESULT.RE.value:
            os.system(f'rm -rf {solution_folder}/')
            return judge_result,  int(solution_id)
        if judge_result['result'] == OJ_RESULT.ML.value:
            os.system(f'rm -rf {solution_folder}/')
            return judge_result,  int(solution_id)
        if judge_result['result'] == OJ_RESULT.TL.value:
            os.system(f'rm -rf {solution_folder}/')
            return judge_result,  int(solution_id)
        os.system(f'rm -rf {solution_folder}/')
        return judge_result,  int(solution_id)
