import { useState } from 'react';
import { Bus, Ticket, MessageCircle, Building2 } from 'lucide-react';
import SearchBuses from './components/SearchBuses';
import MyBookings from './components/MyBookings';
import ChatAssistant from './components/ChatAssistant';
import BusProviders from './components/BusProviders';

type TabType = 'search' | 'bookings' | 'chat' | 'providers';

function App() {
  const [activeTab, setActiveTab] = useState<TabType>('search');

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center gap-3">
            <Bus size={32} className="text-blue-600" />
            <div>
              <h1 className="text-3xl font-bold text-gray-800">Bus Booking System</h1>
              <p className="text-sm text-gray-600">Book your journey with ease</p>
            </div>
          </div>
        </div>
      </header>

      <nav className="bg-white border-b shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex gap-1">
            <button
              onClick={() => setActiveTab('search')}
              className={`flex items-center gap-2 px-6 py-4 font-medium transition-colors border-b-2 ${activeTab === 'search'
                ? 'text-blue-600 border-blue-600'
                : 'text-gray-600 border-transparent hover:text-gray-800'
                }`}
            >
              <Bus size={20} />
              Search Buses
            </button>
            <button
              onClick={() => setActiveTab('bookings')}
              className={`flex items-center gap-2 px-6 py-4 font-medium transition-colors border-b-2 ${activeTab === 'bookings'
                ? 'text-blue-600 border-blue-600'
                : 'text-gray-600 border-transparent hover:text-gray-800'
                }`}
            >
              <Ticket size={20} />
              My Bookings
            </button>
            <button
              onClick={() => setActiveTab('chat')}
              className={`flex items-center gap-2 px-6 py-4 font-medium transition-colors border-b-2 ${activeTab === 'chat'
                ? 'text-blue-600 border-blue-600'
                : 'text-gray-600 border-transparent hover:text-gray-800'
                }`}
            >
              <MessageCircle size={20} />
              AI Assistant
            </button>
            <button
              onClick={() => setActiveTab('providers')}
              className={`flex items-center gap-2 px-6 py-4 font-medium transition-colors border-b-2 ${activeTab === 'providers'
                ? 'text-blue-600 border-blue-600'
                : 'text-gray-600 border-transparent hover:text-gray-800'
                }`}
            >
              <Building2 size={20} />
              Bus Providers
            </button>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {activeTab === 'search' && <SearchBuses />}
        {activeTab === 'bookings' && <MyBookings />}
        {activeTab === 'chat' && <ChatAssistant />}
        {activeTab === 'providers' && <BusProviders />}
      </main>

      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6 text-center text-gray-600">
          <p className="text-sm">Bus Booking System - Your trusted travel partner</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
