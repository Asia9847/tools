import os
import sys

BASE_DIR = os.getcwd() + "/src"

SRC_DIRS = [
    'api',
    'icons',
    'layout',
    'styles',
    'utils',
    'views',
]
DIR_LIST = []


def getdirlist():
    for dir in SRC_DIRS:
        dir = BASE_DIR + '/' + dir
        DIR_LIST.append(dir)


def createdirs():
    if not os.path.exists(BASE_DIR):
        print('src文件夹没有找到,已经自动创建')
        os.makedirs(BASE_DIR)

    for dir in DIR_LIST:
        if not os.path.exists(dir):
            os.makedirs(dir)
            print(dir + '已创建')
        else:
            print(dir + '文件夹以存在,已经跳过')

    print("运行结束")


def main():
    getdirlist()
    createdirs()


if __name__ == '__main__':
    main()
# for param in sys.argv:
#     print(param)
