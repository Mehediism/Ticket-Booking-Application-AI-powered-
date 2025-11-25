import json
import os
from dotenv import load_dotenv
from config.database import get_db_connection, init_database
from models.district import District
from models.dropping_point import DroppingPoint
from models.bus_provider import BusProvider
from models.provider_route import ProviderRoute
from models.bus_document import BusDocument

load_dotenv()

def seed_database():
    print("Initializing database schema...")
    init_database()

    print("Starting database seeding...")

    with open('data/data.json', 'r') as f:
        data = json.load(f)

    print("Seeding districts and dropping points...")
    for district in data['districts']:
        try:
            district_id = District.create(district['name'])
            print(f"Created district: {district['name']}")

            for dp in district['dropping_points']:
                DroppingPoint.create(district_id, dp['name'], dp['price'])
                print(f"  - Added dropping point: {dp['name']} (৳{dp['price']})")
        except Exception as e:
            print(f"District {district['name']} may already exist: {e}")
            district_obj = District.get_by_name(district['name'])
            if district_obj:
                district_id = district_obj['id']

    print("\nSeeding bus providers and routes...")
    provider_files = {
        "Desh Travel": "bus_info/desh travel.txt",
        "Ena": "bus_info/ena.txt",
        "Green Line": "bus_info/green line.txt"
    }

    for provider in data['bus_providers']:
        try:
            contact_info = ""
            address = ""
            privacy_policy = ""

            if provider['name'] in provider_files:
                with open(provider_files[provider['name']], 'r') as f:
                    content = f.read()
                    privacy_policy = content

                    for line in content.split('\n'):
                        if 'Contact Information:' in line:
                            contact_info = line.replace('Contact Information:', '').strip()
                        if 'Official Address:' in line:
                            address = line.replace('Official Address:', '').strip()

            provider_id = BusProvider.create(
                provider['name'],
                contact_info,
                address,
                privacy_policy
            )
            print(f"Created provider: {provider['name']}")

            for district_name in provider['coverage_districts']:
                district_obj = District.get_by_name(district_name)
                if district_obj:
                    ProviderRoute.create(provider_id, district_obj['id'])
                    print(f"  - Added route to: {district_name}")
        except Exception as e:
            print(f"Provider {provider['name']} may already exist: {e}")

    print("\nSeeding bus documents for RAG...")
    for provider_name, file_path in provider_files.items():
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                BusDocument.create(provider_name, content)
                print(f"Created document for: {provider_name}")
        except Exception as e:
            print(f"Document for {provider_name} may already exist: {e}")

    print("\nDatabase seeding completed!")
    print("\nNote: If you see 'already exists' messages, that's normal for re-runs.")

if __name__ == "__main__":
    seed_database()
