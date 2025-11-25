export interface District {
  id: string;
  name: string;
  created_at: string;
}

export interface BusProvider {
  id: string;
  name: string;
  contact_info: string;
  address: string;
  privacy_policy: string;
  created_at: string;
}

export interface SearchResult {
  provider: string;
  provider_details: BusProvider;
  from_district: string;
  to_district: string;
  dropping_point: string;
  fare: number;
}

export interface Booking {
  id: string;
  booking_reference: string;
  customer_name: string;
  customer_phone: string;
  from_district: string;
  to_district: string;
  dropping_point: string;
  bus_provider: string;
  travel_date: string;
  fare: number;
  status: string;
  created_at: string;
}
