from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

from config.database import init_database
from controllers.bus_controller import BusController
from controllers.booking_controller import BookingController
from controllers.chat_controller import ChatController

load_dotenv()

app = FastAPI(title="Bus Booking System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    init_database()
    print("Database initialized successfully")
except Exception as e:
    print(f"Database initialization error: {e}")

class SearchBusRequest(BaseModel):
    from_district: str
    to_district: str
    max_price: Optional[int] = None

class BookingRequest(BaseModel):
    customer_name: str
    customer_phone: str
    from_district: str
    to_district: str
    dropping_point: str
    bus_provider: str
    travel_date: str
    fare: int

class CancelBookingRequest(BaseModel):
    booking_reference: str
    customer_phone: str

class ChatRequest(BaseModel):
    message: str

bus_controller = BusController()
booking_controller = BookingController()
chat_controller = ChatController()

@app.get("/")
def read_root():
    return {"message": "Bus Booking System API with MVC Architecture"}

@app.post("/search-buses")
def search_buses(request: SearchBusRequest):
    try:
        results = bus_controller.search_buses(
            request.from_district,
            request.to_district,
            request.max_price
        )
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/book-ticket")
def book_ticket(request: BookingRequest):
    try:
        result = booking_controller.create_booking(
            request.customer_name,
            request.customer_phone,
            request.from_district,
            request.to_district,
            request.dropping_point,
            request.bus_provider,
            request.travel_date,
            request.fare
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/my-bookings/{phone}")
def get_bookings(phone: str):
    try:
        bookings = booking_controller.get_bookings_by_phone(phone)
        return {"bookings": bookings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/cancel-booking")
def cancel_booking(request: CancelBookingRequest):
    try:
        result = booking_controller.cancel_booking(
            request.booking_reference,
            request.customer_phone
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/districts")
def get_districts():
    try:
        districts = bus_controller.get_all_districts()
        return {"districts": districts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/bus-providers")
def get_bus_providers():
    try:
        providers = bus_controller.get_all_providers()
        return {"providers": providers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/bus-providers/{provider_name}")
def get_provider_details(provider_name: str):
    try:
        details = bus_controller.get_provider_details(provider_name)
        if not details:
            raise HTTPException(status_code=404, detail="Provider not found")
        return details
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/bus-providers/district/{district_name}")
def get_providers_by_district(district_name: str):
    try:
        providers = bus_controller.get_providers_by_district(district_name)
        return {"providers": providers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        response = chat_controller.process_query(request.message)
        return {"response": response}
    except Exception as e:
        return {"response": f"I'm having trouble processing your question. Error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
