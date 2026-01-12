"""
짝수 제곱 제너레이터 실습 프로그램

이 프로그램은 제너레이터를 활용하여 짝수의 제곱을 생성하고, 메모리 사용량과
처리 속도를 비교하는 기능을 제공합니다.

주요 기능:
- 제너레이터 함수로 짝수의 제곱 생성
- 0부터 1,000,000까지의 짝수 제곱 총합 계산
- 일반 리스트 방식과 제너레이터 방식의 메모리 사용량 및 처리 속도 비교

변경 내역:
- 2026-01-12 [김준서(C1098)]: 초기 버전 생성 (짝수 제곱 제너레이터 실습)
"""

import sys
import time


# 제너레이터 함수: 0 이상 n 미만의 정수 중 짝수만 제곱해서 하나씩 생성합니다.
# Args: n (int) - 생성할 정수의 상한값 (n 미만)
# Yields: int - 짝수의 제곱값을 하나씩 생성
def even_square_gen(n):
    for i in range(n):
        if i % 2 == 0:
            yield i ** 2


# 메모리 사용량과 처리 속도를 비교하고 결과를 출력하는 함수
def compare_performance():
    print("짝수 제곱 총합 계산: 리스트 vs 제너레이터 비교")
    print()
    
    n = 1000001
    
    # 1) 일반 리스트 방식
    print("1) 일반 리스트 방식:")
    start_time = time.time()
    even_squares_list = [i ** 2 for i in range(n) if i % 2 == 0]
    list_memory = sys.getsizeof(even_squares_list)
    list_total = sum(even_squares_list)
    list_time = time.time() - start_time
    print(f"   총합: {list_total:,}")
    print(f"   메모리: {list_memory:,} bytes ({list_memory / 1024 / 1024:.2f} MB)")
    print(f"   시간: {list_time:.4f} 초")
    print()
    
    # 2) 제너레이터 방식
    print("2) 제너레이터 방식:")
    start_time = time.time()
    gen = even_square_gen(n)
    gen_memory = sys.getsizeof(gen)
    gen_total = sum(gen)
    gen_time = time.time() - start_time
    print(f"   총합: {gen_total:,}")
    print(f"   메모리: {gen_memory:,} bytes ({gen_memory / 1024:.2f} KB)")
    print(f"   시간: {gen_time:.4f} 초")
    print()
    
    # 3) 비교 결과
    print("3) 비교 결과:")
    memory_diff = list_memory - gen_memory
    print(f"   메모리 차이: {memory_diff:,} bytes ({memory_diff / 1024 / 1024:.2f} MB)")
    print(f"   제너레이터가 약 {list_memory / gen_memory:.0f}배 더 적은 메모리 사용")
    if gen_time > 0:
        speed_ratio = list_time / gen_time
        if speed_ratio > 1:
            print(f"   제너레이터가 약 {speed_ratio:.2f}배 더 빠름")
        else:
            print(f"   리스트가 약 {1/speed_ratio:.2f}배 더 빠름")


if __name__ == "__main__":
    compare_performance()
