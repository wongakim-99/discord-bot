import discord, asyncio
from config.config import DISCORD_TOKEN, TARGET_TEXT_CHANNEL_ID
from events.attendances.attendance_check import register_attendance_events
from events.penaltys.penalty_scheduler import penalty_scheduler
from commands.general import register_general_commands

# from utils.db_test_connection import test_connection

# Gateway Intents 설정
intents = discord.Intents.default()
intents.messages = True  # 메시지 관련 이벤트를 처리하려면 활성화
intents.message_content = True  # 메시지 내용 접근 권한 활성화
intents.voice_states = True  # 음성 상태 변경 이벤트 활성화

client = discord.Client(intents=intents)

# 봇의 상태 메시지
@client.event
async def on_ready():  # 봇이 실행되면 한 번 실행됨
    print(f"Logged in as {client.user}")
    asyncio.create_task(penalty_scheduler())  # 스케줄러 실행
    await client.change_presence(
        status=discord.Status.online, 
        activity=discord.Game("개발 테스트")
    )
    # 데이터베이스 연결 테스트
    try:
        # test_connection()  # 데이터베이스 연결 테스트 실행 (활성화 시 주석 해제)
        print("✅ 데이터베이스 연결 테스트 성공")
    except Exception as e:
        print(f"❌ 데이터베이스 연결 테스트 실패: {e}")

# 봇 종료 처리
@client.event
async def on_disconnect():
    print("🔴 봇이 연결을 종료했습니다.")

# 이벤트 및 명령어 등록
register_attendance_events(client, TARGET_TEXT_CHANNEL_ID)
register_general_commands(client)

# 봇 실행
if __name__ == "__main__":
    print("🚀 봇 실행 준비 중")
    # test_connection()  # 데이터베이스 연결 테스트 실행 -> 데이터 베이스 정상 작동 ✅
    client.run(DISCORD_TOKEN) 