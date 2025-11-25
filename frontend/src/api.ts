const API_URL = 'http://localhost:8000';

export const searchBuses = async (fromDistrict: string, toDistrict: string, maxPrice?: number) => {
  const response = await fetch(`${API_URL}/search-buses`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from_district: fromDistrict,
      to_district: toDistrict,
      max_price: maxPrice
    })
  });
  return response.json();
};

export const bookTicket = async (bookingData: {
  customer_name: string;
  customer_phone: string;
  from_district: string;
  to_district: string;
  dropping_point: string;
  bus_provider: string;
  travel_date: string;
  fare: number;
}) => {
  const response = await fetch(`${API_URL}/book-ticket`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(bookingData)
  });
  return response.json();
};

export const getMyBookings = async (phone: string) => {
  const response = await fetch(`${API_URL}/my-bookings/${phone}`);
  return response.json();
};

export const cancelBooking = async (bookingReference: string, phone: string) => {
  const response = await fetch(`${API_URL}/cancel-booking`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      booking_reference: bookingReference,
      customer_phone: phone
    })
  });
  return response.json();
};

export const getDistricts = async () => {
  const response = await fetch(`${API_URL}/districts`);
  return response.json();
};

export const sendChatMessage = async (message: string) => {
  const response = await fetch(`${API_URL}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  });
  return response.json();
};

export const getBusProviders = async () => {
  const response = await fetch(`${API_URL}/bus-providers`);
  return response.json();
};

export const getProviderDetails = async (providerName: string) => {
  const response = await fetch(`${API_URL}/bus-providers/${encodeURIComponent(providerName)}`);
  return response.json();
};

export const getProvidersByDistrict = async (districtName: string) => {
  const response = await fetch(`${API_URL}/bus-providers/district/${encodeURIComponent(districtName)}`);
  return response.json();
};

