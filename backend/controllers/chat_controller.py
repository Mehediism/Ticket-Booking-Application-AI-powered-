from models.bus_document import BusDocument
from models.district import District
from models.bus_provider import BusProvider
from models.provider_route import ProviderRoute
from groq import Groq
import os
import json

class ChatController:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or api_key == "gsk_your_groq_api_key_here":
            self.groq_client = None
        else:
            self.groq_client = Groq(api_key=api_key)

    def process_query(self, user_query):
        if not self.groq_client:
            return self._fallback_response(user_query)

        try:
            relevant_docs = BusDocument.search(user_query, limit=3)
            context = "\n\n".join([doc["content"] for doc in relevant_docs])

            districts = District.get_all()
            providers = BusProvider.get_all()
            routes = ProviderRoute.get_all()

            routes_summary = {}
            for route in routes:
                provider = route['provider_name']
                district = route['district_name']
                if provider not in routes_summary:
                    routes_summary[provider] = []
                routes_summary[provider].append(district)

            system_context = f"""You are a helpful bus booking assistant. Use the following information to answer questions:

AVAILABLE DISTRICTS: {json.dumps([d['name'] for d in districts])}

BUS PROVIDERS AND THEIR ROUTES:
{json.dumps(routes_summary, indent=2)}

PROVIDER DETAILS:
{context}

Answer the user's question accurately based on this data. If asking about routes or availability, check if both districts are served by the same provider. For fare information, explain that fares vary by dropping point and destination."""

            response = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_context},
                    {"role": "user", "content": user_query}
                ],
                temperature=0.7,
                max_tokens=1000
            )

            return response.choices[0].message.content
        except Exception as e:
            return f"I encountered an error processing your request: {str(e)}"

    def _fallback_response(self, query):
        query_lower = query.lower()

        if "contact" in query_lower or "phone" in query_lower or "email" in query_lower:
            docs = BusDocument.get_all()
            response = "Here are the contact details I have:\n\n"
            for doc in docs:
                if "Contact Information:" in doc['content']:
                    lines = doc['content'].split('\n')
                    for line in lines:
                        if "Contact Information:" in line or "Email:" in line:
                            response += f"{doc['provider_name']}: {line.strip()}\n"
            return response

        elif "district" in query_lower or "route" in query_lower or "serve" in query_lower:
            routes = ProviderRoute.get_all()
            routes_summary = {}
            for route in routes:
                provider = route['provider_name']
                district = route['district_name']
                if provider not in routes_summary:
                    routes_summary[provider] = []
                routes_summary[provider].append(district)

            response = "Here are the available routes:\n\n"
            for provider, districts in routes_summary.items():
                response += f"{provider}: {', '.join(districts)}\n"
            return response

        else:
            return "I can help you with information about bus routes, providers, bookings, and contact details. Please note: The GROQ API key is not configured, so I'm providing basic information. What would you like to know?"
