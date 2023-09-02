

import psutil
import time
from .cpu import CpuInfo
from .disks import DiskInfo
from .memory import MemoryInfo
from .display import DisplayInfo
from .temperature import TemperatureInfo
from .base import SysInfoBase

from twisted.internet import threads
from twisted.internet.defer import inlineCallbacks


class CustomStatusBlock(SysInfoBase):
    keys = []

    def __init__(self, actual, post_read=None):
        super(CustomStatusBlock, self).__init__(actual)
        self._post_read = post_read

    def install(self):
        super(CustomStatusBlock, self).install()
        for x in self.keys:
            if not hasattr(self, x):
                setattr(self, x, None)
        self._items = {x: x for x in self.keys}


class StatusInfo(SysInfoBase):
    def __init__(self, *args):
        super(StatusInfo, self).__init__(*args)

    def install(self):
        super(StatusInfo, self).install()
        temperature = TemperatureInfo(self.actual)
        temperature.install()
        disks = DiskInfo(self.actual)
        disks.install()
        memory = MemoryInfo(self.actual)
        memory.install()
        display = DisplayInfo(self.actual)
        display.install()
        cpu = CpuInfo(self.actual)
        cpu.install()
        self._items = {
            'uptime': self._uptime,
            'cpu': cpu,
            'disks': disks,
            'memory': memory,
            'display': display,
            'temperature': temperature,
        }

    def register_status_block(self, name, block):
        block.install()
        self._items[name] = block

    @inlineCallbacks
    def _uptime(self):
        boot_time = yield threads.deferToThread(psutil.boot_time)
        return time.time() - boot_time
