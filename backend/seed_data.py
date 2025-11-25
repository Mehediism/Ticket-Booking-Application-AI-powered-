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

    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'data', 'data.json')
    with open(data_path, 'r') as f:
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
    
    # Dynamically load provider files
    provider_files = {}
    bus_info_dir = os.path.join(base_dir, 'bus_info')
    if os.path.exists(bus_info_dir):
        for filename in os.listdir(bus_info_dir):
            if filename.endswith('.txt'):
                # key is the filename without extension, e.g. "hanif"
                provider_key = filename[:-4].lower() 
                provider_files[provider_key] = os.path.join(bus_info_dir, filename)
    else:
        print(f"Warning: {bus_info_dir} directory not found!")


    for provider in data['bus_providers']:
        try:
            contact_info = ""
            address = ""
            privacy_policy = ""
            
            # Match provider name case-insensitively
            provider_name_lower = provider['name'].lower()
            
            if provider_name_lower in provider_files:
                file_path = provider_files[provider_name_lower]
                print(f"  - Reading info from {file_path}")
                with open(file_path, 'r') as f:
                    content = f.read()
                    privacy_policy = content

                    for line in content.split('\n'):
                        if 'Contact Information:' in line:
                            contact_info = line.replace('Contact Information:', '').strip()
                        if 'Official Address:' in line:
                            address = line.replace('Official Address:', '').strip()
            else:
                print(f"  - No info file found for {provider['name']}")

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
    for provider_key, file_path in provider_files.items():
        try:
            # Use the key (filename) as provider name or try to format it nicely
            provider_name = provider_key.title() 
            with open(file_path, 'r') as f:
                content = f.read()
                BusDocument.create(provider_name, content)
                print(f"Created document for: {provider_name}")
        except Exception as e:
            print(f"Document for {provider_key} may already exist: {e}")

    print("\nDatabase seeding completed!")
    print("\nNote: If you see 'already exists' messages, that's normal for re-runs.")

if __name__ == "__main__":
    seed_database()
