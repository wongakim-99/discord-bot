# 일반 명령어 로직

def register_general_commands(client):
    @client.event
    async def on_message(message):
        if message.content == "김영웅 바보":
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