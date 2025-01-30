import pymysql
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수에서 DB 정보 가져오기
DB_HOST = os.getenv("DB_HOST")  # RDS 엔드포인트
DB_USER = os.getenv("DB_USER")  # 사용자 이름
DB_PASSWORD = os.getenv("DB_PASSWORD")  # 비밀번호
DB_NAME = os.getenv("DB_NAME")  # 데이터베이스 이름

def get_connection():
    """RDS 데이터베이스 연결"""
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
