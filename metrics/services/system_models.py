from dataclasses import dataclass


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
    total_ram: float  # in GB
    used_ram: float  # in GB
    available_ram: float  # in GB


@dataclass(frozen=True, slots=True)
class PythonInfo:
    version: str
    implementation: str
    compiler: str


@dataclass(frozen=True, slots=True)
class SystemInfo:
    os_info: OSInfo
    cpu_info: CPUInfo
    memory_info: MemoryInfo
    python_info: PythonInfo
