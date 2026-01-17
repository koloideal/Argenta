__all__ = [
    "get_kernel_version",
    "get_gpu_info"
]

import platform
import sys

import pynvml


def get_kernel_version() -> dict[str, str]:
    system = platform.system()

    if system == "Windows":
        ver = sys.getwindowsversion()
        kernel_version = f"{ver.major}.{ver.minor}.{ver.build}"

        if ver.build >= 22000:
            product_name = "Windows 11"
        else:
            product_name = "Windows 10"

        return {
            'kernel_version': kernel_version,
            'product_name': product_name
        }

    elif system == "Linux":
        return {
            'kernel_version': platform.release(),
            'product_name': platform.system()
        }

    elif system == "Darwin":
        return {
            'kernel_version': platform.release(),
            'product_name': f"macOS {platform.mac_ver()[0]}"
        }
    else:
        return {
            'kernel_version': platform.release(),
            'product_name': platform.system(),
        }

def get_gpu_info() -> str:
    try:
        pynvml.nvmlInit()
        device_count = pynvml.nvmlDeviceGetCount()
        if device_count == 0:
            return "N/A"

        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        name = pynvml.nvmlDeviceGetName(handle)

        if isinstance(name, bytes):
            name = name.decode("utf-8")

        pynvml.nvmlShutdown()
        return name
    except pynvml.NVMLError:
        return "N/A"

