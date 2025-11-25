import { useState, useEffect } from 'react';
import { Search } from 'lucide-react';
import { District, SearchResult } from '../types';
import { searchBuses, getDistricts } from '../api';
import BusResults from './BusResults';

export default function SearchBuses() {
  const [districts, setDistricts] = useState<District[]>([]);
  const [fromDistrict, setFromDistrict] = useState('');
  const [toDistrict, setToDistrict] = useState('');
  const [maxPrice, setMaxPrice] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  useEffect(() => {
    loadDistricts();
  }, []);

  const loadDistricts = async () => {
    const data = await getDistricts();
    setDistricts(data.districts);
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!fromDistrict || !toDistrict) return;

    setLoading(true);
    setSearched(true);
    try {
      const data = await searchBuses(
        fromDistrict,
        toDistrict,
        maxPrice ? parseInt(maxPrice) : undefined
      );
      setResults(data.results);
    } catch (error) {
      console.error('Search failed:', error);
    }
    setLoading(false);
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Search Buses</h2>
        <form onSubmit={handleSearch} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                From District
              </label>
              <select
                value={fromDistrict}
                onChange={(e) => setFromDistrict(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              >
                <option value="">Select departure</option>
                {districts.map((d) => (
                  <option key={d.id} value={d.name}>
                    {d.name}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                To District
              </label>
              <select
                value={toDistrict}
                onChange={(e) => setToDistrict(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              >
                <option value="">Select destination</option>
                {districts.map((d) => (
                  <option key={d.id} value={d.name}>
                    {d.name}
                  </option>
                ))}
              </select>
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Maximum Price (optional)
            </label>
            <input
              type="number"
              value={maxPrice}
              onChange={(e) => setMaxPrice(e.target.value)}
              placeholder="Enter max price in Taka"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition-colors flex items-center justify-center gap-2 disabled:bg-gray-400"
          >
            <Search size={20} />
            {loading ? 'Searching...' : 'Search Buses'}
          </button>
        </form>
      </div>

      {searched && <BusResults results={results} loading={loading} />}
    </div>
  );
}
