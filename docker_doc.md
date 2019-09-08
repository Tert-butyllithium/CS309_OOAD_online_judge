# Docker

Docker container的构建

第一步先构建镜像：`docker build -t judger:v2 .`

第二步直接run:`docker run --mount type=bind,source=/home/data/Code/2019fall/OJ_template/Judger/demo/,target=/Judger/mount judge:v2 python3Judger/mount/demo.py`

注意第二步有几个细节，首先`source`后面跟着的应该是目标文件夹，其次目前测试出来的是在manjaro系统中，`os.system`命令会直接到根目录，所以这个时候在demo.py中应该改写成`os.system(gcc /Judger/mount/main.c -o main)`

