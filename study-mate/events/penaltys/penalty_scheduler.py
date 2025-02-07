import asyncio
from datetime import datetime
from events.penaltys.penalty_manager import apply_penalties

async def penalty_scheduler():
    """
    매일 토요일, 일요일 14:15에 벌금을 부과하는 스케줄러
    """
    has_applied_today = False  # 벌금이 오늘 이미 부과되었는지 확인하는 플래그

    while True:
        now = datetime.now()
        print(f"현재 시간: {now}, 요일: {now.weekday()}")

        # 현재 요일 확인 (토요일=5, 일요일=6)
        if now.weekday() in [4, 5]:  # 토요일, 일요일
            # 14:15에 벌금 부과
            if (now.hour == 14 and now.minute >= 15) or (14 < now.hour < 19) or (now.hour == 19 and now.minute <= 30):
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