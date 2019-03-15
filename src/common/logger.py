#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys
import logging
import time
import ctypes
import inspect
import multiprocessing as mp
import threading

STD_OUTPUT_HANDLE = -11
FOREGROUND_BLUE = 0x01
FOREGROUND_GREEN = 0x02
FOREGROUND_RED = 0x04
FOREGROUND_INTENSITY = 0x08

win_platform = sys.platform.startswith('win')
win_console = sys.stdin.isatty()


class WinColor(object):

    def __init__(self):
        super(WinColor, self).__init__()

    @staticmethod
    def set_cmd_color(color):
        std_out_handle = ctypes.windll.kernel32.GetstdHandle(STD_OUTPUT_HANDLE)
        res_bool = ctypes.windll.kernel32.SetConsoleTextAttribute(std_out_handle, color)
        return res_bool

    def reset_color(self):
        self.set_cmd_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)

    def red(self, log_str):
        self.set_cmd_color(FOREGROUND_RED | FOREGROUND_INTENSITY)
        self.reset_color()
        return log_str

    def green(self, log_str):
        self.set_cmd_color(FOREGROUND_GREEN | FOREGROUND_INTENSITY)
        self.reset_color()
        return log_str

    def blue(self, log_str):
        self.set_cmd_color(FOREGROUND_BLUE | FOREGROUND_INTENSITY)
        self.reset_color()
        return log_str


def _warp_with(level, code):
    def inner(text, bold=False):
        c = code
        if bold:
            c = "1;%s" % c
        text_with_color = "\033[%sm%s\033[0m" % (c, text)
        console_print(level, text_with_color)
        return text_with_color
    return inner


win_color = WinColor()
red = win_color.red if (win_platform and win_console) else _warp_with(logging.ERROR, '31')
green = win_color.green if (win_platform and win_console) else _warp_with(logging.INFO, '32')
blue = win_color.blue if (win_platform and win_console) else _warp_with(logging.WARNING, '34')


def log_cur_time():
    return time.strftime('%Y-%m-%d %H:%M:%S')


def set_log(log_name):
    formatter = logging.Formatter("%(message)s")
    logger_ = logging.getLogger(__name__)
    hdlr = logging.FileHandler(log_name)
    hdlr.setFormatter(formatter)
    logger_.addHandler(hdlr)
    logger_.setLevel(logging.DEBUG)
    return logger_


def console_print(print_level, log_str):
    if print_level <= log_str:
        print log_str


class LogAndPrint:
    def __init__(self, full_log_path):
        self.temp_logger = set_log(full_log_path)

    def info_log(self, info):
        f = inspect.currentframe().f_back
        path, mod = os.path.split(f.f_code.co_filename)
        line_no = f.f_lineno
        func_name = f.f_code.co_name
        process_name = mp.current_process().name
        thread_name = threading.currentThread().getName()
        info_log = '%s INFO %s %s %s %s [line:%s] : %s' % (log_cur_time(), process_name, thread_name, mod, func_name,
                                                         line_no, info)
        return info_log

    def info(self, info_str):
        info_log = LogAndPrint.info_log(self, info_str)
        self.temp_logger.info(green(info_log))

    def error(self, error_str):
        error_log = LogAndPrint.info_log(self, error_str)
        self.temp_logger.error(red(error_log))

    def warning(self, warning_str):
        warning_log = LogAndPrint.info_log(self, warning_str)
        self.temp_logger.warning(blue(warning_log))


def set_test_log():
    path_, file_ = os.path.split(sys.argv[0])
    para = time.strftime('%Y%m%d%H%M%S')
    temp_log_name = file_[:-3]
    log_dir = os.path.join(sys.path[0], 'log', temp_log_name)
    if os.path.exists(log_dir) is False:
        os.makedirs(log_dir)
    full_log_name_ = os.path.join(log_dir, temp_log_name + para + '.log')
    logger_ = LogAndPrint(full_log_name_)
    return logger_


log_level = logging.DEBUG
logger = set_test_log()



