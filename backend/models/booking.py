from config.database import get_db_connection
import random
import string

class Booking:
    @staticmethod
    def generate_reference():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    @staticmethod
    def create(customer_name, customer_phone, from_district, to_district,
               dropping_point, bus_provider, travel_date, fare):
        booking_ref = Booking.generate_reference()
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO bookings
                (booking_reference, customer_name, customer_phone, from_district,
                 to_district, dropping_point, bus_provider, travel_date, fare, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'confirmed')
            """, (booking_ref, customer_name, customer_phone, from_district,
                  to_district, dropping_point, bus_provider, travel_date, fare))
            conn.commit()
            booking_id = cursor.lastrowid
            cursor.close()
            return {"id": booking_id, "booking_reference": booking_ref}
        finally:
            conn.close()

    @staticmethod
    def get_by_phone(phone):
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM bookings WHERE customer_phone = %s ORDER BY created_at DESC",
                (phone,)
            )
            results = cursor.fetchall()
            cursor.close()
            return results
        finally:
            conn.close()

    @staticmethod
    def get_by_reference_and_phone(booking_reference, phone):
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM bookings WHERE booking_reference = %s AND customer_phone = %s",
                (booking_reference, phone)
            )
            result = cursor.fetchone()
            cursor.close()
            return result
        finally:
            conn.close()

    @staticmethod
    def cancel(booking_reference, phone):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE bookings SET status = 'cancelled' WHERE booking_reference = %s AND customer_phone = %s",
                (booking_reference, phone)
            )
            conn.commit()
            affected = cursor.rowcount
            cursor.close()
            return affected > 0
        finally:
            conn.close()
