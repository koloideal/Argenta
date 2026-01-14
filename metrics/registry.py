from typing import Any, Callable, ClassVar, ParamSpec, TypeVar, overload, override, Generic


P = ParamSpec("P")
R = TypeVar("R", default=float)


class Benchmark(Generic[P, R]):
    def __init__(
        self, 
        func: Callable[P, R], 
        *,
        name: str, 
        description: str, 
        iterations: int
    ) -> None:
        self.func = func
        self.name = name
        self.description = description
        self.iterations = iterations
        
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        return self.func(*args, **kwargs)
    
    @override
    def __repr__(self) -> str:
        return f'Benchmark<{self.name=}, {self.description=}, {self.iterations=}>'
        
    @override
    def __str__(self) -> str:
        return f'Benchmark({self.name=}, {self.description=}, {self.iterations=})'
    

class Benchmarks:
    _benchmarks: ClassVar[list[Benchmark[Any, Any]]] = []

    @overload
    @classmethod
    def register(
        cls,
        call: Callable[P, R],
        *,
        name: str = "",
        description: str = "",
        iterations: int = 100,
    ) -> Callable[P, R]: ...

    @overload
    @classmethod
    def register(
        cls,
        call: None = None,
        *,
        name: str = "",
        description: str = "",
        iterations: int = 100,
    ) -> Callable[[Callable[P, R]], Callable[P, R]]: ...

    @classmethod
    def register(
        cls,
        call: Callable[P, R] | None = None,
        *,
        name: str = "",
        description: str = "",
        iterations: int = 100,
    ) -> Callable[[Callable[P, R]], Callable[P, R]] | Callable[P, R]:
        def decorator(func: Callable[P, R]) -> Callable[P, R]:
            cls._benchmarks.append(
                Benchmark(
                    func,
                    name = name or func.__name__,
                    description = description or f'description for {name or func.__name__} with {iterations} iterations',
                    iterations = iterations
                )
            )
            return func

        if call is None:
            return decorator
        else:
            return decorator(call)
            
    @classmethod
    def get_benchmarks(cls) -> list[Benchmark[Any, Any]]:
        return cls._benchmarks
            
benchmark = Benchmarks.register
