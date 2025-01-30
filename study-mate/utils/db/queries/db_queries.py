from utils.db.db_connection import get_connection

def get_user_id(discord_id):
    """디스코드 ID로 user_id 조회"""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT id FROM users WHERE discord_id = %s"
            cursor.execute(sql, (discord_id,))
            result = cursor.fetchone()
            return result["id"] if result else None
    finally:
        connection.close()


def add_user(discord_id, nickname):
    """새로운 유저 추가"""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO users (discord_id, nickname) VALUES (%s, %s) ON DUPLICATE KEY UPDATE nickname = VALUES(nickname)"
            cursor.execute(sql, (discord_id, nickname))
        connection.commit()
    finally:
        connection.close()


def save_attendance(user_id, channel_name, entry_time, status):
    """출석 기록 저장"""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO attendance (user_id, channel_name, entry_time, status) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (user_id, channel_name, entry_time, status))
        connection.commit()
    finally:
        connection.close()
