from models.bus_document import BusDocument
from models.district import District
from models.bus_provider import BusProvider
from models.provider_route import ProviderRoute
from models.dropping_point import DroppingPoint
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
            # Get all providers to check against query
            providers = BusProvider.get_all()
            
            relevant_docs = []
            # Check if any provider name is mentioned in the query
            for provider in providers:
                if provider['name'].lower() in user_query.lower():
                    # Fetch specific document for this provider
                    # We can use search with just the provider name to get their doc
                    docs = BusDocument.search(provider['name'], limit=1)
                    relevant_docs.extend(docs)
            
            # If no specific provider mentioned, or to add more context, do a general search
            if not relevant_docs:
                search_term = user_query
                query_lower = user_query.lower()
                
                if "cancel" in query_lower or "refund" in query_lower:
                    search_term = "Cancellation Policy"
                elif "contact" in query_lower or "phone" in query_lower or "email" in query_lower:
                    search_term = "Contact Information"
                elif "address" in query_lower:
                    search_term = "Official Address"
                    
                relevant_docs = BusDocument.search(search_term, limit=3)
                
            # Deduplicate docs based on id or content
            seen_content = set()
            unique_docs = []
            for doc in relevant_docs:
                if doc['content'] not in seen_content:
                    unique_docs.append(doc)
                    seen_content.add(doc['content'])
            
            context = "\n\n".join([doc["content"] for doc in unique_docs])

            districts = District.get_all()
            providers = BusProvider.get_all()
            routes = ProviderRoute.get_all()

            # Build routes summary with provider coverage
            routes_summary = {}
            for route in routes:
                provider = route['provider_name']
                district = route['district_name']
                if provider not in routes_summary:
                    routes_summary[provider] = []
                routes_summary[provider].append(district)

            # Get all dropping points with prices for each district
            district_fares = {}
            for district in districts:
                dropping_points = DroppingPoint.get_by_district_name(district['name'])
                district_fares[district['name']] = [
                    {
                        'dropping_point': dp['name'],
                        'price': dp['price']
                    }
                    for dp in dropping_points
                ]

            system_context = f"""You are a helpful bus booking assistant. Use the following information to answer questions:

AVAILABLE DISTRICTS: {json.dumps([d['name'] for d in districts])}

BUS PROVIDERS AND THEIR ROUTES:
{json.dumps(routes_summary, indent=2)}

FARES BY DISTRICT (Dropping Points and Prices in Taka):
{json.dumps(district_fares, indent=2)}

PROVIDER DETAILS:
{context}

IMPORTANT INSTRUCTIONS:
- When asked about fares/prices, check the FARES BY DISTRICT section
- To find buses from District A to District B under X taka:
  1. Find providers that serve BOTH District A and District B (check BUS PROVIDERS AND THEIR ROUTES)
  2. Look up the fares for District B in FARES BY DISTRICT
  3. List providers with fares under X taka
- Always mention the dropping point name along with the price
- Prices are in Bangladeshi Taka (৳)
- Be specific with numbers and provider names
- If asked about contact details, address, or cancellation, check the PROVIDER DETAILS section.

Answer the user's question accurately based on this data."""

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
