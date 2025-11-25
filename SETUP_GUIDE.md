# Complete Setup Guide - Bus Booking System

## Overview
This guide will help you set up the Bus Booking System with MySQL database and MVC architecture.

## What's New
- **MVC Architecture**: Clean separation of concerns
  - Models: Database operations
  - Controllers: Business logic
  - Views: API endpoints
- **MySQL Database**: Using XAMPP/phpMyAdmin instead of Supabase
- **RAG Pipeline**: AI assistant powered by Groq API
- **All task requirements fulfilled**

## Quick Start (5 minutes)

### 1. Start MySQL
- Open XAMPP Control Panel
- Start **Apache** and **MySQL**
- Verify MySQL is running at http://localhost/phpmyadmin

### 2. Create Database
- Open phpMyAdmin: http://localhost/phpmyadmin
- Click "New" to create database
- Database name: `busticketapp`
- Collation: `utf8mb4_general_ci` (default)
- Click "Create"

### 3. Configure Backend
```bash
cd backend
```

Edit `.env` file:
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=               # Leave empty if you haven't set a MySQL password
DB_NAME=busticketapp
GROQ_API_KEY=gsk_...       # Optional: Get from https://console.groq.com
```

### 4. Install and Seed
```bash
# Install Python packages
pip install -r requirements.txt

# Create tables and seed data
python seed_data.py
```

Expected output:
```
Initializing database schema...
Starting database seeding...
Created district: Dhaka
  - Added dropping point: Gabtoli (৳500)
  - Added dropping point: Mohakhali (৳550)
...
Database seeding completed!
```

### 5. Start Backend
```bash
# Option 1: Direct Python
python main.py

# Option 2: Uvicorn
uvicorn main:app --reload

# Backend runs at: http://localhost:8000
```

### 6. Start Frontend
Open new terminal:
```bash
# From project root
npm install
npm run dev

# Frontend runs at: http://localhost:5173
```

## Verify Setup

### Backend Health Check
```bash
curl http://localhost:8000
# Should return: {"message":"Bus Booking System API with MVC Architecture"}
```

### Check Districts
```bash
curl http://localhost:8000/districts
# Should return list of 10 districts
```

### Test Frontend
- Open: http://localhost:5173
- Click "Search Buses" tab
- Dropdowns should show districts
- Select "Dhaka" → "Rajshahi"
- Click "Search Buses"
- Should show available buses

## Troubleshooting

### Issue: Districts dropdown is empty

**Cause**: Backend not running or database not seeded

**Solution**:
1. Check backend is running: `curl http://localhost:8000`
2. Check database tables exist in phpMyAdmin
3. Re-run: `python seed_data.py`

### Issue: AI Assistant shows "Sorry, I encountered an error"

**Cause**: GROQ_API_KEY not set or invalid

**Solution**:
1. Get API key from https://console.groq.com
2. Update `.env` file
3. Restart backend
4. The AI will work in fallback mode without API key (limited functionality)

### Issue: "Can't connect to MySQL server"

**Cause**: MySQL not running or wrong credentials

**Solution**:
1. Start MySQL in XAMPP
2. Verify credentials in `.env`
3. Check MySQL port (default: 3306)

### Issue: "Database already exists" errors

**Cause**: Re-running seed_data.py

**Solution**: This is normal! The script handles duplicates gracefully

## MVC Architecture Overview

### Directory Structure
```
backend/
├── config/
│   └── database.py          # Database connection pool
├── models/                  # Data models (M)
│   ├── district.py
│   ├── dropping_point.py
│   ├── bus_provider.py
│   ├── provider_route.py
│   ├── booking.py
│   └── bus_document.py
├── controllers/             # Business logic (C)
│   ├── bus_controller.py
│   ├── booking_controller.py
│   └── chat_controller.py
├── main.py                  # API endpoints (V)
├── seed_data.py            # Database seeder
└── requirements.txt
```

### How It Works

1. **Client Request** → Frontend sends API request
2. **View (main.py)** → FastAPI endpoint receives request
3. **Controller** → Business logic processes request
4. **Model** → Database operations
5. **Response** → Data flows back through layers

Example: Booking a ticket
```
POST /book-ticket
  ↓
main.py (view)
  ↓
booking_controller.create_booking() (controller)
  ↓
Booking.create() (model)
  ↓
MySQL database
```

## Database Schema

### Tables Created
1. **districts** - 10 major districts
2. **dropping_points** - Multiple points per district with fares
3. **bus_providers** - 6 providers with contact info
4. **provider_routes** - Junction table for provider-district mapping
5. **bookings** - Passenger booking records
6. **bus_documents** - Privacy policies for RAG pipeline

### Sample Queries
```sql
-- View all districts
SELECT * FROM districts;

-- View routes with provider names
SELECT bp.name as provider, d.name as district
FROM provider_routes pr
JOIN bus_providers bp ON pr.provider_id = bp.id
JOIN districts d ON pr.district_id = d.id;

-- View all bookings
SELECT * FROM bookings ORDER BY created_at DESC;
```

## API Endpoints

### Public Endpoints
- `GET /` - Health check
- `GET /districts` - List all districts
- `GET /bus-providers` - List all providers
- `POST /search-buses` - Search available buses
- `POST /book-ticket` - Book a ticket
- `GET /my-bookings/{phone}` - Get bookings by phone
- `POST /cancel-booking` - Cancel a booking
- `POST /chat` - AI assistant endpoint

### Example API Calls

**Search Buses:**
```bash
curl -X POST http://localhost:8000/search-buses \
  -H "Content-Type: application/json" \
  -d '{
    "from_district": "Dhaka",
    "to_district": "Rajshahi",
    "max_price": 500
  }'
```

**Book Ticket:**
```bash
curl -X POST http://localhost:8000/book-ticket \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Doe",
    "customer_phone": "01712345678",
    "from_district": "Dhaka",
    "to_district": "Rajshahi",
    "dropping_point": "Shah Makhdum",
    "bus_provider": "Desh Travel",
    "travel_date": "2025-12-01",
    "fare": 480
  }'
```

## RAG Pipeline Details

### How AI Assistant Works

1. **User Query** → "Which buses go to Rajshahi?"
2. **Document Search** → Searches bus_documents table
3. **Context Building** → Combines:
   - Provider documents
   - District data
   - Route information
4. **LLM Processing** → Groq API generates response
5. **User Response** → Natural language answer

### Fallback Mode
Without GROQ_API_KEY, the assistant uses rule-based responses:
- Contact queries → Returns provider contacts
- Route queries → Lists routes from database
- General queries → Basic information

## Testing Checklist

- [ ] MySQL running in XAMPP
- [ ] Database `busticketapp` created
- [ ] Backend dependencies installed
- [ ] Database seeded successfully
- [ ] Backend running on port 8000
- [ ] API health check responds
- [ ] Districts endpoint returns data
- [ ] Frontend running on port 5173
- [ ] District dropdowns populated
- [ ] Bus search works
- [ ] Booking creation works
- [ ] My Bookings lookup works
- [ ] AI Assistant responds (basic mode without API key)

## Docker Alternative

If you prefer Docker:

1. Update `.env`:
```
DB_HOST=host.docker.internal  # Instead of localhost
```

2. Start container:
```bash
docker-compose up -d
```

3. Seed database:
```bash
docker exec -it busticketapp_backend python seed_data.py
```

## Getting GROQ API Key

1. Visit: https://console.groq.com
2. Sign up/Login
3. Go to API Keys section
4. Create new API key
5. Copy key to `.env` file
6. Restart backend

## Support

If you encounter issues:
1. Check MySQL is running in XAMPP
2. Verify database `busticketapp` exists
3. Check backend logs for errors
4. Verify .env file configuration
5. Ensure all dependencies are installed

## Success Indicators

You know everything is working when:
- ✅ Backend shows "Database initialized successfully"
- ✅ Frontend loads without console errors
- ✅ District dropdowns show all 10 districts
- ✅ Search returns bus results
- ✅ Bookings can be created and viewed
- ✅ AI Assistant responds (even in fallback mode)

Enjoy your Bus Booking System!
