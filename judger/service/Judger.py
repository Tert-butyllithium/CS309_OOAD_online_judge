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
from config import OJ_JAVA_TIME_BONUS
from config import OJ_JAVA_MEMORY_BONUS
from config import DATA_PATH


class Judger(object):
    def __init__(self):
        pass

    def exec_cmd(self, cmd):
        r = os.popen(cmd)
        text = r.read()
        r.close()
        return text

    def output_Code(self, code, language_config):
        path = USER_CODES_FOLDER
        if not os.path.exists(path):
            self.exec_cmd(f"mkdir {path}")
        file_name = f'{USER_CODES_FOLDER}/Main{FILE_TYPE[language_config]}'
        with open(file_name, 'w+') as file:
            saved_stdout = sys.stdout
            sys.stdout = file
            print(code)
            sys.stdout = saved_stdout
            file.close()

    def compile(self, language_config):
        def compileC_CPP(file):
            compile_result_log = f'{USER_CODES_FOLDER}/compile_result.log'
            command = f'g++ {file} -o {USER_CODES_FOLDER}/Main 2> {compile_result_log}'
            logger.info(f"COMPILE COMMAND: {command}")
            os.system(command)
            time.sleep(0.1)
            log_file = open(compile_result_log, 'r')
            compile_result = log_file.read()
            log_file.close()
            if compile_result:
                logger.info('Compile error')
                return False, compile_result.replace(file, 'Main.cpp')
            return True, ''


        def compile_JAVA(file):
            compile_result_log = f'{USER_CODES_FOLDER}/compile_result.log'
            command = f'/usr/bin/javac {file} -d {USER_CODES_FOLDER} -encoding UTF-8 2> {compile_result_log}'
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
        def compile_Kotlin(file):
            compile_result_log = f'{USER_CODES_FOLDER}/compile_result.log'
            command = f'kotlinc {file} -include-runtime -d {USER_CODES_FOLDER}/Main.jar 2> {compile_result_log} '
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
        file = f'{USER_CODES_FOLDER}/Main{FILE_TYPE[language_config]}'
        logger.info(f'COMPILING CODE: {file}')
        if language_config == LANGUAGE.C.value or language_config == LANGUAGE.CPP.value:
            return compileC_CPP(file)
        elif language_config == LANGUAGE.PASCAL.value:
            pass
        elif language_config == LANGUAGE.JAVA.value:
            return compile_JAVA(file)
        elif language_config == LANGUAGE.PY2.value or language_config == LANGUAGE.PY3.value:
            return True, ''
        elif language_config == LANGUAGE.KOTLIN.value:
            return compile_Kotlin(file)
        return True, ''

    def run_code(self, language_config, problem_id, time_limit, memory_limit):

        def get_docker_command():
            ml = memory_limit
            tl = time_limit
            prefix = f'docker run --rm -u {str(SYSTEM_UID)}:{str(SYSTEM_UID)}'
            command = ''
            if language_config == LANGUAGE.C.value or language_config == LANGUAGE.CPP.value:
                command = f'{code_file} < {input_path} > {output_path} 2> {error_file}'
            elif language_config == LANGUAGE.PASCAL.value:
                pass
            elif language_config == LANGUAGE.JAVA.value:
                command = f'java -XX:-UseCompressedClassPointers -cp {USER_CODES_FOLDER}/ Main < {input_path} > {output_path} 2> {error_file}'
                tl += OJ_JAVA_TIME_BONUS
                ml += OJ_JAVA_MEMORY_BONUS
            elif language_config == LANGUAGE.PY2.value:
                command = f'python2 {code_file}.py < {input_path} > {output_path} 2> {error_file}'
            elif language_config == LANGUAGE.PY3.value:
                command = f'python3 {code_file}.py < {input_path} > {output_path} 2> {error_file}'
            elif language_config == LANGUAGE.KOTLIN.value:
                command = f'java -XX:-UseCompressedClassPointers -jar {code_file}.jar < {input_path} > {output_path} 2> {error_file}'
                tl += OJ_JAVA_TIME_BONUS
                ml += OJ_JAVA_MEMORY_BONUS
            else:
                logger.error(f'Error! Cannot recognize language.')
            docker_result_log = f'{USER_CODES_FOLDER}/docker_result.log'
            docker_command = f'{prefix} -v {Project_PATH}:{Project_PATH}  judge:v3 python3 {RUN_CODE_PY} \'{command}\' {str(tl)} {str(ml)} \'{docker_result_log}\''

            logger.info('RUNNING COMMAND: ' + command)
            logger.debug(docker_command)
            return docker_command

        user_folder = USER_CODES_FOLDER
        problem_folder = f'{DATA_PATH}/{str(problem_id)}'
        result = {
            'time': 0,
            'result': 0,
            'memory': 0,
            'error': ''
        }
        logger.info(problem_folder)
        for testfile in os.listdir(problem_folder):
            if not testfile.endswith('.in'):
                continue
            # /home/isc-/Desktop/CS309_OOAD_online_judge/data/1001/1.in
            input_path = f'{problem_folder}/{testfile}'
            # /home/isc-/Desktop/CS309_OOAD_online_judge/userCodes/11712225/1.out
            output_path = f'{user_folder}/{testfile[0:len(testfile) - 3]}.out'
            # /home/isc-/Desktop/CS309_OOAD_online_judge/userCodes/11712225/Main
            code_file = f'{user_folder}/Main'
            #
            error_file = f'{user_folder}/{testfile[0:len(testfile) - 3]}.err'

            logger.info(f'RUNNING CODE: {code_file} {testfile}')
            # 对于不同的语言
            docker_command = get_docker_command()
            # docker_thread = DockerThread(docker_command)
            # docker_thread.start()
            os.system(docker_command)
            docker_result_log = f'{USER_CODES_FOLDER}/docker_result.log'
            while not os.path.exists(docker_result_log):
                logger.debug("NOT EXISTS DOCKER_RESULT_LOG")
                time.sleep(1)
                pass
            time.sleep(0.1)
            file = open(docker_result_log, 'r')
            docker_result = eval(file.read())
            file.close()
            logger.debug(docker_result)
            result['time'] = max(docker_result['timeused'], result['time'])
            # result['TLE'] = docker_result['TLE']
            result['result'] = docker_result['result']
            result['error'] = docker_result['error']
            result['memory'] = max(docker_result['memoryused'], result['memory'])
        return result

    def run(self, code, language_config, problem_id, time_limit, memory_limit, spj):
        judge_result = {
            'time': 0,
            'memory': 0,
            'result': -1,
            'error': ''
        }
        self.output_Code(code, language_config)
        compile_result, compile_error = self.compile(language_config)

        if not compile_result:
            judge_result['result'] = OJ_RESULT.CE.value
            judge_result['error'] = compile_error
            os.system(f'rm -rf {USER_CODES_FOLDER}/*')
            return judge_result

        runtime_result = self.run_code(language_config, problem_id, time_limit, memory_limit)
        logger.debug(runtime_result)
        judge_result['time'] = runtime_result['time']
        judge_result['result'] = runtime_result['result']
        judge_result['memory'] = runtime_result['memory']
        judge_result['result'] = runtime_result['result']
        judge_result['error'] = runtime_result['error']
        if judge_result['result'] == OJ_RESULT.RE.value:
            return judge_result

        output_folder = USER_CODES_FOLDER
        standard_output_folder = f'{DATA_PATH}/{str(problem_id)}'
        if spj == '0':
            if not self.compare_output(output_folder, standard_output_folder):
                judge_result['result'] = OJ_RESULT.WA.value
            else:
                logger.debug(judge_result)
                judge_result['result'] = OJ_RESULT.AC.value
                logger.debug(OJ_RESULT.AC.value)
                logger.debug(judge_result)
            os.system(f'rm -rf {USER_CODES_FOLDER}/*')
        else:
            if not self.compare_output_spj(output_folder, standard_output_folder):
                judge_result['result'] = OJ_RESULT.WA.value
            else:
                judge_result['result'] = OJ_RESULT.AC.vlaue
            os.system(f'rm -rf {USER_CODES_FOLDER}/*')
        return judge_result

    def compare_output_spj(self, output_folder, standard_output_folder):
        logger.debug(standard_output_folder)
        spj_cpp = f'{standard_output_folder}spj.cpp'
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
            TC_out = standard_output_folder + TC_out
            TC_in = TC_out[0:len(TC_out) - 4] + '.in'
            if not os.path.exists(TC_in):
                raise Exception(TC_in + ' not found but ' + TC_out + ' found')
            TC_id = TC_out[len(standard_output_folder): len(TC_out) - 4]
            user_out = output_folder + TC_id + '.out'
            if not os.path.exists(user_out):
                return False
            result = os.system(spj_exec + ' ' + TC_in + ' ' + TC_out + ' ' + user_out)
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
                    fail_count += 1
                    break
                if not stan and out == '\n':
                    success_count += 1
                    break
                if out.strip() != stan.strip():
                    fail_count += 1
                    break
            outfile.close()
            stan_file.close()
        if success_count == file_count:
            return True
        else:
            return False
