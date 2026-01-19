#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''This module can be used even if you do not have Andor SDK installed on the computer
(it will just fail to connect).

Authors
-------
    Nick Metelski
    Alain Dijkstra
'''
import os
import sys
import logging
from functools import wraps

# CRITICAL: Add DLL directory to PATH before importing ATSpectrograph
dll_dir = r"C:\Program Files\Andor SDK\Python\pyAndorSpectrograph\pyAndorSpectrograph\libs\Windows\64"
os.environ['PATH'] = dll_dir + os.pathsep + os.environ.get('PATH', '')

# Python 3.8+ also needs this for DLL loading
if hasattr(os, 'add_dll_directory'):
    os.add_dll_directory(dll_dir)

from pyAndorSpectrograph.spectrograph import ATSpectrograph


def err_wrapper(func):
    """Wrapper for calls to atmcd object that takes care of the error codes."""

    @wraps(func)
    def wrapped(*args, **kwargs):
        retval = func(*args, **kwargs)
        if hasattr(retval, "__len__") and len(retval) > 1:
            err_code = retval[0]
            output = retval[1:]
            if hasattr(output, "__len__") and len(output) == 1:
                output = output[0]
        else:
            err_code = retval
            output = retval
        logging.debug(
            f'pyAndorSDK2 call to {func.__name__}, args: {args}, err code: {err_code}, output: {output}')
        return output

    return wrapped


class AndorSpectrographDiscovery(ATSpectrograph):

    def discover_hardware(self):
        self.Initialize("")
        n_devices = self.GetNumberDevices()
        # AndorSpectrographDiscovery._devices = [AndorShamrockHW(n) for n in range(n_devices)]
        # return AndorSpectrographDiscovery._devices

    def disconnect(self):
        self.Close()

    def __getattribute__(self, name):
        attr = super(AndorSpectrographDiscovery, self).__getattribute__(name)
        if callable(attr):
            attr = err_wrapper(attr)
        return attr

    def __del__(self):
        self.Close()
