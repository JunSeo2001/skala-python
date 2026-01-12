"""
================================================================================
부서별 평균 급여 분석 프로그램
================================================================================

이 프로그램은 직원(Employee) 데이터를 활용하여 부서별 평균 급여를 계산하고 출력하는 기능을 제공합니다.

주요 기능:
- 부서별 평균 급여 계산 및 출력

변경 내역:
- 2026-01-12 [김준서(C1098)]: 초기 버전 생성 (부서별 평균 급여 계산 기능)
- 2026-01-12 [김준서(C1098)]: 함수 로직 간소화 및 최적화
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


# 모든 부서별 평균 급여를 계산하여 딕셔너리 형태로 반환합니다.
# Args: employee_list (list) - 직원 정보를 담은 딕셔너리 리스트
# Returns: dict - {부서명: 평균급여} 형태의 딕셔너리
def get_average_salary_by_department(employee_list):
    result = {}
    for dept in set(emp["department"] for emp in employee_list):
        salaries = [emp["salary"] for emp in employee_list if emp["department"] == dept]
        result[dept] = sum(salaries) / len(salaries)
    return result


# 모든 부서별 평균 급여를 출력하는 함수
def print_department_average_salaries():
    # 부서별 평균 급여 계산
    avg_salaries = get_average_salary_by_department(employees)
    
    # 각 부서별로 평균 급여 출력
    print("부서별 평균 급여:")
    for dept, avg_salary in avg_salaries.items():
        print(f"   {dept}: ${avg_salary:,.0f}")
    print()
    
if __name__ == "__main__":
    print_department_average_salaries()
