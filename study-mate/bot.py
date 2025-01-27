import discord, asyncio
from config.config import DISCORD_TOKEN, TARGET_TEXT_CHANNEL_ID
from events.attendance_check import register_attendance_events

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

# 특정 메시지 입력시 봇의 응답
@client.event
async def on_message(message):
    if message.content == "김영웅 바보":  # 메시지 감지
        await message.channel.send(f"{message.author.mention}, 동의합니다 휴먼")
    elif message.content == "김영웅 천재":  
        await message.channel.send(f"{message.author.mention}, 그건..좀...아닙니다 휴먼")
    elif message.content == "너를 만든 개발자는 누구니?":
        await message.channel.send(f"{message.author.mention}, 키크고 잘생긴 김가원 입니다.")
    elif message.content == "허준에 대해 한줄 요약좀":
        await message.channel.send(f"{message.author.mention}, 이름만 들으면 약대 출신같겠지만, 현실은 기계공학과 랩실 노예입니다.")
    elif message.content == "김가원에 대해 한줄 요약좀":
        await message.channel.send(f"{message.author.mention}, He's alpha male.")
    elif message.content == "김영웅에 대해 한줄 요약좀":
        await message.channel.send(f"{message.author.mention}, 미친놈 같지만, 미친놈이 맞습니다.")

# 이벤트 및 명령어 등록
register_attendance_events(client, TARGET_TEXT_CHANNEL_ID)

# 봇 실행
if __name__ == "__main__":
    client.run(DISCORD_TOKEN)
