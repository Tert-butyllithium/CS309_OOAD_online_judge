import os
import sys
import time
from config import Project_PATH
from config import SERVICE_PATH
from config import FILE_TYPE
from config import USER_CODES_FOLDER
from config import logger
from config import OJ_AC
from config import OJ_WA
from config import OJ_TL
from config import OJ_ML
from config import OJ_RE
from config import OJ_CE
from config import RUN_CODE_PY
# from Runner import DockerThread
from config import SYSTEM_UID
from config import OJ_JAVA_TIME_BONUS
from config import OJ_JAVA_MEMORY_BONUS


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
            self.exec_cmd("mkdir " + path)
        file_name = USER_CODES_FOLDER + "/Main" + FILE_TYPE[language_config]
        with open(file_name, 'w+') as file:
            saved_stdout = sys.stdout
            sys.stdout = file
            print(code)
            sys.stdout = saved_stdout
            file.close()

    def compile(self, language_config):
        def compileC_CPP(file):
            compile_result_log = f'{USER_CODES_FOLDER}/compile_result.log'
            command = f'g++ {file} -o {USER_CODES_FOLDER}Main 2> {compile_result_log}'
            logger.info(f"COMPILE COMMAND: {command}")
            if os.system(command):
                logger.info("Compile error")
                time.sleep(0.1)
                with open(compile_result_log, 'r+') as logFile:
                    result = logFile.read()
                    logFile.close()
                    if result:
                        return False, result.replace(file, 'main.cpp')
            return True, ''

        def compile_JAVA(file):
            compile_result_log = f'{USER_CODES_FOLDER}/compile_result.log'
            command = f'/usr/bin/javac {file} -d {USER_CODES_FOLDER} -encoding UTF8 2> {compile_result_log}'
            logger.info(f'COMPILING COMMAND: {command}')
            # logger.debug(self.exec_cmd(command))
            if os.system(command):
                logger.info("Compile error")
                time.sleep(0.1)
                with open(compile_result_log, 'r+') as logFile:
                    result = logFile.read()
                    logFile.close()
                    if result:
                        return False,result.replace(file, 'Main')
            return True, ''

        # /home/isc-/Desktop/CS309_OOAD_online_judge/userCodes/11712225/Main.cpp
        file = USER_CODES_FOLDER + 'Main' + FILE_TYPE[language_config]
        logger.info("COMPILING CODE: " + file)
        if language_config == 1 or language_config == 0:
            return compileC_CPP(file)
        elif language_config == 2:
            pass
        elif language_config == 3:
            return compile_JAVA(file)
        elif language_config == 6:
            pass
        return True, ''

    def run_code(self, language_config, problem_id, time_limit, memory_limit):

        def get_docker_command():
            ml = memory_limit
            tl = time_limit
            prefix = 'docker run --rm -u ' + str(SYSTEM_UID) + ':' + str(SYSTEM_UID)
            if language_config == 0 or language_config == 1:
                command = code_file + ' < ' + input_path + ' > ' + output_path
            elif language_config == 2:
                pass
            elif language_config == 3:
                command = 'java -XX:-UseCompressedClassPointers -cp ' + USER_CODES_FOLDER + '/ Main < ' + input_path + ' > ' + output_path
                tl += OJ_JAVA_TIME_BONUS
                ml += OJ_JAVA_MEMORY_BONUS
            elif language_config == 4:
                command = 'python2 ' + code_file + '.py < ' + input_path + ' > ' + output_path
            elif language_config == 5:
                command = 'python ' + code_file + '.py < ' + input_path + ' > ' + output_path
            else:
                pass
            docker_result_log = USER_CODES_FOLDER + 'docker_result.log'
            # runtime_log = USER_CODES_FOLDER + 'runtime.log'
            # command += f' 2> {runtime_log}'
            docker_command = f'{prefix} -v {Project_PATH}:{Project_PATH}  judge:v3 python3 {RUN_CODE_PY} \'{command}\' {str(tl)} {str(ml)} \'{docker_result_log}\''

            # prefix + ' -v ' + Project_PATH + ':' + Project_PATH + ' judge:v3 python3 ' + RUN_CODE_PY + ' \'' + command + '\' ' + str(
            #    tl) + ' ' + str(ml) + ' \'' + docker_result_log + '\''
            logger.info('RUNNING COMMAND: ' + command)
            name = str(abs(hash(str(time.time()) + docker_command)))
            docker_command = docker_command[: len(prefix) + 1] + '--name ' + name + ' ' + docker_command[
                                                                                          len(prefix) + 1:]
            logger.debug(docker_command)
            return docker_command, name

        user_folder = USER_CODES_FOLDER
        problem_folder = SERVICE_PATH + 'data/' + str(problem_id) + '/'
        result = {
            'time': 0,
            'result': 0,
            'memory': 0,
            'error': ''
        }
        logger.error(problem_folder)
        for testfile in os.listdir(problem_folder):
            if not testfile.endswith('.in'):
                continue
            # /home/isc-/Desktop/CS309_OOAD_online_judge/data/1001/1.in
            input_path = problem_folder + testfile
            # /home/isc-/Desktop/CS309_OOAD_online_judge/userCodes/11712225/1.out
            output_path = user_folder + testfile[0:len(testfile) - 3] + '.out'
            # /home/isc-/Desktop/CS309_OOAD_online_judge/userCodes/11712225/Main
            code_file = user_folder + 'Main'

            logger.info("RUNNING CODE: " + code_file + " " + testfile)
            # 对于不同的语言
            docker_command, docker_name = get_docker_command()
            # docker_thread = DockerThread(docker_command)
            # docker_thread.start()
            os.system(docker_command)
            docker_result_log = USER_CODES_FOLDER + '/docker_result.log'
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
            result['memory'] =max(docker_result['memoryused'], result['memory'])
            # if result['TLE'] or result['error'] or result['MLE']:
            #     return result

            # os.system('docker stop ' + docker_name)
            # os.system('docker rm ' + docker_name)
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
            judge_result['result'] = OJ_CE
            judge_result['error'] = compile_error
            os.system('rm -rf ' + USER_CODES_FOLDER)
            return judge_result

        runtime_result = self.run_code(language_config, problem_id, time_limit, memory_limit)
        logger.debug(runtime_result)
        judge_result['time'] = runtime_result['time']
        judge_result['result'] = runtime_result['result']
        judge_result['memory'] = runtime_result['memory']
        judge_result['result'] = runtime_result['result']
        judge_result['error'] = runtime_result['error']
        if judge_result['result'] == OJ_RE:
            return judge_result

        output_folder = USER_CODES_FOLDER
        standard_output_folder = SERVICE_PATH + 'data/' + str(problem_id) + '/'
        if spj == '0':
            if not self.compare_output(output_folder, standard_output_folder):
                judge_result['result'] = OJ_WA
            else:
                judge_result['result'] = OJ_AC
            os.system('rm -rf ' + USER_CODES_FOLDER + '/*')
        else:
            if not self.compare_output_spj(output_folder, standard_output_folder):
                judge_result['result'] = OJ_WA
            else:
                judge_result['result'] = OJ_AC
            os.system('rm -rf ' + USER_CODES_FOLDER + '/*')
        return judge_result

    def compare_output_spj(self, output_folder, standard_output_folder):
        logger.debug(standard_output_folder)
        spj_cpp = standard_output_folder + 'spj.cpp'
        spj_exec = spj_cpp[0:len(spj_cpp) - 4]
        if os.path.exists(spj_cpp):
            compile_result = self.exec_cmd('g++ ' + spj_cpp + ' -o ' + spj_exec)
            if compile_result:
                raise Exception("Compile spj.cpp error")
        else:
            raise Exception("File spj.cpp not found in \'" + spj_cpp + '\'')
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
            out_file_path = output_folder + out_file
            stan_file_path = standard_output_folder + out_file
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

# CPP_CODE = '#include <bits/stdc++.h>\n\nusing namespace std;\n\tint main() {\n\t\n\tint a;\n\tcin >> a;\n\tfor(int i = 0; i < a; i++) {\n\t\tcout << i << endl;\n\t}\n}'
#
# CPP_LOOP = 'int main() {\n\twhile(1) {\n\tint a = 1;\n\tint b = 2;\n\t}}'
#
# JAVA_CODE = 'import java.util.*;\
# \
# public class Main{\
# 	public static void main(String[] args) {\
# 		Scanner input = new Scanner (System.in);\
# 		int a = input.nextInt();\
# 		for(int i = 0; i < a; i++) {\
# 			System.out.println(i);\
# 		}\
# 	}\
# }'
#
# PY_CODE = 'a = input()\n\
# for i in range(0, int(a)):\n\
# 	print(i)'
#
# PY2_CODE = 'a = input()\n\
# for i in range(0, int(a)):\n\
# 	print(i)'
#
# C_CODE = "#include \"iostream\"\n\
# int main () {\n\
# 	int a;\n\
# 	scanf(\"%d\", &a);\n\
# 	int i = 0;\n\
# 	while (i < a) {\n\
# 		printf(\"%d\\n\", i++);\n\
# 	}\n\
# }"
#
# PYTHON_TLE = 'import time \ntime.sleep(90)\n'
# PYTHON_RUNTIME_RERROR = 'a = 1\nprint(a + "ss")'
# judger = Judger()
# print(judger.run(C_CODE, 0, 1001, 1))
# print(judger.run(CPP_LOOP, 1, 1001, 1))
#
# print(judger.run(CPP_CODE, 1, 1001, 1))
# print(judger.run(JAVA_CODE, 3, 1001, 3))
# print(judger.run(PY_CODE, 4, 1001, 3))
# print(judger.run(PY2_CODE, 5, 1001, 3))
# print(judger.run(PYTHON_TLE, 4, 1001, 3))
# print(judger.run(PYTHON_RUNTIME_RERROR, 4, 1001, 3))
