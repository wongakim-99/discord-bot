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
            WHERE NOT EXISTS (
                SELECT 1
                FROM attendance a
                WHERE u.id = a.user_id AND DATE(a.entry_time) = %s
            )
            """
            cursor.execute(sql, (current_date,))
            result = cursor.fetchall()
            print(f"🛠️ 디버깅: absent_users = {result}")  # 디버깅 로그 추가
            return result
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
            print(f"✅ 벌금 추가 준비: user_id={user_id}, amount={amount}, reason={reason}")
            cursor.execute(sql, (user_id, amount, reason))
        connection.commit()
        print(f"✅ 벌금 추가 완료: user_id={user_id}")
    except Exception as e:
        print(f"❌ 벌금 추가 실패: {e}")
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


def get_last_penalty_amount(user_id):
    """
    특정 사용자의 마지막 벌금 금액 조회
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
            SELECT amount
            FROM penalties
            WHERE user_id = %s
            ORDER BY id DESC  -- 가장 최근 벌금을 가져오기 위해 id 내림차순 정렬
            LIMIT 1
            """
            cursor.execute(sql, (user_id,))
            result = cursor.fetchone()

            # 벌금이 없으면 None 반환
            if result:
                print(f"🛠️ 디버깅: 마지막 벌금 금액 = {result['amount']}")
                return result["amount"]
            else:
                print(f"🛠️ 디버깅: 이전 벌금 없음")
                return 0  # 기존 벌금이 없으면 0 반환
    finally:
        connection.close()
