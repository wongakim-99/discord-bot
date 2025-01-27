import discord, asyncio
from config.config import DISCORD_TOKEN, TARGET_TEXT_CHANNEL_ID
from events.attendance_check import register_attendance_events
from commands.general import register_general_commands

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
    await client.change_presence(
        status=discord.Status.online, 
        activity=discord.Game("영웅이와 야스")
    )

# 이벤트 및 명령어 등록
register_attendance_events(client, TARGET_TEXT_CHANNEL_ID)
register_general_commands(client)

# 봇 실행
if __name__ == "__main__":
    client.run(DISCORD_TOKEN)
