__all__ = [
    "SystemInfo",
    "get_system_info"
]

from dataclasses import dataclass
import platform
import sys

import cpuinfo
import psutil


@dataclass(frozen=True, slots=True)
class SystemInfo:
    os_info: OSInfo
    cpu_info: CPUInfo
    memory_info: MemoryInfo
    python_info: PythonInfo

@dataclass(frozen=True, slots=True)
class OSInfo:
    name: str
    kernel_version: str

@dataclass(frozen=True, slots=True)
class CPUInfo:
    name: str
    architecture: str
    physical_cores: int
    logical_cores: int
    max_frequency: float

@dataclass(frozen=True, slots=True)
class MemoryInfo:
    total_ram: float # in GB
    used_ram: float # in GB
    available_ram: float # in GB

@dataclass(frozen=True, slots=True)
class PythonInfo:
    version: str
    implementation: str
    compiler: str


def get_system_info() -> SystemInfo:
    os_info = get_os_info()
    cpu_info = get_cpu_info()
    memory_info = get_memory_info()
    python_info = get_python_info()
    return SystemInfo(
        os_info=os_info,
        cpu_info=cpu_info,
        memory_info=memory_info,
        python_info=python_info,
    )

def get_os_info() -> OSInfo:
    system = platform.system()

    if system == "Windows":
        ver = sys.getwindowsversion()
        kernel_version = f"{ver.major}.{ver.minor}.{ver.build}"

        if ver.build >= 22000:
            product_name = "Windows 11"
        else:
            product_name = "Windows 10"

        return OSInfo(
            name=product_name,
            kernel_version=kernel_version,
        )
    elif system == "Darwin":
        return OSInfo(
            kernel_version=platform.release(),
            name=f"macOS {platform.mac_ver()[0]}"
        )
    else:
        return OSInfo(
            kernel_version=platform.release(),
            name=platform.system()
        )

def get_cpu_info() -> CPUInfo:
    cpu_info = cpuinfo.get_cpu_info()
    cpu_name = cpu_info["brand_raw"]
    cpu_architecture = cpu_info["arch"]
    cpu_physical_cores = psutil.cpu_count(logical=False)
    cpu_logical_cores = psutil.cpu_count(logical=True)

    cpu_freq = psutil.cpu_freq()
    cpu_max_frequency = cpu_freq.max

    return CPUInfo(
        name=cpu_name,
        architecture=cpu_architecture,
        physical_cores=cpu_physical_cores,
        logical_cores=cpu_logical_cores,
        max_frequency=cpu_max_frequency
    )

def get_memory_info() -> MemoryInfo:
    mem = psutil.virtual_memory()
    total_ram = round(mem.total / (1024**3), 2)
    used_ram = round(mem.used / (1024**3), 2)
    available_ram = round(mem.available / (1024**3), 2)

    return MemoryInfo(
        total_ram=total_ram,
        used_ram=used_ram,
        available_ram=available_ram,
    )

def get_python_info() -> PythonInfo:
    python_version = platform.python_version()
    python_implementation = platform.python_implementation()
    python_compiler = platform.python_compiler()
    return PythonInfo(
        version=python_version,
        implementation=python_implementation,
        compiler=python_compiler
    )


