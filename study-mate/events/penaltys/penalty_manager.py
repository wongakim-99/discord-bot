from datetime import datetime
from utils.db.queries.db_queries import get_absent_users, add_penalty

async def apply_penalties():
    print("김영웅, 허준 벌금기원, 지각하면 뒤지는거야")
    """
    매주 토요일, 일요일 오후 2시 15분에 출석하지 않은 사용자에게 벌금을 부과
    """
    now = datetime.now()

    # 토요일(5) 또는 일요일(6)인지 확인
    if now.weekday() in [5, 6]:
        penalty_time = now.replace(hour=00, minute=00, second=0, microsecond=0)
        
        if now >= penalty_time:
            current_date = now.strftime("%Y-%m-%d")

            # 출석하지 않은 사용자 조회
            print(f"📅 현재 날짜: {current_date}")
            absent_users = get_absent_users(current_date)
            print(f"🛑 출석하지 않은 사용자: {absent_users}")

            # 벌금 부과
            for user in absent_users:
                user_id = user["user_id"]
                nickname = user["nickname"]
                amount = 2000  # 벌금 기본값
                reason = "출석하지 않음"

                add_penalty(user_id, amount, reason)
                print(f"✅ 벌금 부과: {nickname}님에게 {amount}원 벌금 부과")
