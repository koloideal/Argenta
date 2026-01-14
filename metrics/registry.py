__all__ = [
    "Benchmark",
    "Benchmarks",
    "benchmark"
]

from typing import Callable, ClassVar, overload, override

BenchmarkAsFunc = Callable[[], float]


class Benchmark:
    def __init__(
            self,
            func: BenchmarkAsFunc,
            *,
            type_: str,
            name: str,
            description: str,
            iterations: int
    ) -> None:
        self.func = func
        self.type_ = type_
        self.name = name
        self.description = description
        self.iterations = iterations

    def run(self) -> float:
        return self.func()

    @override
    def __repr__(self) -> str:
        return f'Benchmark<{self.type_=}, {self.name=}, {self.description=}, {self.iterations=}>'

    @override
    def __str__(self) -> str:
        return f'Benchmark({self.type_=}, {self.name=}, {self.description=}, {self.iterations=})'


class Benchmarks:
    _benchmarks: ClassVar[list[Benchmark]] = []

    @overload
    @classmethod
    def register(
            cls,
            call: BenchmarkAsFunc,
            *,
            type_: str = "",
            description: str = "",
            iterations: int = 100,
    ) -> BenchmarkAsFunc:
        ...

    @overload
    @classmethod
    def register(
            cls,
            call: None = None,
            *,
            type_: str = "",
            description: str = "",
            iterations: int = 100,
    ) -> Callable[[BenchmarkAsFunc], BenchmarkAsFunc]:
        ...

    @classmethod
    def register(
            cls,
            call: BenchmarkAsFunc | None = None,
            *,
            type_: str = "",
            description: str = "",
            iterations: int = 100,
    ) -> Callable[[BenchmarkAsFunc], BenchmarkAsFunc] | BenchmarkAsFunc:
        def decorator(func: BenchmarkAsFunc) -> BenchmarkAsFunc:
            cls._benchmarks.append(
                Benchmark(
                    func,
                    type_=type_,
                    name=func.__name__,
                    description=description or f'description for {func.__name__} with {iterations} iterations',
                    iterations=iterations
                )
            )
            return func

        if call is None:
            return decorator
        else:
            return decorator(call)

    @classmethod
    def get_benchmarks(cls) -> list[Benchmark]:
        return cls._benchmarks


benchmark = Benchmarks.register
