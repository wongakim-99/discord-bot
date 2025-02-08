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


def add_penalty(user_id, amount, penalty_type, stack_count, detail_data):
    """
    벌금 기록 추가
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
            INSERT INTO penalties (user_id, amount, penalty_type, status, stack_count)
            VALUES (%s, %s, %s, 'nonpay', %s)
            """
            print(f"✅ 벌금 추가 준비: user_id={user_id}, amount={amount}, penalty_type={penalty_type}, stack={stack_count}")
            cursor.execute(sql, (user_id, amount, penalty_type, stack_count))
            penalty_id = cursor.lastrowid  # penalties 의 ID 가져오기

            # 세부 테이블에 데이터 추가
            if penalty_type == '지각':
                detail_sql = """
                            INSERT INTO late_reasons (penalty_id, nickname, submitted_reason)
                            VALUES (%s, %s, %s)
                            """
                cursor.execute(detail_sql, (penalty_id, detail_data['nickname'], detail_data['reason']))

            elif penalty_type == '무단결석':
                detail_sql = """
                            INSERT INTO absent_details (penalty_id, nickname, absence_date)
                            VALUES (%s, %s, %s)
                            """
                cursor.execute(detail_sql, (penalty_id, detail_data['nickname'], detail_data['absence_date']))

            elif penalty_type == '출튀':
                detail_sql = """
                            INSERT INTO escape_details (penalty_id, nickname, escape_reason)
                            VALUES (%s, %s, %s)
                            """
                cursor.execute(detail_sql, (penalty_id, detail_data['nickname'], detail_data['reason']))

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


def get_last_penalty_stack(user_id):
    """
    사용자의 최근 벌금 스택 값을 가져옵니다. 없으면 0을 반환.
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
            SELECT stack_count
            FROM penalties
            WHERE user_id = %s
            ORDER BY date_issued DESC
            LIMIT 1
            """
            cursor.execute(sql, (user_id,))
            result = cursor.fetchone()
            return result["stack_count"] if result else 0
    finally:
        connection.close()


def get_user_id_by_discord_id(discord_id):
    """
    디스코드 사용자 ID로 users 테이블의 내부 ID 조회
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT id FROM users WHERE discord_id = %s"
            cursor.execute(sql, (discord_id,))
            result = cursor.fetchone()
            if result:
                return result['id']  # 내부 ID 반환
            else:
                return None  # 디스코드 ID가 없으면 None 반환
    finally:
        connection.close()


def has_penalty_today(user_id, date):
    """
    특정 사용자에 대해 오늘 벌금이 이미 부과되었는지 확인
    """
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
            SELECT COUNT(*) AS penalty_count FROM penalties
            WHERE user_id = %s AND DATE(date_issued) = %s
            """
            cursor.execute(sql, (user_id, date))
            result = cursor.fetchone()
            if result and result['penalty_count'] > 0:
                return True  # 벌금이 이미 부과된 경우
            return False  # 벌금이 부과되지 않은 경우
    finally:
        connection.close()
