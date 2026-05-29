import time

import numpy as np
import pyvisa
from PySide6.QtCore import QMutexLocker

import ScopeFoundry as SFT

channel_list = {'x': 0, 'y': 1, 'z': 2}
boolian_list = {True: 1, False: 0} # bool(i)
inv_boolian_list = {'1': True, '0': False}


class PiezoJenaNV40_HW(SFT.HardwareModule):
    channel_x = SFT.ParameterGroup('Channel X')
    position_x = SFT.PhysicalParameter('Position', dtype=float, parent=channel_x)
    remote_x = SFT.PhysicalParameter('Remote', dtype=bool, value=True, parent=channel_x)
    closed_loop_x = SFT.PhysicalParameter('Closed loop', dtype=bool, value=True, parent=channel_x, readonly=True)
    soft_start_x = SFT.PhysicalParameter('Soft start', dtype=bool, value=True, parent=channel_x)

    channel_y = SFT.ParameterGroup('Channel Y')
    position_y = SFT.PhysicalParameter('Position', dtype=float, parent=channel_y)
    remote_y = SFT.PhysicalParameter('Remote', dtype=bool, value=True, parent=channel_y)
    closed_loop_y = SFT.PhysicalParameter('Closed loop', dtype=bool, value=True, parent=channel_y, readonly=True)
    soft_start_y = SFT.PhysicalParameter('Soft start', dtype=bool, value=True, parent=channel_y)

    channel_z = SFT.ParameterGroup('Channel Z')
    position_z = SFT.PhysicalParameter('Position', dtype=float, parent=channel_z)
    remote_z = SFT.PhysicalParameter('Remote', dtype=bool, value=True, parent=channel_z)
    closed_loop_z = SFT.PhysicalParameter('Closed loop', dtype=bool, value=True, parent=channel_z, readonly=True)
    soft_start_z = SFT.PhysicalParameter('Soft start', dtype=bool, value=False, parent=channel_z)

    port = SFT.ObjectParameter('Port', str, value='ASRL12::INSTR', readonly=False)
    firmware = SFT.ObjectParameter('Firmware version', str, readonly=True)
    display_light = SFT.PhysicalParameter('Display illumination', float, unit='%',
                                          range=SFT.MinMaxRangeType(min=0, max=100))
    error = SFT.PhysicalParameter('Last error message', str, readonly=True)

    settling_value = SFT.ObjectParameter('Settling value', float, value=0.002, readonly=True)

    def __init__(self, *args, **kwargs):
        SFT.HardwareModule.__init__(self, *args, **kwargs)
        self.piezo = None

    def connect(self):
        rm = pyvisa.ResourceManager()
        device_list = rm.list_resources()

        if not self.port.value() in device_list:
            raise Exception('Piezo is not connected at given port.')
        self.piezo = rm.open_resource(self.port.value())
        self.piezo.write_termination = '\r'
        self.piezo.read_termination = '\r'
        self.piezo.baud_rate = 19200

        firmware = self.get_firmware_version()
        self.firmware.setValue(firmware)

        self.position_x.connect_to_hardware(
            read_func=lambda: self.get_single_position_SI('x'),
            write_func=lambda pos: self.set_position_SI('x', pos),
        )
        self.remote_x.connect_to_hardware(
            write_func=lambda rem: self.set_remote('x', rem)
        )
        self.closed_loop_x.connect_to_hardware(
            read_func=lambda: self.get_closed_loop('x'),
            write_func=lambda closed: self.set_closed_loop('x', closed)
        )
        self.soft_start_x.connect_to_hardware(
            read_func=lambda: self.get_soft_start('x'),
            write_func=lambda soft: self.set_soft_start('x', soft)
        )
        self.position_y.connect_to_hardware(
            read_func=lambda: self.get_single_position_SI('y'),
            write_func=lambda pos: self.set_position_SI('y', pos)
        )
        self.remote_y.connect_to_hardware(
            write_func=lambda rem: self.set_remote('y', rem)
        )
        self.closed_loop_y.connect_to_hardware(
            read_func=lambda: self.get_closed_loop('y'),
            write_func=lambda closed: self.set_closed_loop('y', closed)
        )
        self.soft_start_y.connect_to_hardware(
            read_func=lambda: self.get_soft_start('y'),
            write_func=lambda soft: self.set_soft_start('y', soft)
        )
        self.position_z.connect_to_hardware(
            read_func=lambda: self.get_single_position_SI('z'),
            write_func=lambda pos: self.set_position_SI('z', pos)
        )
        self.remote_z.connect_to_hardware(
            write_func=lambda rem: self.set_remote('z', rem)
        )
        self.closed_loop_z.connect_to_hardware(
            read_func=lambda: self.get_closed_loop('z'),
            write_func=lambda closed: self.set_closed_loop('z', closed)
        )
        self.soft_start_z.connect_to_hardware(
            read_func=lambda: self.get_soft_start('z'),
            write_func=lambda soft: self.set_soft_start('z', soft)
        )
        self.display_light.connect_to_hardware(
            read_func=lambda: self.get_light(),
            write_func=lambda x: self.set_light(x)
        )
        self.error.connect_to_hardware(
            read_func=lambda: self.get_error(),
        )
        self.closed_loop_x.write_to_device(True)
        self.closed_loop_y.write_to_device(True)
        self.closed_loop_z.write_to_device(True)
        self.position_x.trigger_read()
        self.position_y.trigger_read()
        self.position_z.trigger_read()
        self.remote_x.write_to_device(True)
        self.remote_y.write_to_device(True)
        self.remote_z.write_to_device(True)
        self.soft_start_x.write_to_device(True)
        self.soft_start_y.write_to_device(True)
        self.soft_start_z.write_to_device(False)
        self.display_light.trigger_read()
        self.error.trigger_read()
        self.closed_loop_x.sigValueChanged.connect(self.set_position_range_and_unit)
        self.closed_loop_y.sigValueChanged.connect(self.set_position_range_and_unit)
        self.closed_loop_z.sigValueChanged.connect(self.set_position_range_and_unit)
        self.set_position_range_and_unit()

    def set_position_range_and_unit(self):
        if self.closed_loop_x.value() is True:
            self.position_x.set_range(SFT.MinMaxRangeType(min=0, max=80e-6, decimals=8))
            self.position_x.set_unit('m')
        else:
            self.position_x.set_range(SFT.MinMaxRangeType(min=-20, max=130))
            self.position_x.set_unit('V')
        if self.closed_loop_y.value() is True:
            self.position_y.set_range(SFT.MinMaxRangeType(min=0, max=80e-6))
            self.position_y.set_unit('m')
        else:
            self.position_y.set_range(SFT.MinMaxRangeType(min=-20, max=130))
            self.position_y.set_unit('V')
        if self.closed_loop_z.value() is True:
            self.position_z.set_range(SFT.MinMaxRangeType(min=0, max=80e-6))
            self.position_z.set_unit('m')
        else:
            self.position_z.set_range(SFT.MinMaxRangeType(min=-20, max=130))
            self.position_z.set_unit('V')
        self.position_x.trigger_read()
        self.position_y.trigger_read()
        self.position_z.trigger_read()

    def __ask(self, message):
        with QMutexLocker(self.device_mutex):
            answer = self.piezo.query(message)[1:]
        return answer

    def __write(self, message):
        with QMutexLocker(self.device_mutex):
            self.piezo.write(message)

    def __read(self):
        with QMutexLocker(self.device_mutex):
            answer = self.piezo.read()[1:]
        return answer

    def __execute(self, command: str, channel=None, value=None, style='ask'):
        """Execute a device command and check if the device returned an error
        Args:
            command (str): Device command
            channel (str): Which piezo axis to address 0=x, 1=y, 2=z
            value (str): Value corresponding to the command
            style (str): can be either 'ask' or 'tell', this determines whether the function waits for an answer or not.
        Returns:
            str: Response from the device
        """
        message = command
        if not channel is None:
            message = message + ',' + str(channel)
        if not value is None:
            message = message + ',' + str(value)
        if style == 'ask':
            return self.__ask(message)
        elif style == 'tell':
            self.__write(message)
        else:
            raise ValueError("No valid style of sending a command.")

    def get_firmware_version(self):
        answer = self.__ask('ver').split(',')[1]
        # Because this weird device throws a termination character three times when asked for the firmware version
        # I need to read twice more.
        answer += '\t' + self.__read()
        answer += '\t' + self.__read()
        return answer

    def set_position_SI(self, channel: str, value):
        """Depending on whether the device is set to closed or open loop it takes volts or um as a unit for setting a value.
        Using this function I make that it takes volts or m to stick with SI units."""
        ch_nr = channel_list[channel]
        value = float(value)
        closed_loop_check = {'x': self.closed_loop_x.value(),
                             'y': self.closed_loop_y.value(),
                             'z': self.closed_loop_z.value()}
        if closed_loop_check[channel] is True:
            value = value * 1e6
        self.set_position(channel=channel, value=value)

    def set_position(self, channel: str, value):
        ch_nr = channel_list[channel]
        self.__execute(command='set', channel=ch_nr, value=str(value), style='tell')

    def get_single_position_SI(self, channel: str):
        """Depending on whether the device is set to closed or open loop it takes volts or um as a unit for setting a value.
        Using this function I make that it takes volts or m to stick with SI units."""
        ch_nr = channel_list[channel]
        position = self.get_single_position(channel=channel)
        closed_loop_check = {'x': self.closed_loop_x.value(),
                             'y': self.closed_loop_y.value(),
                             'z': self.closed_loop_z.value()}
        if closed_loop_check[channel] is True:
            position = position / 1e6
        return position

    def get_single_position(self, channel: str):
        """Because it takes a few moments for the stage to reach its final position, the current position is read in a loop until the
        stage stabilizes. As a threshold for considered stable the value of settling_value is used which can be either in the unit
        of um or in the unit V."""
        tolerance = self.settling_value.value()
        ch_nr = channel_list[channel]
        meas_old = float(self.__execute(command='rk', channel=ch_nr).split(',')[2])
        time.sleep(0.05)
        meas_new = float(self.__execute(command='rk', channel=ch_nr).split(',')[2])
        while np.abs(meas_new - meas_old) > tolerance:
            meas_old = meas_new
            meas_new = float(self.__execute(command='rk', channel=ch_nr).split(',')[2])
            time.sleep(0.05)
        return meas_new

    def get_all_positions(self):
        positions = self.__execute(command='measure').split(',')
        return positions[1], positions[2], positions[3]

    def set_remote(self, channel: str, remote: bool):
        ch_nr = channel_list[channel]
        remote_nr = boolian_list[remote]
        self.__execute(command='setk', channel=ch_nr, value=remote_nr, style='tell')

    def set_closed_loop(self, channel: str, closed_loop: bool):
        ch_nr = channel_list[channel]
        loop_nr = boolian_list[closed_loop]
        self.__execute(command='cloop', channel=ch_nr, value=loop_nr, style='tell')

    def get_closed_loop(self, channel: str):
        ch_nr = channel_list[channel]
        answer = self.__execute(command='cloop', channel=ch_nr).split(',')[2]
        return inv_boolian_list[str(answer)]

    def get_soft_start(self, channel: str):
        ch_nr = channel_list[channel]
        answer = self.__execute(command='fenable', channel=ch_nr).split(',')[2]
        return inv_boolian_list[str(answer)]

    def set_soft_start(self, channel: str, soft):
        ch_nr = channel_list[channel]
        soft_nr = boolian_list[soft]
        self.__execute(command='fenable', channel=ch_nr, value=str(soft_nr), style='tell')

    def get_light(self):
        answer = self.__execute(command='light').split(',')[1]
        percent = float(answer) * 100 / 255
        return percent

    def set_light(self, percent: float):
        value = percent * 255 / 100
        self.__execute(command='light', value=str(value), style='tell')

    def get_error(self):
        return self.__execute(command='ERR?')

    def disconnect(self):
        if self.piezo is not None:
            self.piezo.close()
            self.piezo = None
