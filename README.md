# 我是产品经理

## 可用的参考：

https://github.com/QingdaoU/OnlineJudge 青岛大学oj

Demo:  https://qduoj.com/ ,  http://10.20.47.211:8080/, http://10.20.97.68

## 特色功能：

- 代码补全，即可以要求用户完成一个接口，类似于LeetCode
- 代码禁止，如禁止并自动删除代码中的`#pragma GCC optimize(2)  `
- hack
- 代码查重

## 评测

- 可与web端分离
- 基于docker：如果从头写的话有一堆坑，[参考](https://docs.onlinejudge.me/#/judger/how_it_works)
- 可以正确完成评测，超时以及非法访问时可以自动结束
- 支持special judge
- 多语言支持：Java, C++, Python, Kotlin

## web-管理

- 支持markdown的文本编辑器，并支持插入图片，并支持mathjax
- 基本的文件管理，比如删除、上传和解压
- 创建比赛
- 支持从HUSTOJ无缝迁移，因为我们的题目都出在HUSTOJ上

## web-用户

- 比赛结束后可以看到比赛题目里面的所有信息，包括其他用户的提交和自己代码的评测信息
  - 注意这里要限制一下测评信息的长度，防止超限

## 题目

- 每个题目都有指定的权限，无权限表示所有用户都能访问
- 权限大致分为三种：未发布，比赛中，在题库

## 比赛

仅支持ICPC赛制，比赛可以设置距离比赛结束多长时间封榜

- 管理员和比赛创建者不受此限制

## 提交/状态

所有用户的提交，比赛中的提交会在赛后同步到这里来

- 按用户搜索

- 按题目搜索

  以上两种搜索也应该有入口在用户页和题目页

- 按照测评状态筛选

- 按语言筛选

- 按代码提交时间排序（默认）

- 按运行时间排序

- 按代码长度排序

- 按占用内存排序



# 页面

## 用户端

登录：`login ` 拿到一个token并存到session里面，`logout` 

主页：`news` 拿到所有的news

题目：

- 所有公开的题目：`problems` 所有的题目（管理员可以看到非公开的）
  
  - 每个题目包含`id`, `title`, `submisson`,`ac`
  
- 题目搜索：`find_by_id`

- 题目页点进去之后包含：`id`, `title`, `submisson`,`ac`, `time_limit`,`mem_limit`, **status**, **submit** ,`description`, `input`, `output`, `sample_input `, `sample_output`, `hint`

  `hint` 如果为空就不显示了

比赛：

- 所有公开的比赛: `contests`（管理员可以看到非公开的）

  - 题目，按照预先的顺序`find_by_contest`

    相比题目页会多一个属性`num` 表示内部的顺序

  - 提交，属于这个比赛的所有状态`find_by_contest`

    这里和外面的相比可以筛选`id` 和`author` 和`problem` 
  
    - `find_by_id_contest` 传入两个参数
    - `find_by_author_contest` 传入两个参数
    - `find_by_problem`  传入真实的problem id
  
  - ~~通知，属于这个题目的所有通知`find_by_contest`~~ 
  
  - 排名，属于这个比赛的排名`find_by_contest`
  
    和hustoj的一样就行了

状态/提交

- 所有的提交：`submission`
- `time`	`id`	`status`	`problem`	`time`	`memory`	`language`	`author`
- 筛选：`find_by_status` 根据提交测评的结果来筛选一下
- 搜索：`find_by_author` 

FAQ

一个静态的页面展示我们的编译选项

## 管理端

//TO-DO

## 其它功能

