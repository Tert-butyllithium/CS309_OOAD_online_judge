import os
import sys
from config import Project_PATH
from config import FILE_TYPE
from config import USER_CODES_FOLDER
from config import logger
from config import OJ_AC
from config import OJ_WA
from config import OJ_TL
from config import OJ_ML
from config import OJ_RE
from config import OJ_CE
from TLEjudger import TimeoutThread
from config import RUN_CODE_PY
import time

WRONG_ANSWER = 0
ACCEPT = 1
TLE = 2
MLE = 3
RUNTIME_ERROR = 4
COMPILE_ERROR = 5
OTHER_ERROR = 6


class Judger(object):
    def __init__(self):
        pass

    def output_Code(self, code, language_config, append=None):
        path = USER_CODES_FOLDER
        if not os.path.exists(path):
            self.exec_cmd("mkdir " + path)
        # /home/isc-/桌面/CS309_OOAD_online_judge/userCodes/11712225/Main.cpp
        file_name = USER_CODES_FOLDER + "/Main" + FILE_TYPE[language_config]
        with open(file_name, 'w+') as file:
            saved_stdout = sys.stdout
            sys.stdout = file
            if append != None:
                print(append)
            print(code)
            sys.stdout = saved_stdout

    def compileC_CPP(self, file, append=None):
        logger.info("COMPILE COMMAND: " + 'g++ ' + file + ' -o ' + USER_CODES_FOLDER + 'Main')
        # g++ /home/isc-/桌面/CS309_OOAD_online_judge/userCodes/11712225/Main.cpp -o /home/isc-/桌面/CS309_OOAD_online_judge/userCodes/11712225/Main
        if append == None:
            command = 'g++ ' + file + ' -o ' + USER_CODES_FOLDER + 'Main'
        else:
            command = 'g++ ' + file + ' ' + append + '  -o ' + USER_CODES_FOLDER + 'Main'
        if os.system(command):
            logger.info("Compile error")
            return False
        return True

    def compile_JAVA(self, file):
        logger.info('COMPILING COMMAND: ' + "javac " + file)
        if os.system("javac " + file):
            logger.info("Compile error")
            return False
        return True

    """需要加一个新的参数 str_append， to represent the parameter in the cmd"""
    """需要把各个语言的编译单独封装"""

    def compile(self, language_config):
        # /home/isc-/桌面/CS309_OOAD_online_judge/userCodes/11712225/Main.cpp
        file = USER_CODES_FOLDER + 'Main' + FILE_TYPE[language_config]
        logger.info("COMPILING CODE: " + file)
        if language_config == 1 or language_config == 0:
            return self.compileC_CPP(file)
        elif language_config == 2:
            pass
        elif language_config == 3:
            return self.compile_JAVA(file)
        elif language_config == 6:
            pass
        return True

    def exec_cmd(self, cmd):
        r = os.popen(cmd)
        text = r.read()
        r.close()
        return text

    def run_code(self, language_config, problem_id, time_limit):
        user_folder = USER_CODES_FOLDER
        problem_folder = Project_PATH + 'data/' + str(problem_id) + '/'
        result = {
            'time': 0,
            'result': 0,
            'running_success': True
        }
        for testfile in os.listdir(problem_folder):
            if not testfile.endswith('.in'):
                continue
            # /home/isc-/桌面/CS309_OOAD_online_judge/data/1001/1.in
            input_path = problem_folder + testfile
            # /home/isc-/桌面/CS309_OOAD_online_judge/userCodes/11712225/1.out
            output_path = user_folder + testfile[0:len(testfile) - 3] + '.out'
            # /home/isc-/桌面/CS309_OOAD_online_judge/userCodes/11712225/Main
            code_file = user_folder + 'Main'

            logger.info("RUNNING CODE: " + code_file + " " + testfile)
            timeout_thread = TimeoutThread(time_limit)
            if language_config == 0 or language_config == 1:
                command = code_file + ' < ' + input_path + '> ' + output_path
                docker_command = 'docker run -v ' + RUN_CODE_PY + ':' + RUN_CODE_PY + ' -v ' + USER_CODES_FOLDER + ':' + USER_CODES_FOLDER + ' -v ' + input_path + ':' + input_path + ' judge:v2 python3 ' + RUN_CODE_PY + ' \'' + command + '\''
                logger.info('RUNNING COMMAND: ' + command)
                via_result = self.TLE_judge(timeout_thread, docker_command)
                result['result'] = via_result['result']
                result['time'] = via_result['time'] + result['time']
                # result = self.exec_cmd(command)
            elif language_config == 2:
                pass
            elif language_config == 3:
                command = 'java -cp ' + USER_CODES_FOLDER + '/ Main < ' + input_path + ' > ' + output_path
                docker_command = 'docker run -v ' + RUN_CODE_PY + ':' + RUN_CODE_PY + ' -v ' + USER_CODES_FOLDER + ':' + USER_CODES_FOLDER + ' -v ' + input_path + ':' + input_path + ' judge:v2 python3 ' + RUN_CODE_PY + ' \'' + command + '\''
                logger.info('RUNNING COMMAND: ' + command)
                via_result = self.TLE_judge(timeout_thread, docker_command)
                result['result'] = via_result['result']
                result['time'] = via_result['time'] + result['time']
                # result = self.exec_cmd(command)
            elif language_config == 4:
                command = 'python2 ' + code_file + '.py < ' + input_path + ' > ' + output_path
                docker_command = 'docker run -v ' + RUN_CODE_PY + ':' + RUN_CODE_PY + ' -v ' + USER_CODES_FOLDER + ':' + USER_CODES_FOLDER + ' -v ' + input_path + ':' + input_path + ' judge:v2 python3 ' + RUN_CODE_PY + ' \'' + command + '\''
                logger.info('RUNNING COMMAND: ' + command)
                via_result = self.TLE_judge(timeout_thread, docker_command)
                result['result'] = via_result['result']
                result['time'] = via_result['time'] + result['time']
                # result = self.exec_cmd(command)
            elif language_config == 5:
                command = 'python ' + code_file + '.py < ' + input_path + ' > ' + output_path
                docker_command = 'docker run -v ' + RUN_CODE_PY + ':' + RUN_CODE_PY + ' -v ' + USER_CODES_FOLDER + ':' + USER_CODES_FOLDER + ' -v ' + input_path + ':' + input_path + ' judge:v2 python3 ' + RUN_CODE_PY + ' \'' + command + '\''
                logger.info('RUNNING COMMAND: ' + command)
                via_result = self.TLE_judge(timeout_thread, docker_command)
                result['result'] = via_result['result']
                result['time'] = via_result['time'] + result['time']
                # result = self.exec_cmd(command)
            else:
                pass
            if result['result'] != 0:
                result['running_success'] = False
                return result
        return result

    def run(self, code, language_config, problem_id, time_limit):
        judge_result = {
            'time': 0,
            'memory': 0,
            'result': -1,
            'error': ''
        }
        self.output_Code(code, language_config)
        if not self.compile(language_config):
            judge_result['result'] = OJ_CE
            return judge_result
        runtime_result = self.run_code(language_config, problem_id, time_limit)
        logger.debug(runtime_result)
        judge_result['result'] = runtime_result['result']
        judge_result['time'] = runtime_result['time']
        if not runtime_result['running_success']:
            return judge_result
        output_folder = USER_CODES_FOLDER + '/'
        standard_output_folder = Project_PATH + 'data/' + str(problem_id) + '/'
        if not self.compare_output(output_folder, standard_output_folder):
            judge_result['result'] = OJ_WA
            return judge_result
        judge_result['result'] = OJ_AC
        os.system('rm -rf ' + USER_CODES_FOLDER + '/')
        return judge_result

    '''return the pass rate of this submission'''

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
        if success_count / file_count == 1:
            return True
        else:
            return False

    def TLE_judge(self, timeout_thread, docker_command):
        name = abs(hash(docker_command))
        # logger.debug(str(name))
        timeout_thread.container_name = name
        docker_command = docker_command[:10] + ' --name ' + str(name) + docker_command[10:]
        logger.info("DOCKER_COMMAND: " + docker_command)
        timeout_thread.start()
        start_time = time.time()
        # logger.info('DOCKER COMMAND: ' + docker_command)
        runtime_result = self.exec_cmd(docker_command)
        end_time = time.time()
        timeout_thread.setCancel()
        result = timeout_thread.result
        logger.debug(result)
        if runtime_result != '':
            result['result'] = OJ_RE
            result['running_success'] = False
        result['time'] = end_time - start_time
        return result


CPP_CODE = '#include <bits/stdc++.h>\n\nusing namespace std;\n\nint main() {\n\tint a;\n\tcin >> a;\n\tfor(int i = 0; i < a; i++) {\n\t\tcout << i << endl;\n\t}\n}'

CPP_LOOP = 'int main() {\n\twhile(1) {\n\tint a = 1;\n\tint b = 2;\n\t}}'

JAVA_CODE = 'import java.util.*;\
\
public class Main{\
	public static void main(String[] args) {\
		Scanner input = new Scanner (System.in);\
		int a = input.nextInt();\
		for(int i = 0; i < a; i++) {\
			System.out.println(i);\
		}\
	}\
}'

PY_CODE = 'a = input()\n\
for i in range(0, int(a)):\n\
	print(i)'

PY2_CODE = 'a = input()\n\
for i in range(0, int(a)):\n\
	print(i)'

C_CODE = "#include \"iostream\"\n\
int main () {\n\
	int a;\n\
	scanf(\"%d\", &a);\n\
	int i = 0;\n\
	while (i < a) {\n\
		printf(\"%d\\n\", i++);\n\
	}\n\
}"

PYTHON_TLE = 'import time \ntime.sleep(3)\n'
judger = Judger()
# judger.run(11712225, C_CODE, 0, 1001)
# print(judger.run(CPP_LOOP, 1, 1001, 1))
# print(judger.run(CPP_CODE, 1, 1001, 1))
# print(judger.run(JAVA_CODE, 3, 1001, 3))
# print(judger.run(PY_CODE, 4, 1001, 3))
# print(judger.run(PY2_CODE, 5, 1001, 3))
print(judger.run(PYTHON_TLE, 4, 1001, 3))
