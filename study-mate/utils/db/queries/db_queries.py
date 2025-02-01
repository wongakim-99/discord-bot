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


def get_absent_users(current_date):
    """
    현재 날짜에 출석하지 않은 사용자 조회
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
            SELECT u.id AS user_id, u.nickname
            FROM users u
            LEFT JOIN attendance a
            ON u.id = a.user_id AND DATE(a.entry_time) = %s
            WHERE a.id IS NULL
            """
            cursor.execute(sql, (current_date,))
            return cursor.fetchall()
    finally:
        connection.close()


def add_penalty(user_id, amount, reason):
    """
    벌금 기록 추가
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
            INSERT INTO penalties (user_id, amount, reason, status)
            VALUES (%s, %s, %s, 'nonpay')
            """
            cursor.execute(sql, (user_id, amount, reason))
        connection.commit()
    finally:
        connection.close()


def update_attendance_exit(user_id, exit_time, duration):
    """퇴장 시간 및 체류 시간 업데이트"""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
            UPDATE attendance
            SET exit_time = %s, duration = %s
            WHERE user_id = %s AND exit_time IS NULL
            """
            cursor.execute(sql, (exit_time, duration, user_id))
        connection.commit()
    finally:
        connection.close()
