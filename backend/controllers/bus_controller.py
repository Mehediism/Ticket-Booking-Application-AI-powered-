from models.district import District
from models.dropping_point import DroppingPoint
from models.bus_provider import BusProvider

class BusController:
    @staticmethod
    def search_buses(from_district, to_district, max_price=None):
        from_providers = BusProvider.get_providers_serving_district(from_district)
        to_providers = BusProvider.get_providers_serving_district(to_district)

        from_names = {p['name'] for p in from_providers}
        to_names = {p['name'] for p in to_providers}
        available_providers = from_names & to_names

        dropping_points = DroppingPoint.get_by_district_name(to_district)

        if max_price:
            dropping_points = [dp for dp in dropping_points if dp['price'] <= max_price]

        results = []
        for provider_name in available_providers:
            provider = BusProvider.get_by_name(provider_name)
            for dp in dropping_points:
                results.append({
                    "provider": provider_name,
                    "provider_details": provider,
                    "from_district": from_district,
                    "to_district": to_district,
                    "dropping_point": dp['name'],
                    "fare": dp['price']
                })

        return results

    @staticmethod
    def get_all_districts():
        return District.get_all()

    @staticmethod
    def get_all_providers():
        return BusProvider.get_all()
