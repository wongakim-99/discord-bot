import asyncio
from datetime import datetime
from events.penaltys.penalty_manager import apply_penalties
from config.config import STUDY_DAYS, STUDY_START_HOUR, STUDY_START_MINUTE, PENALTY_END_HOUR, PENALTY_END_MINUTE

async def penalty_scheduler():
    """
    매일 토요일, 일요일 14:15에 벌금을 부과하는 스케줄러
    """
    has_applied_today = False  # 벌금이 오늘 이미 부과되었는지 확인하는 플래그

    while True:
        now = datetime.now()
        print(f"현재 시간: {now}, 요일: {now.weekday()}")

        # 현재 요일 확인 (토요일=5, 일요일=6)
        if now.weekday() in STUDY_DAYS:  # 지정된 스터디 요일 확인
            if (now.hour == STUDY_START_HOUR and now.minute >= STUDY_START_MINUTE) or \
                    (STUDY_START_HOUR < now.hour < PENALTY_END_HOUR) or \
                    (now.hour == PENALTY_END_HOUR and now.minute <= PENALTY_END_MINUTE):
                if not has_applied_today:
                    print("🚨 벌금 부과 시작!")
                    await apply_penalties()
                    has_applied_today = True  # 벌금 부과 완료 플래그 설정
            else:
                has_applied_today = False  # 시간이 지나면 플래그 초기화
        else:
            has_applied_today = False  # 평일에는 플래그 초기화

        # 1분 간격으로 확인
        await asyncio.sleep(25)