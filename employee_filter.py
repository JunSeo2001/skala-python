"""
================================================================================
직원 정보 필터링 및 분석 프로그램
================================================================================

이 프로그램은 직원(Employee) 데이터를 활용하여 다양한 조건으로 필터링하고 정렬하는 기능을 제공합니다.

주요 기능:
1. 부서와 급여 조건에 따른 직원 필터링
2. 나이 조건에 따른 직원 정보 추출
3. 급여 기준 정렬 및 상위 직원 조회
4. 부서별 평균 급여 계산 및 출력

작성일: 2026년 1월 12일
작성자: 김준서(C1098)
================================================================================
"""

# 직원 데이터 정의
employees = [
    {"name": "Alice", "department": "Engineering", "age": 30, "salary": 85000},
    {"name": "Bob", "department": "Marketing", "age": 25, "salary": 60000},
    {"name": "Charlie", "department": "Engineering", "age": 35, "salary": 95000},
    {"name": "David", "department": "HR", "age": 45, "salary": 70000},
    {"name": "Eve", "department": "Engineering", "age": 28, "salary": 78000},
]


# 부서가 "Engineering"이고 급여가 80000 이상인 직원들의 이름을 반환합니다.
# Args: employee_list (list) - 직원 정보를 담은 딕셔너리 리스트
# Returns: list - 조건을 만족하는 직원들의 이름 리스트
def filter_engineering_high_salary(employee_list):
    result = [
        emp["name"] 
        for emp in employee_list 
        if emp["department"] == "Engineering" and emp["salary"] >= 80000
    ]
    return result


# 30세 이상인 직원의 이름과 부서를 튜플 형태로 반환합니다.
# Args: employee_list (list) - 직원 정보를 담은 딕셔너리 리스트
#       min_age (int) - 최소 나이 기준 (기본값: 30)
# Returns: list - (이름, 부서) 튜플을 담은 리스트
def get_employees_over_age(employee_list, min_age=30):
    result = [
        (emp["name"], emp["department"]) 
        for emp in employee_list 
        if emp["age"] >= min_age
    ]
    return result


# 급여 기준으로 직원 리스트를 내림차순 정렬하고, 상위 N명의 이름과 급여를 반환합니다.
# Args: employee_list (list) - 직원 정보를 담은 딕셔너리 리스트
#       top_n (int) - 상위 몇 명을 반환할지 지정 (기본값: 3)
# Returns: list - (이름, 급여) 튜플을 담은 리스트 (급여 내림차순)
def get_top_salaries(employee_list, top_n=3):
    # 급여 기준으로 내림차순 정렬
    sorted_employees = sorted(
        employee_list, 
        key=lambda x: x["salary"], 
        reverse=True
    )
    
    # 상위 N명의 이름과 급여 추출
    result = [
        (emp["name"], emp["salary"]) 
        for emp in sorted_employees[:top_n]
    ]
    return result


# 모든 부서별 평균 급여를 계산하여 딕셔너리 형태로 반환합니다.
# Args: employee_list (list) - 직원 정보를 담은 딕셔너리 리스트
# Returns: dict - {부서명: 평균급여} 형태의 딕셔너리
def get_average_salary_by_department(employee_list):
    # 1단계: 부서별로 급여 합계와 인원 수를 저장할 딕셔너리 생성
    # 예: {"Engineering": {"total": 258000, "count": 3}, ...}
    department_stats = {}
    
    # 2단계: 각 직원을 순회하면서 부서별로 급여 합계와 인원 수를 누적
    for emp in employee_list:
        dept = emp["department"]  # 현재 직원의 부서명
        salary = emp["salary"]     # 현재 직원의 급여
        
        # 해당 부서가 처음 나오면 딕셔너리에 초기값 설정
        if dept not in department_stats:
            department_stats[dept] = {"total": 0, "count": 0}
        
        # 부서별 급여 합계에 현재 직원의 급여 추가
        department_stats[dept]["total"] += salary
        # 부서별 인원 수 1 증가
        department_stats[dept]["count"] += 1
    
    # 3단계: 각 부서의 평균 급여 계산 (합계 / 인원 수)
    result = {}
    for dept, stats in department_stats.items():
        avg_salary = stats["total"] / stats["count"]  # 평균 = 합계 / 인원 수
        result[dept] = avg_salary
    
    return result


# 메인 실행 함수: 모든 필터링 및 분석 기능을 실행하고 결과를 출력합니다.
def main():
    print("=" * 80)
    print("직원 정보 필터링 및 분석 결과")
    print("=" * 80)
    print()
    
    # 1) 부서가 "Engineering"이고 salary >= 80000인 직원들의 이름만 리스트로 출력
    print("1) 부서가 'Engineering'이고 급여가 80,000 이상인 직원들의 이름:")
    engineering_high_salary = filter_engineering_high_salary(employees)
    print(f"   결과: {engineering_high_salary}")
    print()
    
    # 2) 30세 이상인 직원의 이름과 부서를 튜플 (name, department) 형태로 리스트로 출력
    print("2) 30세 이상인 직원의 이름과 부서 (튜플 형태):")
    employees_over_30 = get_employees_over_age(employees, min_age=30)
    print(f"   결과: {employees_over_30}")
    print()
    
    # 3) 급여 기준으로 직원 리스트를 salary 내림차순으로 정렬하고, 상위 3명의 이름과 급여를 출력
    print("3) 급여 기준 내림차순 정렬, 상위 3명의 이름과 급여:")
    top_salaries = get_top_salaries(employees, top_n=3)
    print(f"   결과: {top_salaries}")
    print()
    
    print("=" * 80)


# 4) 모든 부서별 평균 급여를 출력하는 함수
def print_department_average_salaries():
    print("=" * 80)
    print("부서별 평균 급여 분석")
    print("=" * 80)
    print()
    
    # 부서별 평균 급여 계산
    avg_salaries = get_average_salary_by_department(employees)
    
    # 각 부서별로 평균 급여 출력
    print("부서별 평균 급여:")
    for dept, avg_salary in avg_salaries.items():
        print(f"   {dept}: ${avg_salary:,.0f}")
    print()
    
    print("=" * 80)


if __name__ == "__main__":
    main()
