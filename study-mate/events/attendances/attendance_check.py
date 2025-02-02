from datetime import datetime
from utils.db.queries.db_queries import get_user_id, add_user, save_attendance, update_attendance_exit

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
            entry_time = datetime.now()
            
            # 사용자 DB 확인 및 추가
            user_id = get_user_id(str(member.id))
            if not user_id:
                add_user(str(member.id), member.name)
                user_id = get_user_id(str(member.id))
            
            # 지각 여부 판단
            late_time = entry_time.replace(hour=00, minute=00, second=0, microsecond=0)
            status = "late" if entry_time > late_time else "atten"

            # 출석 기록 DB 저장
            save_attendance(user_id, channel_name, entry_time, status)
            
            # 메모리에도 저장
            voice_channel_entry_times[member.id] = {"channel": channel_name, "time": entry_time}
            
            print(f"{member.name}님이 '{channel_name}' 채널에 {entry_time.strftime('%Y-%m-%d %H:%M:%S')}에 입장했습니다.")
            await text_channel.send(f"{member.name}님이 '{channel_name}' 채널에 {entry_time.strftime('%Y-%m-%d %H:%M:%S')}에 입장했습니다. (상태: {status})")

       # 음성 채널 퇴장 이벤트
        elif before.channel is not None and after.channel is None:
            if member.id in voice_channel_entry_times:
                entry_info = voice_channel_entry_times.pop(member.id)
                exit_time = datetime.now()
                user_id = get_user_id(str(member.id))

                if user_id:
                    # 체류 시간 계산 및 DB 업데이트
                    duration = (exit_time - entry_info["time"]).seconds
                    update_attendance_exit(user_id, exit_time, duration)
                
                print(f"{member.name}님이 '{entry_info['channel']}' 채널에서 나갔습니다. (입장 시간: {entry_info['time']})")
                await text_channel.send(f"{member.name}님이 '{entry_info['channel']}' 채널에서 나갔습니다. (입장 시간: {entry_info['time']})")