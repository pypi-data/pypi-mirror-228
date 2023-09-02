import os
import sys
import time

r=os.path.abspath(os.path.dirname(__file__))
rootpath=os.path.split(r)[0]
sys.path.append(os.path.split(r)[0])
import logging
from logging import handlers


def handle_log(log_path,log_name="AutoTest"):
    '''

    :param log_path: 必须定义日志文件需要保存的位置；
    :return:
    '''
    log_file_name = time.strftime("%Y%m%d", time.localtime())
    log_dir = os.path.join(log_path,'{}_ky{}.log'.format(log_file_name,log_name))
    kyAAT = logging.getLogger(name='kyAT')

    pycharm = logging.StreamHandler()#控制台渠道

    file = handlers.TimedRotatingFileHandler( filename=log_dir, when='D', encoding='utf-8',interval=1, backupCount=10)

    #日志格式
    fmt = '\033[35m'+'%(asctime)s-%(name)s-%(levelname)s-%(filename)s-%(funcName)s-[line:%(lineno)d]：'+\
          '\033[0m\033[34m'+'%(message)s\033[0m'
    filefmt = '%(asctime)s-%(name)s-%(levelname)s-%(filename)s-%(funcName)s-[line:%(lineno)d]：%(message)s'

    kyAAT.setLevel(logging.DEBUG)
    log_fmt = logging.Formatter(fmt=fmt)
    log_fmt2 = logging.Formatter(fmt=filefmt)

    pycharm.setFormatter(fmt=log_fmt)
    file.setFormatter(fmt=log_fmt2)

    #渠道
    kyAAT.addHandler(pycharm)
    kyAAT.addHandler(file)
    return kyAAT
log= handle_log("./")
