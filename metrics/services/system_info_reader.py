__all__ = [
    "SystemInfo",
    "SystemInfoGetter",
    "get_system_info"
]

from dataclasses import dataclass
import platform
import sys
from typing import Protocol

import cpuinfo
import psutil


@dataclass(frozen=True, slots=True)
class SystemInfo:
    os_info: OSInfo
    cpu_info: CPUInfo
    memory_info: MemoryInfo
    python_version: str
    python_implementation: str


@dataclass(frozen=True, slots=True)
class OSInfo:
    os_name: str
    kernel_version: str


@dataclass(frozen=True, slots=True)
class CPUInfo:
    cpu_name: str
    cpu_architecture: str
    cpu_physical_cores: int
    cpu_logical_cores: int
    cpu_max_frequency: float
    cpu_base_frequency: float


@dataclass(frozen=True, slots=True)
class MemoryInfo:
    total_ram: float # in GB
    available_ram: float # in GB
    l1_cache: float
    l2_cache: float
    l3_cache: float

    
@dataclass(frozen=True, slots=True)
class PythonInfo:
    python_version: str
    python_implementation: str
    python_compiler: str


class SystemInfoGetter(Protocol):
    def __call__(self) -> SystemInfo:
        raise NotImplementedError


def get_system_info() -> SystemInfo:
    os_info = get_os_info()
    os_name = os_info.os_name
    os_kernel_version = os_info.kernel_version

    cpu_info = cpuinfo.get_cpu_info()
    cpu_architecture = cpu_info["arch"]
    cpu_name = cpu_info["brand_raw"]

    gpu_name = get_gpu_name()

    total_ram = psutil.virtual_memory().total / (1024 ** 3)

    python_version = platform.python_version()
    python_implementation = platform.python_implementation()

    return SystemInfo(
        os_name=os_name,
        kernel_version=os_kernel_version,
        cpu_architecture=cpu_architecture,
        cpu_name=cpu_name,
        gpu_name=gpu_name,
        total_ram=total_ram,
        python_version=python_version,
        python_implementation=python_implementation,
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
            os_name=product_name,
            kernel_version=kernel_version,
        )
    elif system == "Darwin":
        return OSInfo(
            kernel_version=platform.release(),
            os_name=f"macOS {platform.mac_ver()[0]}"
        )
    else:
        return OSInfo(
            kernel_version=platform.release(),
            os_name=platform.system()
        )
