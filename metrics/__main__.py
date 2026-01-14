from .registry import Benchmarks, Benchmark


def main():
    all_benchmarks: list[Benchmark] = Benchmarks.get_benchmarks()
    
    for benchmark in all_benchmarks: pass
        
    
if __name__ == '__main__':
    main()