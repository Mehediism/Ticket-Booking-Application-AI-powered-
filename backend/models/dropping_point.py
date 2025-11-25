from config.database import get_db_connection

class DroppingPoint:
    @staticmethod
    def get_by_district_id(district_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT dp.*, d.name as district_name
                FROM dropping_points dp
                JOIN districts d ON dp.district_id = d.id
                WHERE dp.district_id = %s
            """, (district_id,))
            results = cursor.fetchall()
            cursor.close()
            return results
        finally:
            conn.close()

    @staticmethod
    def get_by_district_name(district_name):
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT dp.*, d.name as district_name
                FROM dropping_points dp
                JOIN districts d ON dp.district_id = d.id
                WHERE d.name = %s
            """, (district_name,))
            results = cursor.fetchall()
            cursor.close()
            return results
        finally:
            conn.close()

    @staticmethod
    def create(district_id, name, price):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO dropping_points (district_id, name, price) VALUES (%s, %s, %s)",
                (district_id, name, price)
            )
            conn.commit()
            point_id = cursor.lastrowid
            cursor.close()
            return point_id
        finally:
            conn.close()
