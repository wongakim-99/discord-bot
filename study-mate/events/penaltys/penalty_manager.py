from datetime import datetime
from utils.db.queries.db_queries import get_absent_users, add_penalty, get_last_penalty_stack, has_penalty_today
from config.config import STUDY_DAYS, STUDY_START_HOUR, STUDY_START_MINUTE, PENALTY_END_HOUR, PENALTY_END_MINUTE

async def apply_penalties():
    print("김영웅, 허준 벌금기원, 지각하면 뒤지는거야")
    """
    매주 토요일, 일요일 오후 2시 15분에 출석하지 않은 사용자에게 벌금을 부과
    """
    now = datetime.now()

    # 토요일(5) 또는 일요일(6)인지 확인
    if now.weekday() in STUDY_DAYS:
        penalty_time = now.replace(hour=STUDY_START_HOUR, minute=STUDY_START_MINUTE, second=0, microsecond=0)
        penalty_end_time = now.replace(hour=PENALTY_END_HOUR, minute=PENALTY_END_MINUTE, second=0, microsecond=0)

        print(f"벌금 부과 시작 시간: {penalty_time}")
        print(f"벌금 부과 종료 시간: {penalty_end_time}")

        if penalty_time <= now <= penalty_end_time:
            current_date = now.strftime("%Y-%m-%d")

            # 출석하지 않은 사용자 조회
            print(f"📅 현재 날짜: {current_date}")
            absent_users = get_absent_users(current_date)
            print(f"🛑 출석하지 않은 사용자: {absent_users}")

            # 벌금 부과
            for user in absent_users:
                user_id = user["user_id"]
                nickname = user["nickname"]
                
                # 기존 스택 값 조회
                last_stack = get_last_penalty_stack(user_id)
                new_stack = last_stack + 1

                # 벌금 계산 로직(기존 벌금이 있으면 2배, 없으면 기본값 2000원 부과)
                amount = 2000 * (2 ** (new_stack - 1))

                detail_data = {
                    "nickname" : nickname,
                    "absence_date" : current_date,
                }

                add_penalty(user_id, amount, "무단결석", new_stack, detail_data)
                print(f"✅ {nickname} 벌금 {amount} ㅅㄱ")
        else:
            print("⏩ 벌금 부과 시간 범위가 아님")
    else:
        print("⏩ 오늘은 스터디 요일이 아님")