"""
대용량 데이터 파이프라인 메모리 프로파일링 프로그램

이 프로그램은 대용량 데이터(1,000만 개의 정수)를 처리할 때 List Comprehension과
Generator Expression의 메모리 사용량을 tracemalloc으로 측정하고 비교하는 기능을 제공합니다.

주요 기능:
- List Comprehension과 Generator Expression의 메모리 점유율 측정 (tracemalloc)
- Lazy Evaluation(지연 평가) 원리 설명 및 비교

변경 내역:
- 2026-01-12 [김준서(C1098)]: 초기 버전 생성 (대용량 데이터 메모리 프로파일링)
"""

import tracemalloc


# List Comprehension 방식: 1,000만 개의 정수를 리스트로 생성하고 처리합니다.
# Args: n (int) - 생성할 정수의 개수 (기본값: 10,000,000)
# Returns: tuple - (총합, 메모리 사용량 정보)
def process_with_list_comprehension(n=10000000):
    # List Comprehension으로 모든 데이터를 메모리에 생성
    numbers = [i for i in range(n)]
    
    # 총합 계산
    total = sum(numbers)
    
    # 현재 메모리 사용량 측정
    current, peak = tracemalloc.get_traced_memory()
    
    return total, current, peak


# Generator Expression 방식: 제너레이터 표현식을 사용하여 지연 평가로 처리합니다.
# Args: n (int) - 생성할 정수의 개수 (기본값: 10,000,000)
# Returns: tuple - (총합, 메모리 사용량 정보)
def process_with_generator_expression(n=10000000):
    # Generator Expression으로 데이터를 지연 평가로 생성
    numbers = (i for i in range(n))
    
    # 총합 계산 (이때 실제로 값들이 생성됨)
    total = sum(numbers)
    
    # 현재 메모리 사용량 측정
    current, peak = tracemalloc.get_traced_memory()
    
    return total, current, peak


# 메모리 사용량을 비교하고 결과를 출력하는 함수
def compare_memory_usage():
    n = 10000000  # 1,000만 개
    
    print("대용량 데이터 파이프라인 메모리 프로파일링")
    print(f"처리할 데이터 개수: {n:,}개")
    print()
    
    # 1) List Comprehension 방식 메모리 측정
    print("1) List Comprehension 방식 메모리 측정:")
    print("   - 모든 데이터를 메모리에 한 번에 생성 (Eager Evaluation)")
    
    tracemalloc.start()
    list_total, list_current, list_peak = process_with_list_comprehension(n)
    tracemalloc.stop()
    
    print(f"   총합: {list_total:,}")
    print(f"   현재 메모리: {list_current / 1024 / 1024:.2f} MB")
    print(f"   최대 메모리: {list_peak / 1024 / 1024:.2f} MB")
    print()
    
    # 2) Generator Expression 방식 메모리 측정
    print("2) Generator Expression 방식 메모리 측정:")
    print("   - 데이터를 필요할 때만 생성 (Lazy Evaluation)")
    
    tracemalloc.start()
    gen_total, gen_current, gen_peak = process_with_generator_expression(n)
    tracemalloc.stop()
    
    print(f"   총합: {gen_total:,}")
    print(f"   현재 메모리: {gen_current / 1024 / 1024:.2f} MB")
    print(f"   최대 메모리: {gen_peak / 1024 / 1024:.2f} MB")
    print()
    
    # 3) 메모리 사용량 비교
    print("3) 메모리 사용량 비교:")
    memory_diff = list_peak - gen_peak
    print(f"   List Comprehension 최대 메모리: {list_peak / 1024 / 1024:.2f} MB")
    print(f"   Generator Expression 최대 메모리: {gen_peak / 1024 / 1024:.2f} MB")
    print(f"   메모리 차이: {memory_diff / 1024 / 1024:.2f} MB")
    if gen_peak > 0:
        ratio = list_peak / gen_peak
        print(f"   Generator Expression이 약 {ratio:.1f}배 더 적은 메모리 사용")
    print()

# 메인 실행 함수
def main():
    compare_memory_usage()


if __name__ == "__main__":
    main()
