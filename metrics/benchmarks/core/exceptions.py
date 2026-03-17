class BenchmarkNotFound(Exception):
    def __init__(self, benchmark_name: str):
        self.benchmark_name = benchmark_name

    def __str__(self) -> str:
        return f"Benchmark with name '{self.benchmark_name}' not found"


class BenchmarksNotFound(Exception):
    def __init__(self, type_: str):
        self.type_ = type_

    def __str__(self) -> str:
        return f"Benchmarks with type '{self.type_}' not found"


class BenchmarksWithSameNameAlreadyExists(Exception):
    def __init__(self, benchmark_name: str):
        self.benchmark_name = benchmark_name

    def __str__(self) -> str:
        return f"Benchmarks with name '{self.benchmark_name}' already exists"
