"""Thin, thread-safe wrapper around pylablib's Newport Picomotor 8742 driver.

pylablib's ``Picomotor8742.query`` writes a command and then reads the reply
as two separate operations on the same connection, so two threads querying at
once (e.g. a WorkerTask polling the position while the Stop button is pressed)
can steal each other's replies. Every call here goes through ``self.mutex``.

The lock is only held per command, never for the whole duration of a move, so
``stop`` can still get through while another thread waits for motion to end.

USB connections go through pyusb/libusb, which requires the controller to be
bound to the WinUSB driver (e.g. with Zadig) instead of Newport's own driver.
Ethernet connections (IP address or hostname) need no driver.
"""
import time

from PySide6.QtCore import QMutex, QMutexLocker
from pylablib.devices import Newport

AXES = (1, 2, 3, 4)


class Picomotor8742Device:
    """Open-loop control of the four Picomotor axes of a Newport 8742.

    Positions are in motor steps, counted by the controller relative to the
    last zero reference (power-up or ``set_zero``). Picomotors have no encoder,
    so the count is not an absolute mirror angle.
    """

    def __init__(self, conn='0', timeout=5.0):
        """
        Args:
            conn (str): USB device index (``'0'`` for the first controller) or
                IP address / hostname for an Ethernet connection.
            timeout (float): communication timeout in s.
        """
        self.conn = conn
        self.timeout = timeout
        self.mutex = QMutex()
        self._dev = None

    @staticmethod
    def count_usb_devices():
        """Number of 8742 controllers visible over USB."""
        return Newport.get_usb_devices_number_picomotor()

    def connect(self):
        conn = self.conn.strip()
        conn = int(conn) if conn.isdigit() else conn
        with QMutexLocker(self.mutex):
            self._dev = Newport.Picomotor8742(conn, timeout=self.timeout)

    def close(self):
        with QMutexLocker(self.mutex):
            if self._dev is not None:
                self._dev.close()
                self._dev = None

    @property
    def is_connected(self):
        return self._dev is not None

    def get_id(self):
        with QMutexLocker(self.mutex):
            return self._dev.get_id()

    def get_motor_type(self, axis):
        """One of ``'none'``, ``'unknown'``, ``'tiny'`` or ``'standard'``."""
        with QMutexLocker(self.mutex):
            return self._dev.get_motor_type(axis)

    def get_position(self, axis):
        with QMutexLocker(self.mutex):
            return int(self._dev.get_position(axis))

    def move_to(self, axis, position):
        """Start an absolute move (in steps); returns immediately."""
        with QMutexLocker(self.mutex):
            self._dev.move_to(axis, int(position))

    def move_by(self, axis, steps):
        """Start a relative move (in steps); returns immediately."""
        with QMutexLocker(self.mutex):
            self._dev.move_by(axis, int(steps))

    def is_moving(self, axis):
        with QMutexLocker(self.mutex):
            return bool(self._dev.is_moving(axis))

    def wait_move(self, axis, timeout=None, poll_interval=0.02):
        """Block until `axis` stops. Releases the lock between polls.

        Returns:
            bool: True if the axis stopped, False if `timeout` (s) ran out.
        """
        t0 = time.monotonic()
        while self.is_moving(axis):
            if timeout is not None and time.monotonic() - t0 > timeout:
                return False
            time.sleep(poll_interval)
        return True

    def stop(self, axis='all'):
        """Decelerate and stop `axis` (or all axes)."""
        with QMutexLocker(self.mutex):
            self._dev.stop(axis)

    def abort(self):
        """Abrupt stop of all axes, without deceleration."""
        with QMutexLocker(self.mutex):
            self._dev.stop('all', immediate=True)

    def set_zero(self, axis):
        """Define the current position of `axis` as 0 steps (does not move)."""
        with QMutexLocker(self.mutex):
            return int(self._dev.set_position_reference(axis, 0))

    def get_velocity_parameters(self, axis):
        """Return ``(speed, acceleration)`` in steps/s and steps/s^2."""
        with QMutexLocker(self.mutex):
            speed, accel = self._dev.get_velocity_parameters(axis)
        return int(speed), int(accel)

    def set_speed(self, axis, speed):
        with QMutexLocker(self.mutex):
            self._dev.setup_velocity(axis, speed=int(speed))

    def set_acceleration(self, axis, accel):
        with QMutexLocker(self.mutex):
            self._dev.setup_velocity(axis, accel=int(accel))
