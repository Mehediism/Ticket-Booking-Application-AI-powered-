import { useState } from 'react';
import { Bus, MapPin } from 'lucide-react';
import { SearchResult } from '../types';
import BookingModal from './BookingModal';

interface BusResultsProps {
  results: SearchResult[];
  loading: boolean;
}

export default function BusResults({ results, loading }: BusResultsProps) {
  const [selectedBus, setSelectedBus] = useState<SearchResult | null>(null);

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-12 text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p className="mt-4 text-gray-600">Searching for buses...</p>
      </div>
    );
  }

  if (results.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-md p-12 text-center">
        <Bus size={48} className="mx-auto text-gray-400 mb-4" />
        <h3 className="text-xl font-semibold text-gray-700 mb-2">No buses found</h3>
        <p className="text-gray-500">Try adjusting your search criteria</p>
      </div>
    );
  }

  return (
    <>
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4">
          Available Buses ({results.length})
        </h3>
        <div className="space-y-4">
          {results.map((result, index) => (
            <div
              key={index}
              className="border border-gray-200 rounded-lg p-4 hover:border-blue-400 transition-all hover:shadow-md"
            >
              <div className="flex justify-between items-start mb-3">
                <div>
                  <h4 className="text-lg font-bold text-gray-800 flex items-center gap-2">
                    <Bus size={20} className="text-blue-600" />
                    {result.provider}
                  </h4>
                  <p className="text-sm text-gray-600 mt-1">
                    {result.from_district} → {result.to_district}
                  </p>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-green-600">
                    ৳{result.fare}
                  </div>
                  <p className="text-xs text-gray-500">per seat</p>
                </div>
              </div>
              <div className="flex items-center gap-2 text-sm text-gray-600 mb-3">
                <MapPin size={16} />
                Dropping Point: {result.dropping_point}
              </div>
              <button
                onClick={() => setSelectedBus(result)}
                className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Book Now
              </button>
            </div>
          ))}
        </div>
      </div>

      {selectedBus && (
        <BookingModal
          bus={selectedBus}
          onClose={() => setSelectedBus(null)}
        />
      )}
    </>
  );
}
