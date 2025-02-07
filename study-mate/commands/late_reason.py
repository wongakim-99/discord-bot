from datetime import datetime
from utils.db.queries.db_queries import get_last_penalty_stack, add_penalty, get_user_id_by_discord_id
from config.config import LATE_REASON_CHANEL_ID, STUDY_DAYS, STUDY_START_HOUR, STUDY_START_MINUTE

def handle_late_reason(client):
    """
    특정 채널에서만 지각 사유를 처리.
    """

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return  # 봇이 보낸 메시지는 무시

        # 채널 검사
        if message.channel.id != LATE_REASON_CHANEL_ID:
            return  # 지정된 채널이 아니면 무시

        # 메시지 내용 검사
        if message.content.startswith("지각사유"):
            # 현재 시간 확인
            now = datetime.now()

            # 오늘이 스터디 요일인지 확인
            if now.weekday() not in STUDY_DAYS:
                await message.channel.send(f"❌ {message.author.mention}, 오늘은 스터디 날이 아닙니다.")
                return

            # 스터디 시작 시간 설정
            study_start_time = now.replace(
                hour=STUDY_START_HOUR, minute=STUDY_START_MINUTE, second=0, microsecond=0
            )

            # 스터디 시작 시간이 지난 경우 -> 지각 사유 제출 불가
            if now >= study_start_time:
                await message.channel.send(
                    f"❌ {message.author.mention}, 지각 사유 제출 마감 시간이 지났습니다. (마감: {STUDY_START_HOUR}:{STUDY_START_MINUTE:02d})"
                )
                return

            # 디스코드 ID로 users 테이블의 내부 ID 조회
            discord_id = message.author.id
            user_id = get_user_id_by_discord_id(discord_id)
            if not user_id:
                await message.channel.send(f"❌ {message.author.mention}, 등록되지 않은 사용자입니다.")
                return

            reason = message.content.replace("지각사유", "").strip()

            # 최근 벌금 스택 가져오기
            last_stack = get_last_penalty_stack(user_id)
            new_stack = last_stack + 1  # 스택 증가

            # 벌금은 고정값 500원
            amount = 500
            add_penalty(user_id, amount, reason, new_stack)

            # 결과 알림
            await message.channel.send(
                f"✅ {message.author.mention}, 지각 사유 제출 완료: '{reason}' (벌금: {amount}원, 스택: {new_stack})"
            )
