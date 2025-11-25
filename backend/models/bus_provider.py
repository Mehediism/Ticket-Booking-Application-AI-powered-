from config.database import get_db_connection
import os
import re

class BusProvider:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM bus_providers ORDER BY name")
            results = cursor.fetchall()
            cursor.close()
            return results
        finally:
            conn.close()

    @staticmethod
    def get_by_name(name):
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM bus_providers WHERE name = %s", (name,))
            result = cursor.fetchone()
            cursor.close()
            return result
        finally:
            conn.close()

    @staticmethod
    def create(name, contact_info="", address="", privacy_policy=""):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO bus_providers (name, contact_info, address, privacy_policy) VALUES (%s, %s, %s, %s)",
                (name, contact_info, address, privacy_policy)
            )
            conn.commit()
            provider_id = cursor.lastrowid
            cursor.close()
            return provider_id
        finally:
            conn.close()

    @staticmethod
    def get_providers_serving_district(district_name):
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT DISTINCT bp.*
                FROM bus_providers bp
                JOIN provider_routes pr ON bp.id = pr.provider_id
                JOIN districts d ON pr.district_id = d.id
                WHERE d.name = %s
            """, (district_name,))
            results = cursor.fetchall()
            cursor.close()
            return results
        finally:
            conn.close()

    @staticmethod
    def get_provider_details(provider_name):
        """Get detailed provider information including data from text files"""
        # Get basic provider info from database
        provider = BusProvider.get_by_name(provider_name)
        if not provider:
            return None
        
        # Read additional info from text file
        bus_info_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'bus_info')
        file_path = os.path.join(bus_info_dir, f"{provider_name.lower()}.txt")
        
        contact_info = ""
        address = ""
        privacy_policy = ""
        website = ""
        
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Extract contact information
                contact_match = re.search(r'Contact Information:\s*(.+?)(?:\n|Privacy Policy)', content, re.DOTALL)
                if contact_match:
                    contact_info = contact_match.group(1).strip()
                
                # Extract address
                address_match = re.search(r'Official Address:\s*(.+?)(?:\n|Contact)', content, re.DOTALL)
                if address_match:
                    address = address_match.group(1).strip()
                
                # Extract privacy policy link
                privacy_match = re.search(r'Privacy Policy / Terms Link:\s*(.+?)(?:\n|$)', content)
                if privacy_match:
                    website = privacy_match.group(1).strip()
                
                # Get full privacy policy text
                privacy_policy = content.strip()
        
        # Get coverage districts
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT d.name
                FROM districts d
                JOIN provider_routes pr ON d.id = pr.district_id
                WHERE pr.provider_id = %s
                ORDER BY d.name
            """, (provider['id'],))
            coverage_districts = [row['name'] for row in cursor.fetchall()]
            cursor.close()
        finally:
            conn.close()
        
        # Get all routes
        routes = BusProvider.get_provider_routes(provider_name)
        
        return {
            'id': provider['id'],
            'name': provider['name'],
            'contact_info': contact_info,
            'address': address,
            'privacy_policy': privacy_policy,
            'website': website,
            'coverage_districts': coverage_districts,
            'routes': routes
        }

    @staticmethod
    def get_provider_routes(provider_name):
        """Get all routes served by a provider"""
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT DISTINCT 
                    d1.name as from_district,
                    d2.name as to_district,
                    dp.name as dropping_point,
                    dp.price
                FROM bus_providers bp
                JOIN provider_routes pr1 ON bp.id = pr1.provider_id
                JOIN districts d1 ON pr1.district_id = d1.id
                JOIN provider_routes pr2 ON bp.id = pr2.provider_id
                JOIN districts d2 ON pr2.district_id = d2.id
                JOIN dropping_points dp ON d2.id = dp.district_id
                WHERE bp.name = %s AND d1.id != d2.id
                ORDER BY d1.name, d2.name, dp.name
            """, (provider_name,))
            results = cursor.fetchall()
            cursor.close()
            
            # Group routes by from-to districts
            routes = {}
            for row in results:
                route_key = f"{row['from_district']} → {row['to_district']}"
                if route_key not in routes:
                    routes[route_key] = []
                routes[route_key].append({
                    'dropping_point': row['dropping_point'],
                    'price': row['price']
                })
            
            return routes
        finally:
            conn.close()
