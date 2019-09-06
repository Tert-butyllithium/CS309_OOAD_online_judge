# API

## 基本内容

按照POST的形式发送请求，需要`X-Judge-Server-Token`头字段，值为`sha256(token)`；

return value形式为：

```JSON
{
	err: request successfully ? null : error code
	data: request successfully ? data returned : bug reason
}
```



## 一般请求

* 用`/judge`发送请求

* 参数如下

  `src` : source code	

  `language_config` : 用的什么语言 JAVA/CPP/PYTHON

  `max_cpu_time` : xxx ms

  `max_memory`  : xxx bytes

  `test_case_id` : 某个文件夹，存下了所有tc

  `output` : 是否要返回用户输出, return for true null for else

* 返回的response：

  如果CE：

```json
{
    "err": "CompileError", 
    "data": "error resson"
}
```

​	else:

```JSON
[
    // 每个字典是跑一个tc所得到的结果
    {
        "cpu_time": xxx,
        // refer to the end of this document
        "result": result code,
        "memory": 用了多少内存,
        "real_time": 实际跑了多久,
        "signal": 0,
        "error": error code,
        // refer to the end of this document
        "exit_code": 0,
        "output_md5": "eccbc87e4b5ce2fe28308fd9f2a7baf3",
        // test case file id
        "test_case": 1
    },
    {
    
    },
]
```

* 是result 和error的返回值：

```
result:
- WRONG_ANSWER = -1 (this means the process exited normally, but the answer is wrong)
- SUCCESS = 0 (this only means the process exited normally)
- CPU_TIME_LIMIT_EXCEEDED = 1
- REAL_TIME_LIMIT_EXCEEDED = 2
- MEMORY_LIMIT_EXCEEDED = 3
- RUNTIME_ERROR = 4
- SYSTEM_ERROR = 5

error:
- SUCCESS = 0
- INVALID_CONFIG = -1
- FORK_FAILED = -2
- PTHREAD_FAILED = -3
- WAIT_FAILED = -4
- ROOT_REQUIRED = -5
- LOAD_SECCOMP_FAILED = -6
- SETRLIMIT_FAILED = -7
- DUP2_FAILED = -8
- SETUID_FAILED = -9
- EXECVE_FAILED = -10
- SPJ_ERROR = -11 (judger module will never return this value, it's used for awswer checker)
```



## SPJ

### 编译

* `/compile_spj`

* 所需参数：

  `src`: special judge soure code

  `spj_version`: version of special judge, used to determine whether to recompile special judge

  `spj_compile_config`: refer to `client/Python/languages.py`, do not need to modify generally

* return response:

  ```
  成功了 ? "success" : 
  {
  	"err": "SPJCompileError", 
      "data": "error resson"
  }
  ```

  

### 评判

* `/judge`