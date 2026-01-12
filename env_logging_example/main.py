"""
환경 변수 및 로깅 설정 실습 프로그램

이 프로그램은 .env 파일을 사용하여 환경 변수를 관리하고, python-dotenv를 이용해
환경 변수를 로딩한 후 logging 모듈을 통해 로그를 설정하는 기능을 제공합니다.

주요 기능:
- .env 파일에서 환경 변수 로딩 (LOG_LEVEL, APP_NAME)
- logging 모듈을 통한 로그 설정 (콘솔 + 파일 출력)
- 다양한 로그 레벨 메시지 출력 (INFO, DEBUG, ERROR)

변경 내역:
- 2026-01-12 [김준서(C1098)]: 초기 버전 생성 (환경 변수 및 로깅 설정 실습)
"""

import os
import logging
from dotenv import load_dotenv


# 로깅 설정 함수: 로그 레벨과 포맷을 설정하고 콘솔 및 파일 핸들러를 추가합니다.
# Args: level_name (str) - 로그 레벨 문자열 (예: "DEBUG", "INFO")
# Returns: None
def setup_logging(level_name: str) -> None:
    # 문자열 레벨("DEBUG") -> logging.DEBUG 변환 (없으면 INFO로 fallback)
    level = getattr(logging, level_name.upper(), logging.INFO)
    
    # 루트 로거 가져오기 및 레벨 설정
    logger = logging.getLogger()
    logger.setLevel(level)
    
    # 중복 핸들러 방지 (재실행 시 핸들러가 중복 추가되는 것을 방지)
    if logger.handlers:
        logger.handlers.clear()
    
    # 로그 포맷 설정: 시간 | 로그레벨 | 메시지
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    
    # 콘솔 핸들러 생성 및 설정
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(fmt)
    
    # 파일 핸들러 생성 및 설정 (app.log 파일에 저장)
    file_handler = logging.FileHandler("app.log", encoding="utf-8")
    file_handler.setLevel(level)
    file_handler.setFormatter(fmt)
    
    # 핸들러를 로거에 추가
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


# 메인 실행 함수: 환경 변수 로딩, 로깅 설정, 로그 메시지 출력을 수행합니다.
def main():
    # .env 파일에서 환경 변수 로딩
    load_dotenv()
    
    # 환경 변수에서 LOG_LEVEL과 APP_NAME 읽기 (기본값: INFO, MyApp)
    log_level = os.getenv("LOG_LEVEL", "INFO")
    app_name = os.getenv("APP_NAME", "MyApp")
    
    # 로깅 설정
    setup_logging(log_level)
    
    # INFO 레벨 메시지 출력
    logging.info("앱 실행 시작")
    
    # DEBUG 레벨 메시지 출력
    logging.debug("환경 변수 로딩 완료")
    
    # ERROR 레벨 메시지 출력 예시: ZeroDivisionError 예외 발생
    try:
        _ = 1 / 0
    except ZeroDivisionError:
        logging.exception("예외 발생 예시")
    
    # APP_NAME 출력
    logging.info(f"APP_NAME={app_name}")


if __name__ == "__main__":
    main()
