# config.py 에서는 .env 파일의 내용을 로드하고, 환경 변수를 관리

import os 
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수 가져오기
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TARGET_TEXT_CHANNEL_ID = int(os.getenv("TARGET_TEXT_CHANNEL_ID"))

# 지각사유 채팅채널
LATE_REASON_CHANEL_ID = int(os.getenv("LATE_REASON_CHANEL_ID"))

# 스터디 날짜 설정 (요일 : 월요일 = 0, 화요일 = 1, 수요일 = 2, ... 토요일 =5, 일요일 = 6)
STUDY_DAYS = [5, 6]  # 토요일(5), 일요일(6)

# 스터디 시작 시간 설정 (24시간 형식)
STUDY_START_HOUR = 00
STUDY_START_MINUTE = 40

# 벌금 부과 가능 시간 범위 (스터디 시작 후 특정 시간까지 허용)
PENALTY_END_HOUR = 23  # 오후 7시
PENALTY_END_MINUTE = 59  # 19:30분까지 가능