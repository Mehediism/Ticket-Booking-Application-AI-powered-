from models.booking import Booking

class BookingController:
    @staticmethod
    def create_booking(customer_name, customer_phone, from_district, to_district,
                      dropping_point, bus_provider, travel_date, fare):
        result = Booking.create(
            customer_name, customer_phone, from_district, to_district,
            dropping_point, bus_provider, travel_date, fare
        )

        booking = Booking.get_by_reference_and_phone(
            result['booking_reference'], customer_phone
        )

        return {
            "success": True,
            "booking_reference": result['booking_reference'],
            "booking": booking
        }

    @staticmethod
    def get_bookings_by_phone(phone):
        return Booking.get_by_phone(phone)

    @staticmethod
    def cancel_booking(booking_reference, customer_phone):
        booking = Booking.get_by_reference_and_phone(booking_reference, customer_phone)

        if not booking:
            raise ValueError("Booking not found or phone number doesn't match")

        if booking['status'] == 'cancelled':
            raise ValueError("Booking already cancelled")

        success = Booking.cancel(booking_reference, customer_phone)

        return {
            "success": success,
            "message": "Booking cancelled successfully" if success else "Failed to cancel"
        }
