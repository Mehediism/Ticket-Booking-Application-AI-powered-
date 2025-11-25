# Quick Start Guide

## Get Up and Running in 3 Steps

### Step 1: Seed the Database (One-time setup)

```bash
cd backend
pip install -r requirements.txt
python seed_data.py
cd ..
```

### Step 2: Start the Backend

**Option A: Using Docker (Recommended)**
```bash
docker-compose up -d
```

**Option B: Without Docker**
```bash
cd backend
python main.py
```

Backend will be available at: `http://localhost:8000`

### Step 3: Start the Frontend

```bash
npm install
npm run dev
```

Frontend will be available at: `http://localhost:5173`

## Try These Features

### 1. Search for Buses
- Go to "Search Buses" tab
- Select: From "Dhaka" To "Rajshahi"
- Set max price: 500
- Click "Search Buses"

### 2. Book a Ticket
- Click "Book Now" on any result
- Enter your name and phone
- Select a travel date
- Confirm booking
- Save your booking reference!

### 3. View Your Bookings
- Go to "My Bookings" tab
- Enter your phone number
- View all your bookings

### 4. Ask the AI Assistant
- Go to "AI Assistant" tab
- Try these questions:
  - "Are there any buses from Dhaka to Rajshahi under 500 taka?"
  - "What are the contact details of Desh Travel?"
  - "Which buses serve Sylhet?"

## Stopping the Application

**Backend (Docker):**
```bash
docker-compose down
```

**Backend (Manual):**
Press `Ctrl+C` in the terminal

**Frontend:**
Press `Ctrl+C` in the terminal

## Troubleshooting

**Backend won't start?**
- Check if port 8000 is available
- Ensure .env file exists in backend/
- Verify Python dependencies are installed

**Frontend won't start?**
- Check if port 5173 is available
- Run `npm install` again
- Clear node_modules and reinstall

**Database errors?**
- Ensure seed_data.py ran successfully
- Check Supabase connection in .env
- Verify tables were created

## Need Help?

Check the detailed documentation:
- **README.md** - Full setup instructions
- **RAG_IMPLEMENTATION.md** - RAG architecture
- **PROJECT_SUMMARY.md** - Complete overview

## Example API Requests

**Search Buses:**
```bash
curl -X POST http://localhost:8000/search-buses \
  -H "Content-Type: application/json" \
  -d '{"from_district":"Dhaka","to_district":"Rajshahi","max_price":500}'
```

**Get Districts:**
```bash
curl http://localhost:8000/districts
```

**Chat with AI:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Which buses go from Dhaka to Chattogram?"}'
```

Happy booking!
