from datetime import datetime
from utils.db.queries.db_queries import get_absent_users, add_penalty, get_last_penalty_amount

async def apply_penalties():
    print("김영웅, 허준 벌금기원, 지각하면 뒤지는거야")
    """
    매주 토요일, 일요일 오후 2시 15분에 출석하지 않은 사용자에게 벌금을 부과
    """
    now = datetime.now()

    # 토요일(5) 또는 일요일(6)인지 확인
    if now.weekday() in [4, 5]:
        penalty_time = now.replace(hour=14, minute=15, second=0, microsecond=0)  # 현재 테스트용
        
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
                
                # 기존 벌금 조회
                last_penalty_amount = get_last_penalty_amount(user_id)

                # 벌금 계산 로직(기존 벌금이 있으면 2배, 없으면 기본값 2000원 부과)
                amount = last_penalty_amount * 2 if last_penalty_amount else 2000
                reason = "출석하지 않음"
                
                add_penalty(user_id, amount, reason)
                print(f"✅ {nickname} 벌금 {amount} ㅅㄱ")
