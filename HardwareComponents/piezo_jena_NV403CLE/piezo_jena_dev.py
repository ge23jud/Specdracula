#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''This module can be used even if you do not have Andor SDK installed on the computer
(it will just fail to connect).

Authors
-------
    Nick Metelski
    Alain Dijkstra
'''
import logging
from functools import wraps

import pyvisa


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


class PiezoJenaNV40Discovery():

    def discover_hardware(self):
        rm = pyvisa.ResourceManager()
        print(rm.list_resources())
        piezo = rm.open_resource('ASRL3::INSTR')
        piezo.write_termination = '\r'
        piezo.read_termination = '\r'
        piezo.baud_rate = 19200
        self.Initialize("")
        n_devices = self.GetNumberDevices()

    def disconnect(self):
        self.Close()

    def __getattribute__(self, name):
        attr = super(PiezoJenaNV40Discovery, self).__getattribute__(name)
        if callable(attr):
            attr = err_wrapper(attr)
        return attr

    def __del__(self):
        self.Close()
