export interface District {
  id: string;
  name: string;
  created_at: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface BusProvider {
  id: number;
  name: string;
}

export interface ProviderDetails {
  id: number;
  name: string;
  contact_info: string;
  address: string;
  privacy_policy: string;
  website: string;
  coverage_districts: string[];
  routes: {
    [key: string]: {
      dropping_point: string;
      price: number;
    }[];
  };
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
