from config.database import get_db_connection

class BusDocument:
    @staticmethod
    def create(provider_name, content):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO bus_documents (provider_name, content) VALUES (%s, %s)",
                (provider_name, content)
            )
            conn.commit()
            doc_id = cursor.lastrowid
            cursor.close()
            return doc_id
        finally:
            conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM bus_documents")
            results = cursor.fetchall()
            cursor.close()
            return results
        finally:
            conn.close()

    @staticmethod
    def search(query, limit=3):
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM bus_documents WHERE content LIKE %s LIMIT %s",
                (f"%{query}%", limit)
            )
            results = cursor.fetchall()
            cursor.close()
            return results
        finally:
            conn.close()
