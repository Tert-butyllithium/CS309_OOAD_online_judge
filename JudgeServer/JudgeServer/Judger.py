import os
import sys

FILE_TYPE = ['.c', '.cpp', '.PAS', '.java', '.py', '.py', '.kt']
Project_PATH = '/home/isc-/桌面/CS309_OOAD_online_judge/'
USER_CODES = Project_PATH + 'userCodes/'


class Judger(object):
    def __init__(self):
        pass

    def output_Code(self, SID, code, language_config):
        path = USER_CODES + str(SID)
        if not os.path.exists(path):
            self.exec_cmd("mkdir /home/isc-/桌面/CS309_OOAD_online_judge/userCodes/" + str(SID))
        file_name = "/home/isc-/桌面/CS309_OOAD_online_judge/userCodes/" + str(SID) + "/Main" + FILE_TYPE[language_config]
        with open(file_name, 'w+') as file:
            saved_stdout = sys.stdout
            sys.stdout = file
            print(code)
            sys.stdout = saved_stdout

    def compile(self, language_config, SID):
        # /home/isc-/桌面/CS309_OOAD_online_judge/userCodes/11712225/Main.cpp
        file = USER_CODES + str(SID) + '/Main' + FILE_TYPE[language_config]
        print("COMPILING CODE: " + file)
        if language_config == 1 or language_config == 0:
            # g++ /home/isc-/桌面/CS309_OOAD_online_judge/userCodes/11712225/Main.cpp -o /home/isc-/桌面/CS309_OOAD_online_judge/userCodes/11712225/Main
            self.exec_cmd('g++ ' + file + ' -o ' + USER_CODES + str(SID) + '/Main')
        elif language_config == 2:
            pass
        elif language_config == 3:
            self.exec_cmd("javac " + file)
        elif language_config == 6:
            pass

    def exec_cmd(self, cmd):
        r = os.popen(cmd)
        text = r.read()
        r.close()
        return text

    def run_code(self, SID, language_config, problem_id):
        user_folder = USER_CODES + str(SID) + '/'
        problem_folder = Project_PATH + 'data/' + str(problem_id) + '/'
        for testfile in os.listdir(Project_PATH + "data/1001/"):
            if not testfile.endswith('.in'):
                continue
            # /home/isc-/桌面/CS309_OOAD_online_judge/data/1001/1.in
            input_path = problem_folder + testfile
            # /home/isc-/桌面/CS309_OOAD_online_judge/userCodes/11712225/1.out
            output_path = user_folder + testfile[0:len(testfile) - 3] + '.out'
            # /home/isc-/桌面/CS309_OOAD_online_judge/userCodes/11712225/Main
            code_file = user_folder + 'Main'

            print("RUNNING CODE: " + code_file + " " + testfile)
            result = "ERROR"
            if language_config == 0 or language_config == 1:
                command = code_file + ' < ' + input_path + '> ' + output_path
                print("RUNNING COMMAND: " + command)
                result = self.exec_cmd(command)
            elif language_config == 2:
                pass
            elif language_config == 3:
                command = USER_CODES + str(SID) + '/ Main < ' + input_path + '> ' + output_path
                print('RUNNING COMMAND: java -cp ' + command)
                result = self.exec_cmd(command)
            elif language_config == 4:
                command = 'python2 ' + code_file + '.py'
                print("RUNNING COMMAND: " + command)
                result = self.exec_cmd(command)
            elif language_config == 5:
                command = 'python ' + code_file + '.py'
                print("RUNNING COMMAND: " + command)
                result = self.exec_cmd(command)
            else:
                pass
        return result

    def run(self, SID, code, language_config, problem_id):
        self.output_Code(SID, code, language_config)
        self.compile(language_config, SID)
        self.run_code(SID, language_config, problem_id)
        output_folder = USER_CODES + str(SID) + '/'
        standard_output_folder = Project_PATH + '/data/' + str(problem_id) + '/'
        pass_rate = self.compare_output(output_folder, standard_output_folder)

    '''return the pass rate of this submission'''

    def compare_output(self, output_folder, standard_output_folder):
        success_count = 0
        fail_count = 0
        user_output_list = os.listdir(output_folder)
        for out_file_path in user_output_list:
            if not out_file_path.endswith('.out'):
                continue
            stan_file_path = standard_output_folder + out_file_path
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
        return success_count / len(os.listdir(output_folder))


CPP_CODE = '#include <bits/stdc++.h>\n\nusing namespace std;\n\nint main() {\n\tint a;\n\tcin >> a;\n\tfor(int i = 0; i < a; i++) {\n\t\tcout << i << endl;\n\t}\n}'

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

PY_CODE = 'a = input()\
for i in range(0, int(a)):\
	print(i)'

PY2_CODE = 'a = input()\
for i in range(0, int(a)):\
	print(i)'
# judger = Judger()
# judger.run(11712225, CPP_CODE, 1, 1001)
