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
            logger.info(f"COMPILE COMMAND: {command}")
            os.system(command)
            time.sleep(0.1)
            log_file = open(compile_result_log, 'r')
            compile_result = log_file.read()
            log_file.close()
            if compile_result:
                logger.info('Compile error')
                return False, compile_result.replace(file, 'Main.py')
            return True, ''

        def compileC_CPP(file, solution_folder):
            # f'{USER_CODES_FOLDER}/compile_result.log'
            compile_result_log = os.path.join(
                solution_folder, 'compile_result.log')
            command = f'g++ {file} -O2 -o {solution_folder}/Main 2> {compile_result_log}'
            logger.info(f"COMPILE COMMAND: {command}")
            os.system(command)
            time.sleep(0.1)
            log_file = open(compile_result_log, 'r')
            compile_result = log_file.read()
            log_file.close()
            if compile_result and 'error:' in compile_result:
                logger.info('Compile error')
                return False, compile_result.replace(file, 'Main.cpp')
            return True, ''

        def compile_JAVA(file, solution_folder):
            logger.debug(2)
            compile_result_log = os.path.join(
                solution_folder, 'compile_result.log')
            command = f'/usr/bin/javac {file} -d {solution_folder} -encoding UTF-8 2> {compile_result_log}'
            logger.info(f'COMPILING COMMAND: {command}')
            # logger.debug(self.exec_cmd(command))
            if os.system(command):
                logger.info("Compile error")
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
            command = f'kotlinc {file} -include-runtime -d {solution_folder}/Main.jar 2> {compile_result_log} '
            logger.info(f'COMPILING COMMAND: {command}')
            os.system(command)
            time.sleep(0.1)
            log_file = open(compile_result_log, 'r')
            compile_result = log_file.read()
            log_file.close()
            if compile_result:
                logger.info('Compile error')
                return False, compile_result.replace(file, 'Main.kt')
            return True, ''
        # /home/isc-/Desktop/CS309_OOAD_online_judge/userCodes/11712225/Main.cpp
        solution_folder = os.path.join(USER_CODES_FOLDER, solution_id)
        file = os.path.join(
            solution_folder, f'Main{FILE_TYPE[language_config]}')
        logger.info(f'COMPILING CODE: {file}')
        if language_config == LANGUAGE.C.value or language_config == LANGUAGE.CPP.value:
            return compileC_CPP(file, solution_folder)
        elif language_config == LANGUAGE.PASCAL.value:
            pass
        elif language_config == LANGUAGE.JAVA.value:
            logger.debug(1)
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
        # logger.debug(1)
        if language_config == LANGUAGE.C.value or language_config == LANGUAGE.CPP.value:
            code_file = os.path.join(solution_folder, 'Main')
        elif language_config == LANGUAGE.JAVA.value:
            code_file = os.path.join(solution_folder, 'Main')
        elif language_config == LANGUAGE.PY2.value or language_config == LANGUAGE.PY3.value:
            code_file = os.path.join(solution_folder, 'Main.py')
        elif language_config == LANGUAGE.KOTLIN.value:
            code_file = os.path.join(solution_folder, 'Main.jar')
        
        # logger.debug(2)
        docker_command = f'{prefix} python3 {RUN_CODE_PY} \'{code_file}\' \'{problem_folder}\' \'{solution_folder}\' {language_config} {time_limit} {memory_limit} \'{docker_result_log}\''

        logger.debug(f'DOCKER_COMMAND: {docker_command}')
        os.system(docker_command)
        testcase_cnt = 0
        for testfile in os.listdir(problem_folder):
            if not testfile.endswith('.in'):
                continue
            testcase_cnt += 1
        start_time = time.time()
        while not os.path.exists(docker_result_log) and time.time() - start_time < 2 * time_limit * testcase_cnt:
            logger.info("NOT EXISTS DOCKER_RESULT_LOG")
            time.sleep(1)
        if time.time() - start_time > time_limit * testcase_cnt:
            result['result'] = OJ_RESULT.TL.value
            result['time'] = time.time() - start_time
            return result
        time.sleep(0.1)
        file = open(docker_result_log, 'r')
        docker_result = eval(file.read())
        file.close()
        logger.info(f'docker_result: {docker_result}')
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
            # judge_result['error'] = judge_result['error'].replace(USER_CODES_FOLDER, '')
            # judge_result['error'] = judge_result['error'].replace('\"', '')
            # judge_result['error'] = judge_result['error'].replace('\'', '')
            return judge_result,  int(solution_id)
        if judge_result['result'] == OJ_RESULT.ML.value:
            os.system(f'rm -rf {solution_folder}/')
            return judge_result,  int(solution_id)
        if judge_result['result'] == OJ_RESULT.TL.value:
            os.system(f'rm -rf {solution_folder}/')
            return judge_result,  int(solution_id)

        # output_folder = USER_CODES_FOLDER
        # standard_output_folder = f'{DATA_PATH}/{str(problem_id)}'
        # if spj == 0:
        #     if not self.compare_output(output_folder, standard_output_folder):
        #         judge_result['result'] = OJ_RESULT.WA.value
        #     else:
        #         judge_result['result'] = OJ_RESULT.AC.value
        #     os.system(f'rm -rf {USER_CODES_FOLDER}/*')
        # else:
        #     if not self.compare_output_spj(output_folder, standard_output_folder):
        #         judge_result['result'] = OJ_RESULT.WA.value
        #     else:
        #         judge_result['result'] = OJ_RESULT.AC.value
        #     os.system(f'rm -rf {USER_CODES_FOLDER}/*')
        return judge_result,  int(solution_id)

    def compare_output_spj(self, output_folder, standard_output_folder):
        logger.info(standard_output_folder)
        spj_cpp = f'{standard_output_folder}/spj.cpp'
        spj_exec = spj_cpp[0:len(spj_cpp) - 4]
        if os.path.exists(spj_cpp):
            compile_result = self.exec_cmd(f'g++ {spj_cpp} -o {spj_exec}')
            if compile_result:
                raise Exception("Compile spj.cpp error")
        else:
            raise Exception(f'File spj.cpp not found in \'{spj_cpp}\'')
        for TC_out in os.listdir(standard_output_folder):
            if not TC_out.endswith('.out'):
                continue
            TC_out = f'{standard_output_folder}/{TC_out}'
            TC_in = TC_out[0:len(TC_out) - 4] + '.in'
            if not os.path.exists(TC_in):
                raise Exception(TC_in + ' not found but ' + TC_out + ' found')
            TC_id = TC_out[len(standard_output_folder): len(TC_out) - 4]
            user_out = output_folder + TC_id + '.out'
            if not os.path.exists(user_out):
                return False
            result = os.system(f'{spj_exec} {TC_in} {TC_out} {user_out}')
            if result != 0:
                return False
        return True

    def compare_output(self, output_folder, standard_output_folder):
        success_count = 0
        fail_count = 0
        file_count = 0
        user_output_list = os.listdir(output_folder)
        for out_file in user_output_list:
            if not out_file.endswith('.out'):
                continue
            file_count += 1
            out_file_path = f'{output_folder}/{out_file}'
            stan_file_path = f'{standard_output_folder}/{out_file}'
            outfile = open(out_file_path)
            stan_file = open(stan_file_path)
            # while outfile.newlines() :
            while outfile.readable() or stan_file.readable():
                out = outfile.readline()
                stan = stan_file.readline()
                if not out and not stan:
                    success_count += 1
                    break
                if bool(out) != bool(stan):
                    logger.debug(111111111111)
                    fail_count += 1
                    break
                if not stan and out == '\n':
                    success_count += 1
                    break
                if out.strip() != stan.strip():
                    logger.debug(222222222222222222222222)
                    fail_count += 1
                    break
            outfile.close()
            stan_file.close()
            outfile = open(out_file_path)
            stan_file = open(stan_file_path)
            logger.debug(f'out: {outfile.read()}')
            logger.debug(f'stan_file: {stan_file.read()}')
            outfile.close()
            stan_file.close()
        if success_count == file_count:
            return True
        else:
            return False
