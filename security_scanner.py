"""
AST 기반 자동 보안 검사기

이 프로그램은 AST(추상 구문 트리)를 활용하여 Python 코드 내의 위험한 함수 호출을
자동으로 탐지하고 리포트를 생성하는 기능을 제공합니다.

주요 기능:
- ast.NodeVisitor를 상속받아 모든 함수 호출(Call) 노드 탐색
- 위험 함수(eval, exec, pickle.load, os.system 등) 감지
- 파일명과 줄 번호를 포함한 상세 리포트 생성

변경 내역:
- 2026-01-12 [김준서(C1098)]: 초기 버전 생성 (AST 기반 보안 검사기)
"""

import ast
import os
from typing import List, Dict, Tuple


# 위험한 함수 목록 정의
DANGEROUS_FUNCTIONS = [
    'eval',
    'exec',
    'compile',
    '__import__',
    'open',  # 파일 접근 관련
    'pickle.load',
    'pickle.loads',
    'os.system',
    'os.popen',
    'subprocess.call',
    'subprocess.Popen',
    'input',  # 사용자 입력 관련
]


# AST 노드 방문자 클래스: 함수 호출을 탐색하고 위험 함수를 감지합니다.
# ast.NodeVisitor를 상속받아 모든 Call 노드를 방문합니다.
class SecurityVisitor(ast.NodeVisitor):
    def __init__(self, filename: str):
        self.filename = filename
        self.violations: List[Dict[str, any]] = []
    
    # Call 노드를 방문할 때 호출되는 메서드
    def visit_Call(self, node: ast.Call):
        # 함수 이름 추출
        func_name = self._get_function_name(node.func)
        
        # 위험 함수 목록과 비교
        if func_name in DANGEROUS_FUNCTIONS:
            violation = {
                'filename': self.filename,
                'line': node.lineno,
                'column': node.col_offset,
                'function': func_name
            }
            self.violations.append(violation)
        
        # 자식 노드들도 계속 방문
        self.generic_visit(node)
    
    # 함수 이름을 추출하는 헬퍼 메서드
    # Args: node - AST 노드
    # Returns: str - 함수 이름
    def _get_function_name(self, node: ast.AST) -> str:
        if isinstance(node, ast.Name):
            # 일반 함수 호출: func()
            return node.id
        elif isinstance(node, ast.Attribute):
            # 메서드 호출: obj.method()
            attr_name = node.attr
            if isinstance(node.value, ast.Name):
                # 모듈.함수 형태: os.system
                return node.value.id + '.' + attr_name
            else:
                # 중첩된 속성 접근
                return self._get_function_name(node.value) + '.' + attr_name
        else:
            # 기타 경우는 빈 문자열 반환
            return ''


# 단일 파일을 분석하고 보안 위반을 찾는 함수
# Args: filepath (str) - 분석할 파일 경로
# Returns: List[Dict] - 발견된 보안 위반 목록
def scan_file(filepath: str) -> List[Dict[str, any]]:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # AST 파싱
        tree = ast.parse(source_code, filename=filepath)
        
        # 보안 검사기 생성 및 실행
        visitor = SecurityVisitor(filepath)
        visitor.visit(tree)
        
        return visitor.violations
    except SyntaxError as e:
        print(f"⚠️  구문 오류: {filepath} (줄 {e.lineno})")
        return []
    except Exception as e:
        print(f"❌ 오류 발생: {filepath} - {str(e)}")
        return []


# 디렉토리 내의 모든 Python 파일을 스캔하는 함수
# Args: directory (str) - 스캔할 디렉토리 경로
# Returns: List[Dict] - 모든 파일에서 발견된 보안 위반 목록
def scan_directory(directory: str) -> List[Dict[str, any]]:
    all_violations = []
    
    for root, dirs, files in os.walk(directory):
        # .git, __pycache__ 등 제외
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'venv', 'env']]
        
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                violations = scan_file(filepath)
                all_violations.extend(violations)
    
    return all_violations


# 보안 위반 리포트를 생성하고 출력하는 함수
# Args: violations (List[Dict]) - 발견된 보안 위반 목록
def generate_report(violations: List[Dict[str, any]]):

    print("보안 검사 리포트")
    print()
    
    if not violations:
        print("보안 위반이 발견되지 않았습니다.")
        print()
        return
    
    print(f"⚠️  총 {len(violations)}개의 보안 위반이 발견되었습니다.")
    print()
    
    # 파일별로 그룹화
    violations_by_file: Dict[str, List[Dict]] = {}
    for violation in violations:
        filename = violation['filename']
        if filename not in violations_by_file:
            violations_by_file[filename] = []
        violations_by_file[filename].append(violation)
    
    # 리포트 출력
    for filename, file_violations in violations_by_file.items():
        print(f"📁 파일: {filename}")
        print(f"   발견된 위반: {len(file_violations)}개")
        print()
        
        for violation in file_violations:
            print(f"   ⚠️  줄 {violation['line']}")
            print(f"      위험 함수: {violation['function']}")
            print()
    


# 메인 실행 함수
def main():
    # 스크립트 파일이 있는 디렉토리를 기준으로 스캔
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"스캔 대상 디렉토리: {script_dir}")
    print()
    
    violations = scan_directory(script_dir)
    generate_report(violations)


if __name__ == "__main__":
    main()
