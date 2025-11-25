from config.database import get_db_connection

class District:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM districts ORDER BY name")
            results = cursor.fetchall()
            cursor.close()
            return results
        finally:
            conn.close()

    @staticmethod
    def get_by_name(name):
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM districts WHERE name = %s", (name,))
            result = cursor.fetchone()
            cursor.close()
            return result
        finally:
            conn.close()

    @staticmethod
    def create(name):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO districts (name) VALUES (%s)", (name,))
            conn.commit()
            district_id = cursor.lastrowid
            cursor.close()
            return district_id
        finally:
            conn.close()
