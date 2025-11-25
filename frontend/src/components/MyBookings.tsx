import { useState } from 'react';
import { Ticket, X, Calendar, MapPin, Bus } from 'lucide-react';
import { Booking } from '../types';
import { getMyBookings, cancelBooking } from '../api';

export default function MyBookings() {
  const [phone, setPhone] = useState('');
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setSearched(true);
    try {
      const data = await getMyBookings(phone);
      setBookings(data.bookings);
    } catch (error) {
      console.error('Failed to fetch bookings:', error);
    }
    setLoading(false);
  };

  const handleCancel = async (bookingRef: string) => {
    if (!confirm('Are you sure you want to cancel this booking?')) return;

    try {
      await cancelBooking(bookingRef, phone);
      const data = await getMyBookings(phone);
      setBookings(data.bookings);
    } catch (error) {
      console.error('Failed to cancel booking:', error);
      alert('Failed to cancel booking. Please try again.');
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">My Bookings</h2>
        <form onSubmit={handleSearch} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Phone Number
            </label>
            <input
              type="tel"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              placeholder="Enter your phone number"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400"
          >
            {loading ? 'Searching...' : 'View My Bookings'}
          </button>
        </form>
      </div>

      {searched && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">
            Your Bookings ({bookings.length})
          </h3>
          {bookings.length === 0 ? (
            <div className="text-center py-12">
              <Ticket size={48} className="mx-auto text-gray-400 mb-4" />
              <p className="text-gray-500">No bookings found</p>
            </div>
          ) : (
            <div className="space-y-4">
              {bookings.map((booking) => (
                <div
                  key={booking.id}
                  className={`border rounded-lg p-4 ${
                    booking.status === 'cancelled'
                      ? 'border-red-200 bg-red-50'
                      : 'border-gray-200'
                  }`}
                >
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <div className="flex items-center gap-2 mb-2">
                        <span className="text-xs font-semibold text-gray-500">
                          REF:
                        </span>
                        <span className="text-lg font-bold text-blue-600">
                          {booking.booking_reference}
                        </span>
                      </div>
                      <h4 className="text-lg font-semibold text-gray-800">
                        {booking.customer_name}
                      </h4>
                    </div>
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-semibold ${
                        booking.status === 'confirmed'
                          ? 'bg-green-100 text-green-800'
                          : 'bg-red-100 text-red-800'
                      }`}
                    >
                      {booking.status.toUpperCase()}
                    </span>
                  </div>

                  <div className="space-y-2 mb-4">
                    <div className="flex items-center gap-2 text-sm text-gray-600">
                      <Bus size={16} />
                      {booking.bus_provider}
                    </div>
                    <div className="flex items-center gap-2 text-sm text-gray-600">
                      <MapPin size={16} />
                      {booking.from_district} → {booking.to_district} ({booking.dropping_point})
                    </div>
                    <div className="flex items-center gap-2 text-sm text-gray-600">
                      <Calendar size={16} />
                      {new Date(booking.travel_date).toLocaleDateString()}
                    </div>
                    <div className="text-lg font-bold text-green-600">
                      ৳{booking.fare}
                    </div>
                  </div>

                  {booking.status === 'confirmed' && (
                    <button
                      onClick={() => handleCancel(booking.booking_reference)}
                      className="w-full bg-red-600 text-white py-2 rounded-lg hover:bg-red-700 transition-colors flex items-center justify-center gap-2"
                    >
                      <X size={16} />
                      Cancel Booking
                    </button>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
