import sys
import _judger
import subprocess


# [xxx, code, language_config, UID, max_cpu_time, max_memory, SPJ
def main(argv):
    language_config = argv[2]
    saveStdout = sys.stdout
    filetype = ['.c', '.cpp', '.PAS', '.java', '.py', '.py', '.kt']
    filename = argv[3] + filetype[language_config]
    with open(filename, 'w+') as file:
        sys.stdout = file
        print(argv[1])
        sys.stdout = saveStdout

    compile()
    SPJ = argv[6]
    if SPJ != 1:
        ret = _judger.run(max_cpu_time=argv[4],
                          max_real_time=argv[4] + 1000,
                          max_memory=argv[5],
                          max_process_number=200,
                          max_output_size=10000,
                          max_stack=32 * 1024 * 1024,
                          # five args above can be _judger.UNLIMITED
                          exe_path="main",
                          input_path="1.in",
                          output_path="1.out",
                          error_path="1.out",
                          args=[],
                          # can be empty list
                          env=[],
                          log_path="judger.log",
                          # can be None
                          seccomp_rule_name="java",
                          uid=0,
                          gid=0)


def compile():
    pass
