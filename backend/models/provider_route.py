from config.database import get_db_connection

class ProviderRoute:
    @staticmethod
    def create(provider_id, district_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO provider_routes (provider_id, district_id) VALUES (%s, %s)",
                (provider_id, district_id)
            )
            conn.commit()
            route_id = cursor.lastrowid
            cursor.close()
            return route_id
        finally:
            conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT pr.*, bp.name as provider_name, d.name as district_name
                FROM provider_routes pr
                JOIN bus_providers bp ON pr.provider_id = bp.id
                JOIN districts d ON pr.district_id = d.id
            """)
            results = cursor.fetchall()
            cursor.close()
            return results
        finally:
            conn.close()
