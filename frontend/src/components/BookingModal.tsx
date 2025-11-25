import { useState } from 'react';
import { X, CheckCircle } from 'lucide-react';
import { SearchResult } from '../types';
import { bookTicket } from '../api';

interface BookingModalProps {
  bus: SearchResult;
  onClose: () => void;
}

export default function BookingModal({ bus, onClose }: BookingModalProps) {
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [date, setDate] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [bookingRef, setBookingRef] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const result = await bookTicket({
        customer_name: name,
        customer_phone: phone,
        from_district: bus.from_district,
        to_district: bus.to_district,
        dropping_point: bus.dropping_point,
        bus_provider: bus.provider,
        travel_date: date,
        fare: bus.fare
      });

      setBookingRef(result.booking_reference);
      setSuccess(true);
    } catch (error) {
      console.error('Booking failed:', error);
      alert('Booking failed. Please try again.');
    }
    setLoading(false);
  };

  if (success) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-lg max-w-md w-full p-6">
          <div className="text-center">
            <CheckCircle size={64} className="mx-auto text-green-500 mb-4" />
            <h3 className="text-2xl font-bold text-gray-800 mb-2">Booking Confirmed!</h3>
            <div className="bg-gray-50 rounded-lg p-4 mb-4">
              <p className="text-sm text-gray-600 mb-2">Your Booking Reference</p>
              <p className="text-3xl font-bold text-blue-600 tracking-wider">{bookingRef}</p>
            </div>
            <p className="text-gray-600 mb-6">
              Please save this reference number for future use. You can use it to view or cancel your booking.
            </p>
            <button
              onClick={onClose}
              className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-md w-full p-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-xl font-bold text-gray-800">Book Your Ticket</h3>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
            <X size={24} />
          </button>
        </div>

        <div className="bg-blue-50 rounded-lg p-4 mb-6">
          <div className="flex justify-between mb-2">
            <span className="text-sm text-gray-600">Provider:</span>
            <span className="font-semibold">{bus.provider}</span>
          </div>
          <div className="flex justify-between mb-2">
            <span className="text-sm text-gray-600">Route:</span>
            <span className="font-semibold">{bus.from_district} → {bus.to_district}</span>
          </div>
          <div className="flex justify-between mb-2">
            <span className="text-sm text-gray-600">Dropping Point:</span>
            <span className="font-semibold">{bus.dropping_point}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-sm text-gray-600">Fare:</span>
            <span className="font-bold text-green-600">৳{bus.fare}</span>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Full Name
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Phone Number
            </label>
            <input
              type="tel"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              placeholder="01XXXXXXXXX"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Travel Date
            </label>
            <input
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              min={new Date().toISOString().split('T')[0]}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400"
          >
            {loading ? 'Processing...' : 'Confirm Booking'}
          </button>
        </form>
      </div>
    </div>
  );
}
