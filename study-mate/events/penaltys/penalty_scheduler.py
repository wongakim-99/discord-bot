import asyncio
from datetime import datetime
from events.penaltys.penalty_manager import apply_penalties

async def penalty_scheduler():
    """
    매일 정해진 시간에 벌금을 부과하는 스케줄러
    """
    while True:
        now = datetime.now()
        print(f"📅 현재 시간: {now}")

        # 매주 토요일, 일요일 14:15에 벌금 부과
        await apply_penalties()

        # 5분 간격으로 반복
        await asyncio.sleep(3600)
