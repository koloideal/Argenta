import platform
import sys

import cpuinfo
import psutil

from metrics.services.system_models import CPUInfo, MemoryInfo, OSInfo, PythonInfo, SystemInfo

_WIN11_MIN_BUILD = 22000


def get_os_info() -> OSInfo:
    if sys.platform == "win32":
        ver = sys.getwindowsversion()
        kernel_version = f"{ver.major}.{ver.minor}.{ver.build}"
        product_name = "Windows 11" if ver.build >= _WIN11_MIN_BUILD else "Windows 10"
        return OSInfo(name=product_name, kernel_version=kernel_version)
    if sys.platform == "darwin":
        mac_version = platform.mac_ver()[0]
        return OSInfo(kernel_version=platform.release(), name=f"macOS {mac_version}")
    return OSInfo(kernel_version=platform.release(), name=platform.system())


def get_cpu_info() -> CPUInfo:
    cpu_details = cpuinfo.get_cpu_info()
    cpu_freq = psutil.cpu_freq()
    return CPUInfo(
        name=cpu_details["brand_raw"],
        architecture=cpu_details["arch"],
        physical_cores=psutil.cpu_count(logical=False) or 0,
        logical_cores=psutil.cpu_count(logical=True) or 0,
        max_frequency=cpu_freq.max,
    )


def get_memory_info() -> MemoryInfo:
    mem = psutil.virtual_memory()
    return MemoryInfo(
        total_ram=round(mem.total / (1024**3), 2),
        used_ram=round(mem.used / (1024**3), 2),
        available_ram=round(mem.available / (1024**3), 2),
    )


def get_python_info() -> PythonInfo:
    return PythonInfo(
        version=platform.python_version(),
        implementation=platform.python_implementation(),
        compiler=platform.python_compiler(),
    )


def get_system_info() -> SystemInfo:
    return SystemInfo(
        os_info=get_os_info(),
        cpu_info=get_cpu_info(),
        memory_info=get_memory_info(),
        python_info=get_python_info(),
    )
