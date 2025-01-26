import discord, asyncio
from dotenv import load_dotenv
import os
from datetime import datetime

# .env 파일 로드
load_dotenv()

# 환경 변수 가져오기
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TARGET_TEXT_CHANNEL_ID = int(os.getenv("TARGET_TEXT_CHANNEL_ID"))

# Gateway Intents 설정
intents = discord.Intents.default()
intents.messages = True  # 메시지 관련 이벤트를 처리하려면 활성화
intents.message_content = True  # 메시지 내용 접근 권한 활성화
intents.voice_states = True  # 음성 상태 변경 이벤트 활성화

client = discord.Client(intents=intents)

# 음성채널 입장 시간을 저장할 딕셔너리
voice_channel_entry_times = {}

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

# 사용자가 음성채널 입장시
@client.event
async def on_voice_state_update(member, before, after):
    # 현재 멤버가 속한 서버(Guild) 가져오기
    guild = member.guild

    # 특정 텍스트 채널 객체 가져오기
    text_channel = client.get_channel(TARGET_TEXT_CHANNEL_ID)

    if text_channel is None:  # 메시지를 보낼 수 있는 채널이 없는 경우
        print(f"{guild.name} 서버에 메시지를 보낼 수 있는 텍스트 채널이 없습니다.")
        return

    # 사용자가 음성 채널에 들어갔을 때
    if before.channel is None and after.channel is not None:
        # 음성 채널 이름 가져오기
        channel_name = after.channel.name
        # 현재 시간 기록
        entry_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        voice_channel_entry_times[member.id] = {"channel": channel_name, "time": entry_time}

        print(f"{member.name}님이 '{channel_name}' 채널에 {entry_time}에 입장했습니다.")
        await text_channel.send(f"{member.name}님이 '{channel_name}' 채널에 {entry_time}에 입장했습니다.")

    # 사용자가 음성 채널에서 나갔을 때
    elif before.channel is not None and after.channel is None:
        if member.id in voice_channel_entry_times:
            entry_info = voice_channel_entry_times.pop(member.id)
            print(f"{member.name}님이 '{entry_info['channel']}' 채널에서 나갔습니다. (입장 시간: {entry_info['time']})")
            
            # 텍스트 채널에 메시지 전송
            await text_channel.send(f"{member.name}님이 '{entry_info['channel']}' 채널에서 나갔습니다. (입장 시간: {entry_info['time']})")

# 봇 실행
client.run(DISCORD_TOKEN)
