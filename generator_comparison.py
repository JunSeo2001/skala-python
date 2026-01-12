"""
================================================================================
제너레이터 기반 반복 구조 비교 프로그램
================================================================================

이 프로그램은 100만 개의 숫자 리스트를 처리할 때 일반 리스트 방식과 제너레이터 방식의
메모리 사용 차이를 비교하는 기능을 제공합니다.

주요 기능:
- 일반 리스트 방식으로 0부터 999,999까지의 정수 총합 계산
- 제너레이터 함수로 동일한 결과 구현
- 두 방법의 메모리 사용량 비교 (sys.getsizeof() 사용)

변경 내역:
- 2026-01-12 [김준서(C1098)]: 초기 버전 생성 (리스트 vs 제너레이터 메모리 비교 기능)
================================================================================
"""

import sys


# 일반 리스트 방식: 0부터 n-1까지의 정수를 담는 리스트를 생성하고 총합을 반환합니다.
# Args: n (int) - 생성할 정수의 개수 (기본값: 1000000)
# Returns: int - 리스트의 모든 정수 합계
def sum_with_list(n=1000000):
    # 0부터 n-1까지의 정수 리스트 생성
    numbers = list(range(n))
    # 리스트의 모든 요소 합계 계산
    total = sum(numbers)
    return total


# 제너레이터 방식: 0부터 n-1까지의 정수를 생성하는 제너레이터 함수
# Args: n (int) - 생성할 정수의 개수 (기본값: 1000000)
# Yields: int - 0부터 n-1까지의 정수를 하나씩 생성
def number_generator(n=1000000):
    for i in range(n):
        yield i


# 제너레이터를 사용하여 총합을 계산합니다.
# Args: n (int) - 생성할 정수의 개수 (기본값: 1000000)
# Returns: int - 제너레이터로 생성된 모든 정수 합계
def sum_with_generator(n=1000000):
    # 제너레이터 함수 호출
    gen = number_generator(n)
    # 제너레이터로 생성된 모든 값의 합계 계산
    total = sum(gen)
    return total


# 메모리 사용량을 비교하고 결과를 출력하는 함수
def compare_memory_usage():
    print("=" * 80)
    print("리스트 vs 제너레이터 메모리 사용량 비교")
    print("=" * 80)
    print()
    
    n = 1000000
    
    # 1) 일반 리스트 방식
    print("1) 일반 리스트 방식:")
    numbers_list = list(range(n))
    list_memory = sys.getsizeof(numbers_list)
    list_total = sum(numbers_list)
    print(f"   총합: {list_total:,}")
    print(f"   메모리 사용량: {list_memory:,} bytes ({list_memory / 1024 / 1024:.2f} MB)")
    print()
    
    # 2) 제너레이터 방식
    print("2) 제너레이터 방식:")
    gen = number_generator(n)
    gen_memory = sys.getsizeof(gen)
    gen_total = sum_with_generator(n)
    print(f"   총합: {gen_total:,}")
    print(f"   제너레이터 객체 메모리 사용량: {gen_memory:,} bytes ({gen_memory / 1024:.2f} KB)")
    print()
    
    # 3) 메모리 차이 비교
    print("3) 메모리 사용량 비교:")
    memory_diff = list_memory - gen_memory
    print(f"   리스트 메모리: {list_memory:,} bytes")
    print(f"   제너레이터 메모리: {gen_memory:,} bytes")
    print(f"   차이: {memory_diff:,} bytes ({memory_diff / 1024 / 1024:.2f} MB)")
    print(f"   제너레이터가 {list_memory / gen_memory:.0f}배 더 적은 메모리 사용")
    print()


if __name__ == "__main__":
    compare_memory_usage()
