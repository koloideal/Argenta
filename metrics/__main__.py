from metrics.utils import attempts_to_average
from .registry import Benchmarks, Benchmark


def main():
    all_benchmarks: list[Benchmark] = Benchmarks.get_benchmarks()
    
    for benchmark in all_benchmarks:
        bench_attempts: list[float] = []
        for _ in range(benchmark.iterations):
            bench_attempts.append(benchmark.run())
            
        print(f'Name: {benchmark.name}\n' 
              f'Description: {benchmark.description}\n' 
              f'Iterations: {benchmark.iterations}\n' 
              f'Average time per iteration: {attempts_to_average(bench_attempts, benchmark.iterations)} ms\n')
        
    
if __name__ == '__main__':
    main()