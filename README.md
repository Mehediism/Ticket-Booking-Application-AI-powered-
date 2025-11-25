# Bus Booking System

A comprehensive bus ticket booking application with an AI-powered RAG (Retrieval-Augmented Generation) assistant. Users can search for buses, book tickets, manage bookings, and get intelligent answers to their queries.

## Features

- **Bus Search**: Search for available buses between districts with optional price filtering
- **Ticket Booking**: Book tickets with passenger information and travel date
- **Booking Management**: View and cancel bookings using phone number
- **AI Assistant**: RAG-powered chatbot that answers questions about routes, providers, fares, and bookings
- **Provider Information**: Access detailed information about bus providers including contact details and privacy policies

## Technology Stack

### Backend
- FastAPI (Python) with **MVC Architecture**
- MySQL (via XAMPP/phpMyAdmin)
- Groq API (LLM for RAG pipeline)
- Docker support for containerized deployment

### Frontend
- React with TypeScript
- Vite
- TailwindCSS
- Lucide React (icons)

## Architecture

### MVC Structure
The backend follows the Model-View-Controller pattern:
- **Models**: Database operations (`models/`)
  - `district.py`, `bus_provider.py`, `booking.py`, etc.
- **Controllers**: Business logic (`controllers/`)
  - `bus_controller.py`, `booking_controller.py`, `chat_controller.py`
- **Views**: API endpoints (`main.py`)
- **Config**: Database configuration (`config/database.py`)

### RAG Pipeline
The application demonstrates a RAG pipeline where:
1. Bus provider documents are stored in the database
2. User queries are processed using semantic search
3. Relevant documents are retrieved and used as context
4. Groq's LLM generates intelligent responses based on the context

## Prerequisites

- Python 3.9+
- Node.js 18+
- XAMPP (MySQL/phpMyAdmin) running on http://localhost/phpmyadmin
- MySQL database named `busticketapp` created
- Docker and Docker Compose (optional, for containerized setup)
- Groq API key (for AI assistant)

## Setup Instructions

### Step 1: Database Setup

1. **Start XAMPP** and ensure MySQL is running
2. **Create Database**:
   - Open http://localhost/phpmyadmin
   - Create a new database named `busticketapp`
   - Leave it empty (tables will be created automatically)

### Step 2: Backend Configuration

1. **Navigate to backend directory**:
```bash
cd backend
```

2. **Configure environment variables** in `.env`:
```bash
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=        # Your MySQL password (empty by default in XAMPP)
DB_NAME=busticketapp
GROQ_API_KEY=gsk_your_groq_api_key_here  # Get from https://groq.com
```

3. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

4. **Seed the database** (one-time setup):
```bash
python seed_data.py
```
This will:
- Create all necessary tables
- Insert districts and dropping points
- Add bus providers and routes
- Load privacy policy documents for RAG

### Step 3: Start the Backend

**Option A: Direct Python**
```bash
python main.py
```

**Option B: Using Docker**
```bash
# From project root
docker-compose up -d
```
Note: For Docker, change `DB_HOST` to `host.docker.internal` in `.env`

The backend will run on `http://localhost:8000`

### Step 4: Start the Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will run on `http://localhost:5173`

## Verification

1. Check backend is running: http://localhost:8000
2. Check districts API: http://localhost:8000/districts
3. Open frontend: http://localhost:5173
4. Try searching for buses
5. Test the AI assistant

## Usage

### Searching for Buses

1. Go to the "Search Buses" tab
2. Select departure and destination districts
3. Optionally set a maximum price
4. Click "Search Buses"
5. Browse available buses and click "Book Now"

### Booking a Ticket

1. After searching, click "Book Now" on any available bus
2. Fill in your name, phone number, and travel date
3. Confirm the booking
4. Save your booking reference number

### Managing Bookings

1. Go to the "My Bookings" tab
2. Enter your phone number
3. View all your bookings
4. Cancel bookings if needed (confirmed bookings only)

### Using the AI Assistant

1. Go to the "AI Assistant" tab
2. Ask questions like:
   - "Are there any buses from Dhaka to Rajshahi under 500 taka?"
   - "Show all bus providers operating from Chattogram to Sylhet"
   - "What are the contact details of Hanif Bus?"
   - "Which buses serve Khulna?"

## API Endpoints

### Backend API (FastAPI)

- `GET /` - API health check
- `POST /search-buses` - Search for available buses
- `POST /book-ticket` - Book a ticket
- `GET /my-bookings/{phone}` - Get bookings by phone number
- `POST /cancel-booking` - Cancel a booking
- `GET /districts` - Get all districts
- `GET /bus-providers` - Get all bus providers
- `POST /chat` - Send a message to the RAG assistant

## Database Schema

### Tables

- **districts**: Available districts
- **dropping_points**: Dropping points with fares
- **bus_providers**: Bus provider information
- **provider_routes**: Routes served by providers
- **bookings**: Passenger bookings
- **bus_documents**: Documents for RAG pipeline

All tables have Row Level Security (RLS) enabled with appropriate policies for public access.

## RAG Pipeline

The RAG (Retrieval-Augmented Generation) pipeline works as follows:

1. **Document Storage**: Bus provider information is stored in the `bus_documents` table
2. **Query Processing**: User questions are sent to the chat endpoint
3. **Context Retrieval**: Relevant documents and database records are retrieved
4. **Response Generation**: Groq's LLM generates contextual responses using the retrieved information
5. **Answer Delivery**: The intelligent response is returned to the user

## Example Questions for AI Assistant

- "Are there any buses from Dhaka to Rajshahi under 500 taka?"
- "Show all bus providers operating from Chattogram to Sylhet"
- "What are the contact details of Desh Travel?"
- "Can I cancel my booking for the bus from Dhaka to Barishal?"
- "Which bus companies serve Rangpur?"
- "What is Green Line's contact information?"

## Data Sources

The application uses the following data:

- **Districts**: 10 major districts in Bangladesh
- **Bus Providers**: 6 providers (Desh Travel, Hanif, Ena, Green Line, Soudia, Shyamoli)
- **Privacy Policies**: Detailed documents for Desh Travel, Ena, and Green Line

## Security Features

- Row Level Security (RLS) on all database tables
- Phone-based booking access control
- Input validation on all forms
- Secure API communication

## Development

### Type Checking

```bash
npm run typecheck
```

### Linting

```bash
npm run lint
```

### Building for Production

```bash
npm run build
```

## Project Structure

```
.
├── backend/
│   ├── bus_info/          # Bus provider documents
│   ├── config/            # Database configuration
│   ├── controllers/       # Business logic controllers
│   ├── data/              # JSON data files
│   ├── models/            # Database models
│   ├── main.py            # FastAPI application
│   ├── seed_data.py       # Database seeding script
│   └── requirements.txt   # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── api.ts         # API client functions
│   │   ├── types.ts       # TypeScript types
│   │   └── App.tsx        # Main application component
│   ├── public/            # Static assets
│   ├── package.json       # Node dependencies
│   └── README.md          # Frontend documentation
├── docker-compose.yml     # Docker configuration
└── README.md              # This file
```

## Notes

- The MySQL database is set up via XAMPP or Docker
- The GROQ API key is pre-configured for the RAG pipeline
- All booking operations require a valid phone number for tracking
- Booking references are unique 8-character codes

## Support

For issues or questions about the application, use the AI Assistant feature or check the provider contact information in the bus documents.
