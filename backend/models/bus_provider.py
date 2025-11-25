from config.database import get_db_connection

class BusProvider:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM bus_providers ORDER BY name")
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
            cursor.execute("SELECT * FROM bus_providers WHERE name = %s", (name,))
            result = cursor.fetchone()
            cursor.close()
            return result
        finally:
            conn.close()

    @staticmethod
    def create(name, contact_info="", address="", privacy_policy=""):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO bus_providers (name, contact_info, address, privacy_policy) VALUES (%s, %s, %s, %s)",
                (name, contact_info, address, privacy_policy)
            )
            conn.commit()
            provider_id = cursor.lastrowid
            cursor.close()
            return provider_id
        finally:
            conn.close()

    @staticmethod
    def get_providers_serving_district(district_name):
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT DISTINCT bp.*
                FROM bus_providers bp
                JOIN provider_routes pr ON bp.id = pr.provider_id
                JOIN districts d ON pr.district_id = d.id
                WHERE d.name = %s
            """, (district_name,))
            results = cursor.fetchall()
            cursor.close()
            return results
        finally:
            conn.close()
