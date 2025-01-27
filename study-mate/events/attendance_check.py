from datetime import datetime

# 음성채널 입장 시간을 저장할 딕셔너리
voice_channel_entry_times = {}

def register_attendance_events(client, target_text_channel_id):
    @client.event
    async def on_voice_state_update(member, before, after):
        # 현재 멤버가 속한 서버(Guild) 가져오기
        guild = member.guild

        # 특정 텍스트 채널 객체 가져오기
        text_channel = client.get_channel(target_text_channel_id)

        if not text_channel:
            print(f"{guild.name} 서버에 메시지를 보낼 수 있는 텍스트 채널이 없습니다.")
            return

        # 음성 채널 입장 이벤트
        if before.channel is None and after.channel is not None:
            # 음성 채널 이름 가져오기
            channel_name = after.channel.name
            
            # 현재 시간 기록
            entry_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            voice_channel_entry_times[member.id] = {"channel": channel_name, "time": entry_time}
            
            print(f"{member.name}님이 '{channel_name}' 채널에 {entry_time}에 입장했습니다.")
            await text_channel.send(f"{member.name}님이 '{channel_name}' 채널에 {entry_time}에 입장했습니다.")

        # 음성 채널 퇴장 이벤트
        elif before.channel is not None and after.channel is None:
            if member.id in voice_channel_entry_times:
                entry_info = voice_channel_entry_times.pop(member.id)
                print(f"{member.name}님이 '{entry_info['channel']}' 채널에서 나갔습니다. (입장 시간: {entry_info['time']})")

                # 텍스트 채널에 메시지 전송
                await text_channel.send(f"{member.name}님이 '{entry_info['channel']}' 채널에서 나갔습니다. (입장 시간: {entry_info['time']})")