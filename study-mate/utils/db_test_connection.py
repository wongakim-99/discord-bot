import sys
import os

# 현재 파일의 상위 디렉토리를 모듈 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# db_connection에서 get_connection 가져오기
from utils.db_connection import get_connection


def test_connection():
    """데이터베이스 연결 테스트"""
    try:
        connection = get_connection()
        print("👍 데이터베이스 연결 성공!")
        with connection.cursor() as cursor:
            # 데이터베이스 버전 확인 쿼리 실행
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"Database Version: {version['VERSION()']}")
    except Exception as e:
        print("😡 데이터베이스 연결 실패:", e)
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()
            print("✅ 데이터베이스 연결 닫힘.")