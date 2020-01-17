#-*- coding:utf-8 -*-
'''
Created on 2018年9月29日
@author: 
Description:  二次封装的日志库

'''


'''
Implements a simple log library.
 
This module is a simple encapsulation of logging module to provide a more
convenient interface to write log. The log will both print to stdout and
write to log file. It provides a more flexible way to set the log actions,
and also very simple. See examples showed below:
 
Example 1: Use default settings

    import log
 
    log.debug('hello, world')
    log.info('hello, world')
    log.warning('hello, world')
    log.error('hello, world')
    log.critical('hello, world')
    log.exception('hello, world')
 
Result:
Print all log messages to file, and only print log whose level is greater
than ERROR to stdout. The log file is located in '/logs/xxx.log' if the module 
name is xxx.py. The default log file handler is size-rotated, if the log 
file's size is greater than 20M, then it will be rotated.
 
Example 2: Use set_logger to change settings
 
    # Change limit size in bytes of default rotating action
    log.set_logger(limit = 10240) # 10M
 
    # Use time-rotated file handler, each day has a different log file, see
    # logging.handlers.TimedRotatingFileHandler for more help about 'when'
    log.set_logger(when = 'D', limit = 1)
 
    # Use normal file handler (not rotated)
    log.set_logger(backup_count = 0)
 
    # File log level set to INFO, and stdout log level set to DEBUG
    log.set_logger(level = 'DEBUG:INFO')
 
    # Both log level set to INFO
    log.set_logger(level = 'INFO')
 
    # Change default log file name and log mode
    log.set_logger(filename = 'logs.log', mode = 'w')
 
    # Change default log formatter
    log.set_logger(fmt = '[%(levelname)s] %(message)s'
'''
 
__author__ = "tuantuan.lv <dangoakachan@foxmail.com>"
__status__ = "Development"
 
__all__ = ['set_logger', 'debug', 'info', 'warning', 'error',
           'critical', 'exception']
 
import os
import sys
import logging.handlers
import getcwd
from framework.func import mkDirs

 
# Color escape string
COLOR_RED='\033[1;31m'
COLOR_GREEN='\033[1;32m'
COLOR_YELLOW='\033[1;33m'
COLOR_BLUE='\033[1;34m'
COLOR_PURPLE='\033[1;35m'
COLOR_CYAN='\033[1;36m'
COLOR_GRAY='\033[1;37m'
COLOR_WHITE='\033[1;38m'
COLOR_RESET='\033[1;0m'
 
# Define log color
LOG_COLORS = {
    'DEBUG': '%s',
    'INFO': COLOR_GREEN + '%s' + COLOR_RESET,
    'WARNING': COLOR_YELLOW + '%s' + COLOR_RESET,
    'EXCEPTION': COLOR_RED + '%s' + COLOR_RESET,
    'ERROR': COLOR_RED + '%s' + COLOR_RESET,
    'CRITICAL': COLOR_RED + '%s' + COLOR_RESET,
}
 
# Global logger
g_logger = None
 
class ColoredFormatter(logging.Formatter):
    '''A colorful formatter.'''
 
    def __init__(self, fmt = None, datefmt = None):
        logging.Formatter.__init__(self, fmt, datefmt)
 
    def format(self, record):
        level_name = record.levelname
        msg = logging.Formatter.format(self, record)
 
        return LOG_COLORS.get(level_name, '%s') % msg
 
def add_handler(cls, level, fmt, colorful, **kwargs):
    '''Add a configured handler to the global logger.'''
    global g_logger
 
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.DEBUG)
 
    handler = cls(**kwargs)
    handler.setLevel(level)
 
    if colorful:
        formatter = ColoredFormatter(fmt)
    else:
        formatter = logging.Formatter(fmt)
 
    handler.setFormatter(formatter)
    g_logger.addHandler(handler)
 
    return handler
 
def add_streamhandler(level, fmt):
    '''Add a stream handler to the global logger.'''
    return add_handler(logging.StreamHandler, level, fmt, True)
 
def add_filehandler(level, fmt, filename , mode, backup_count, limit, when,encoding):
    '''Add a file handler to the global logger.'''
    kwargs = {}
 
    # If the filename is not set, use the default filename
    if filename is None:
        filename = getattr(sys.modules['__main__'], '__file__', 'log.py')
        filename = os.path.basename(filename.replace('.py', '.log'))
        filepath=os.path.join(getcwd.get_cwd(),'logs')
        mkDirs(filepath)#如果没有这个文件夹就新建
        filename = os.path.join(filepath, filename)
 
    kwargs['filename'] = filename   #文件名
    kwargs['encoding'] = encoding   #文件编码
 
    # Choose the filehandler based on the passed arguments
    if backup_count == 0: # Use FileHandler
        cls = logging.FileHandler
        kwargs['mode' ] = mode
    elif when is None:  # Use RotatingFileHandler
        cls = logging.handlers.RotatingFileHandler  #基于文件大小切分
        kwargs['maxBytes'] = limit  #切分后的每个文件大小
        kwargs['backupCount'] = backup_count    #切分文件数
        kwargs['mode' ] = mode
    else: # Use TimedRotatingFileHandler
        cls = logging.handlers.TimedRotatingFileHandler #基于文件日期切分，按天切分
        kwargs['when'] = when
        kwargs['interval'] = limit  #切分后的每个文件大小
        kwargs['backupCount'] = backup_count    #切分文件数
 
    return add_handler(cls, level, fmt, False, **kwargs)
 
def init_logger():
    '''Reload the global logger.'''
    global g_logger
 
    if g_logger is None:
        g_logger = logging.getLogger()
    else:
        logging.shutdown()
        g_logger.handlers = []
 
    g_logger.setLevel(logging.DEBUG)  
 
def set_logger(filename = None, mode = 'a', level='WARNING:DEBUG',
               fmt = '[%(asctime)s] [%(levelname)s] %(message)s',
               backup_count = 5, limit = 1024 * 100, when = None,encoding='utf-8'):
    '''Configure the global logger.
     level ：设置日志级别，该级别及以上级别 的日志才会输出到控制台：写入文件。日志级别debug < info < warning < exception < error < critical
     backup_count： 是保留日志个数，默认的0是不会自动删除掉日志
     limit：文件大小 Bytes
     '''
    level = level.split(':')
    if len(level) == 1: # Both set to the same level
        s_level = f_level = level[0]
    else:
        s_level = level[0]  # StreamHandler log level
        f_level = level[1]  # FileHandler log level
 
    init_logger()
    add_streamhandler(s_level, fmt)#控制台输出
    add_filehandler(f_level, fmt, filename, mode, backup_count, limit, when,encoding)#文件输出
 
    # Import the common log functions for convenient
    import_log_funcs()
 
def import_log_funcs():
    '''Import the common log functions from the global logger to the module.'''
    global g_logger
 
    curr_mod = sys.modules[__name__]
    log_funcs = ['debug', 'info', 'warning', 'exception', 'error',
                 'critical']
 
    for func_name in log_funcs:
        func = getattr(g_logger, func_name)
        setattr(curr_mod, func_name, func)
 

'''=====================================================================
下面这组方法没有做任何操作，仅仅是让在eclipse环境下其他程序调用时不会出现红叉
去掉这组方法不会影响程序的运行
'''
def debug(self, msg=""):  
    '''output DEBUG level LOG'''
    pass  

def info(self, msg=""):  
    ''' output INFO level LOG '''  
    pass  

def warning(self, msg=""):  
    '''  output WARN level LOG '''  
    pass  

def error(self, msg=""):  
    ''' output ERROR level LOG '''  
    pass  

def critical(self, msg=""):  
    ''' output FATAL level LOG '''  
    pass  

def exception(self, msg=""):  
    ''' output Exception stack LOG '''  
    pass  
'''==================================================================='''

# Set a default logger
set_logger()

