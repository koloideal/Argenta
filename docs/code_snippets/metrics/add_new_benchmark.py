from metrics.benchmarks.entity import benchmarks

@benchmarks.register(
    type_="my_category",
    description="Description of what is being measured"
)
def benchmark_my_operation() -> None:
    # Code whose performance is being measured
    pass
