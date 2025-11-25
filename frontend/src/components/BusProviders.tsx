import { useState, useEffect } from 'react';
import { Building2, MapPin, Phone, Globe, X, Search, Filter } from 'lucide-react';
import { getBusProviders, getProviderDetails, getDistricts, getProvidersByDistrict } from '../api';
import { BusProvider, ProviderDetails, District } from '../types';

function BusProviders() {
    const [providers, setProviders] = useState<BusProvider[]>([]);
    const [districts, setDistricts] = useState<District[]>([]);
    const [selectedProvider, setSelectedProvider] = useState<ProviderDetails | null>(null);
    const [loading, setLoading] = useState(false);
    const [detailsLoading, setDetailsLoading] = useState(false);
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedDistrict, setSelectedDistrict] = useState('');

    useEffect(() => {
        loadProviders();
        loadDistricts();
    }, []);

    const loadProviders = async () => {
        setLoading(true);
        try {
            const data = await getBusProviders();
            setProviders(data.providers || []);
        } catch (error) {
            console.error('Error loading providers:', error);
        } finally {
            setLoading(false);
        }
    };

    const loadDistricts = async () => {
        try {
            const data = await getDistricts();
            setDistricts(data.districts || []);
        } catch (error) {
            console.error('Error loading districts:', error);
        }
    };

    const handleProviderClick = async (providerName: string) => {
        setDetailsLoading(true);
        try {
            const details = await getProviderDetails(providerName);
            setSelectedProvider(details);
        } catch (error) {
            console.error('Error loading provider details:', error);
        } finally {
            setDetailsLoading(false);
        }
    };

    // Reload providers when district filter changes
    useEffect(() => {
        if (selectedDistrict) {
            loadProvidersByDistrict(selectedDistrict);
        } else {
            loadProviders();
        }
    }, [selectedDistrict]);

    const loadProvidersByDistrict = async (districtName: string) => {
        setLoading(true);
        try {
            const data = await getProvidersByDistrict(districtName);
            setProviders(data.providers || []);
        } catch (error) {
            console.error('Error loading providers by district:', error);
        } finally {
            setLoading(false);
        }
    };

    const filteredProviders = providers.filter(provider => {
        const matchesSearch = provider.name.toLowerCase().includes(searchQuery.toLowerCase());
        return matchesSearch;
    });

    return (
        <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-sm p-6">
                <div className="flex items-center gap-3 mb-6">
                    <Building2 className="text-blue-600" size={28} />
                    <div>
                        <h2 className="text-2xl font-bold text-gray-800">Bus Providers</h2>
                        <p className="text-sm text-gray-600">Browse all available bus service providers</p>
                    </div>
                </div>

                {/* Search and Filter */}
                <div className="flex gap-4 mb-6">
                    <div className="flex-1 relative">
                        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                        <input
                            type="text"
                            placeholder="Search providers..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                    </div>
                    <div className="relative">
                        <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                        <select
                            value={selectedDistrict}
                            onChange={(e) => setSelectedDistrict(e.target.value)}
                            className="pl-10 pr-8 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent appearance-none bg-white"
                        >
                            <option value="">All Districts</option>
                            {districts.map(district => (
                                <option key={district.id} value={district.name}>{district.name}</option>
                            ))}
                        </select>
                    </div>
                </div>

                {/* Provider Grid */}
                {loading ? (
                    <div className="text-center py-12">
                        <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-600 border-t-transparent"></div>
                        <p className="mt-2 text-gray-600">Loading providers...</p>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {filteredProviders.map(provider => (
                            <div
                                key={provider.id}
                                onClick={() => handleProviderClick(provider.name)}
                                className="bg-gradient-to-br from-blue-50 to-white border border-blue-100 rounded-lg p-6 cursor-pointer hover:shadow-lg hover:scale-105 transition-all duration-200"
                            >
                                <div className="flex items-start justify-between mb-3">
                                    <div className="bg-blue-600 text-white rounded-full p-3">
                                        <Building2 size={24} />
                                    </div>
                                </div>
                                <h3 className="text-xl font-bold text-gray-800 mb-2">{provider.name}</h3>
                                <button className="text-blue-600 hover:text-blue-700 font-medium text-sm flex items-center gap-1">
                                    View Details →
                                </button>
                            </div>
                        ))}
                    </div>
                )}

                {filteredProviders.length === 0 && !loading && (
                    <div className="text-center py-12 text-gray-500">
                        <Building2 size={48} className="mx-auto mb-3 opacity-30" />
                        <p>No providers found</p>
                    </div>
                )}
            </div>

            {/* Provider Details Modal */}
            {selectedProvider && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
                    <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
                        {detailsLoading ? (
                            <div className="p-12 text-center">
                                <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-600 border-t-transparent"></div>
                                <p className="mt-2 text-gray-600">Loading details...</p>
                            </div>
                        ) : (
                            <>
                                {/* Header */}
                                <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-6 flex items-start justify-between">
                                    <div className="flex items-center gap-4">
                                        <div className="bg-white bg-opacity-20 rounded-full p-4">
                                            <Building2 size={32} />
                                        </div>
                                        <div>
                                            <h2 className="text-3xl font-bold">{selectedProvider.name}</h2>
                                            <p className="text-blue-100 mt-1">Bus Service Provider</p>
                                        </div>
                                    </div>
                                    <button
                                        onClick={() => setSelectedProvider(null)}
                                        className="text-white hover:bg-white hover:bg-opacity-20 rounded-full p-2 transition"
                                    >
                                        <X size={24} />
                                    </button>
                                </div>

                                {/* Content */}
                                <div className="p-6 space-y-6">
                                    {/* Contact Information */}
                                    <div className="bg-gray-50 rounded-lg p-4">
                                        <h3 className="font-bold text-lg text-gray-800 mb-3 flex items-center gap-2">
                                            <Phone className="text-blue-600" size={20} />
                                            Contact Information
                                        </h3>
                                        <p className="text-gray-700 whitespace-pre-line">{selectedProvider.contact_info || 'Not available'}</p>
                                    </div>

                                    {/* Address */}
                                    {selectedProvider.address && (
                                        <div className="bg-gray-50 rounded-lg p-4">
                                            <h3 className="font-bold text-lg text-gray-800 mb-3 flex items-center gap-2">
                                                <MapPin className="text-blue-600" size={20} />
                                                Official Address
                                            </h3>
                                            <p className="text-gray-700">{selectedProvider.address}</p>
                                        </div>
                                    )}

                                    {/* Website */}
                                    {selectedProvider.website && (
                                        <div className="bg-gray-50 rounded-lg p-4">
                                            <h3 className="font-bold text-lg text-gray-800 mb-3 flex items-center gap-2">
                                                <Globe className="text-blue-600" size={20} />
                                                Website
                                            </h3>
                                            <a
                                                href={selectedProvider.website}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                className="text-blue-600 hover:text-blue-700 hover:underline break-all"
                                            >
                                                {selectedProvider.website}
                                            </a>
                                        </div>
                                    )}

                                    {/* Coverage Districts */}
                                    <div className="bg-gray-50 rounded-lg p-4">
                                        <h3 className="font-bold text-lg text-gray-800 mb-3">Coverage Districts</h3>
                                        <div className="flex flex-wrap gap-2">
                                            {selectedProvider.coverage_districts.map((district, index) => (
                                                <span
                                                    key={index}
                                                    className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm font-medium"
                                                >
                                                    {district}
                                                </span>
                                            ))}
                                        </div>
                                    </div>

                                    {/* Routes */}
                                    {Object.keys(selectedProvider.routes).length > 0 && (
                                        <div className="bg-gray-50 rounded-lg p-4">
                                            <h3 className="font-bold text-lg text-gray-800 mb-3">Available Routes</h3>
                                            <div className="space-y-3 max-h-60 overflow-y-auto">
                                                {Object.entries(selectedProvider.routes).map(([route, droppingPoints]) => (
                                                    <div key={route} className="bg-white rounded p-3 border border-gray-200">
                                                        <h4 className="font-semibold text-gray-800 mb-2">{route}</h4>
                                                        <div className="grid grid-cols-2 gap-2">
                                                            {droppingPoints.map((dp, idx) => (
                                                                <div key={idx} className="text-sm text-gray-600 flex justify-between">
                                                                    <span>{dp.dropping_point}</span>
                                                                    <span className="font-medium text-blue-600">৳{dp.price}</span>
                                                                </div>
                                                            ))}
                                                        </div>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    )}

                                    {/* Privacy Policy */}
                                    {selectedProvider.privacy_policy && (
                                        <div className="bg-gray-50 rounded-lg p-4">
                                            <h3 className="font-bold text-lg text-gray-800 mb-3">Privacy Policy</h3>
                                            <div className="text-sm text-gray-700 whitespace-pre-line max-h-40 overflow-y-auto">
                                                {selectedProvider.privacy_policy}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            </>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
}

export default BusProviders;
