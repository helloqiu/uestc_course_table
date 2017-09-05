# uestc course table
把电子科大课程表导入到 google calendar。

配合这个使用：
https://gist.github.com/helloqiu/6055929ac8a15af2e50a5ba02885dafd
# Usage
``` bash
$ python setup.py install
$ uestc --help
usage: uestc [-h] [-c position] [-d date] [-p address:port]

把课程表导入到 Google Calendar。

optional arguments:
  -h, --help       show this help message and exit
  -c position      课程 json 文件的位置
  -d date          开学第一周的周一的年月日，例如 2017-09-01
  -p address:port  google 当然不能国内访问啦，你需要一个 socks5 代理，例如 localhost:1080
```
# License
GPL